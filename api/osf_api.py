import settings
import json
import os
import logging
import requests

from pythosf import client
logger = logging.getLogger(__name__)


def get_default_session():
    return client.Session(api_base_url=settings.API_DOMAIN, auth=(settings.USER_ONE, settings.USER_ONE_PASSWORD))


def create_project(session, title='osf selenium test', tags=None, **kwargs):
    """Create a project for your current user through the OSF api.

    By default, projects will be given the `qatest` tag just in case deleting fails.
    If testing search, you will want to give the project no tags (or different tags).
    """
    if tags is None:
        tags = ['qatest', os.environ['PYTEST_CURRENT_TEST']]
    node = client.Node(session=session)
    node.create(title=title, tags=tags, **kwargs)
    return node


def current_user(session=None):
    if not session:
        session = get_default_session()
    user = client.User(session=session)
    user.get()
    return user


def get_node(session, node_id=settings.PREFERRED_NODE):
    return client.Node(session=session, id=node_id)


def get_user_institutions(session, user=None):
    if not user:
        user = current_user(session)
    institution_url = user.relationships.institutions['links']['related']['href']
    data = session.get(institution_url)
    institutions = []
    for institution in data['data']:
        institutions.append(institution['attributes']['name'])
    return institutions


def get_user_addon(session, provider, user=None):
    """Get list of accounts on the given provider that have already been connected by the user."""
    if not user:
        user = current_user(session)
    addon_url = '/v2/users/{}/addons/{}/'.format(user.id, provider)
    return session.get(addon_url)


def upload_single_quickfile(session):
    """Upload a new quickfile. Delete existing quickfiles first.
    Note: Currently using v2.0 of the API. Certain lines will need to be changed on update.
    TODO: Make this more general.
    """

    user = current_user(session)
    quickfiles_url = user.relationships.quickfiles['links']['related']['href']
    delete_all_quickfiles(session, quickfiles_url)

    upload_url = user.relationships.quickfiles['links']['upload']['href']
    return upload_fake_file(session, upload_url=upload_url, quickfile=True)


def delete_all_quickfiles(session, quickfiles_url):
    """ Delete all quickfiles. Just pass in the quickfiles url for the currently logged in user.
    """

    for quickfile in session.get(quickfiles_url)['data']:
        delete_url = quickfile['links']['delete']
        delete_file(session, delete_url)


def get_all_institutions(session):
    url = '/v2/institutions/'
    data = session.get(url)
    institutions = []
    for institution in data['data']:
        institutions.append(institution['attributes']['name'])
    return institutions


def delete_all_user_projects(session, user=None):
    """Delete all of your user's projects that they have permission to delete
    except PREFERRED_NODE (if it's set).
    """
    if not user:
        user = current_user(session)
    nodes_url = user.relationships.nodes['links']['related']['href']
    for _ in range(3):
        try:
            data = session.get(nodes_url)
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code == 502:
                logger.warning('502 Exception caught. Re-trying test')
                continue
            raise exc
        else:
            break
    else:
        logger.info('Max tries attempted')
        raise Exception('API not responding. Giving up.')

    nodes_failed = []
    for node in data['data']:
        if node['id'] != settings.PREFERRED_NODE:
            n = client.Node(id=node['id'], session=session)
            try:
                n.get()
                n.delete()
            except Exception as exc:
                nodes_failed.append((node['id'], exc))
                continue

    if nodes_failed:
        error_message_list = []
        for error_tuple in nodes_failed:
            # Position [0] of error_tuple contains node_id
            # Position [1] of error_tuple contains the exception
            error_message = "node '{}' errored with exception: '{}'".format(error_tuple[0], error_tuple[1])
            error_message_list.append(error_message)
        logger.error('\n'.join(error_message_list))


def delete_project(session, guid, user=None):
    """Delete a single project. Simply pass in the guid
    """
    if not user:
        user = current_user(session)
    nodes_url = user.relationships.nodes['links']['related']['href']
    data = session.get(nodes_url)
    for node in data['data']:
        if node['id'] == guid:
            n = client.Node(id=node['id'], session=session)
            n.get()
            n.delete()


def create_custom_collection(session):
    """Create a new custom collection. You can modify the title of the collection here as well.
    """
    collections_url = '{}/v2/collections/'.format(session.api_base_url)

    payload = {
        'title': 'Selenium API Custom Collection',
    }

    session.post(collections_url, item_type='collections', attributes=payload)


def delete_custom_collections(session):
    """Delete all custom collections for the current user.
    """
    collections_url = '{}/v2/collections/'.format(session.api_base_url)
    data = session.get(collections_url)

    for collection in data['data']:
        if not collection['attributes']['bookmarks']:
            collection_self_url = collections_url + collection['id']
            session.delete(url=collection_self_url, item_type=None)


# TODO rename this to get_node_providers, and create new function that actually IS get_node_addons -
#  note, this is confusing, talk to BrianG before we change this
def get_node_addons(session, node_id):
    """Return a list of the names of all the addons connected to the given node.
    """
    url = '/v2/nodes/{}/files/'.format(node_id)
    data = session.get(url, query_parameters={'page[size]': 20})
    providers = []
    for provider in data['data']:
        providers.append(provider['attributes']['provider'])
    return providers


def waffled_pages(session):
    waffle_list = []
    url = '/v2/_waffle/'
    data = session.get(url)
    for page in data['data']:
        if page['attributes']['active']:
            waffle_list.append(page['attributes']['name'])
    return waffle_list


def get_existing_file(session, node_id=settings.PREFERRED_NODE):
    """Return the name of the first file in OSFStorage on a given node.
    Uploads a new file if one does not exist.
    """
    node = client.Node(session=session, id=node_id)
    node.get()
    files_url = node.relationships.files['links']['related']['href']
    data = session.get(files_url + 'osfstorage/')
    file = data['data']
    if file:
        return data['data'][0]['attributes']['name']
    else:
        return upload_fake_file(session, node)


def upload_fake_file(session, node=None, name='osf selenium test file for testing because its fake.txt', upload_url=None, provider='osfstorage', quickfile=False):
    """Upload an almost empty file to the given node. Return the file's name.

    Note: The default file has a very long name because it makes it easier to click a link to it.
    Quickfiles Note: "/?create_guid=1" must be added via api BEFORE viewing on the front end. See ENG-1351 for more info
    """
    if not upload_url:
        if not node:
            raise TypeError('Node must not be none when upload URL is not set.')
        upload_url = '{}/v1/resources/{}/providers/{}/'.format(settings.FILE_DOMAIN, node.id, provider)

    metadata = session.put(url=upload_url, query_parameters={'kind': 'file', 'name': name}, raw_body={})

    if quickfile:
        # create_guid param is tied to the GET request so we can't use query_parameters={'create_guid': 1} here
        quickfile_path = metadata['data']['attributes']['path']
        info_link = '/v2/files{}/?create_guid=1'.format(quickfile_path)
        session.get(info_link)

    return name, metadata


def delete_addon_files(session, provider, current_browser, guid):
    """Delete all files for the given addon.
    """
    files_url = '{}/v2/nodes/{}/files/{}/'.format(session.api_base_url, guid, provider)

    data = session.get(url=files_url, query_parameters={'page[size]': 20})

    for file in data['data']:
        if file['attributes']['kind'] == 'file':
            delete_url = file['links']['delete']
            file_name = file['attributes']['name']
            if current_browser in file_name:
                delete_file(session, delete_url)


def delete_file(session, delete_url):
    """Delete a file.  A truly stupid method, caller must provide the delete url from the file
    metadata."""

    # include `item_type=None` b/c pythosf doesn't set a default value for this.
    return session.delete(url=delete_url, item_type=None)


def get_providers_list(session=None, type='preprints'):
    """Return the providers list data. The default is the preprint providers list.
    """
    if not session:
        session = get_default_session()
    url = '/v2/providers/' + type
    return session.get(url)['data']


def get_provider_submission_status(provider):
    """Return the boolean attribute `allow_submissions` from the dictionary object (provider)
    """
    return provider['attributes']['allow_submissions']


def get_providers_total(provider_name, session):
    """ Return the total number of preprints for a given service provider.
        Note: Reformat provider names to all lowercase and remove white spaces.
    """
    provider_url = '/v2/providers/preprints/{}/preprints/'.format(provider_name.lower().replace(' ', ''))
    return session.get(provider_url)['links']['meta']['total']


def connect_provider_root_to_node(
    session, provider, external_account_id,
    node_id=settings.PREFERRED_NODE,
):
    """Initialize the node<=>addon connection, add the given external_account_id, and configure it
    to connect to the root folder of the provider."""

    if not session:
        session = get_default_session()

    url = '/v2/nodes/{}/addons/{}/'.format(node_id, provider)

    # Empty POST request "turns it on" (h/t @brianjgeiger). Addon must be configured with a PATCH
    # afterwards.
    # TODO: if box is already connected, will return 400.  Handle that?
    session.post(url=url, item_type='node_addons')

    # This is a workaround for a bug in pythosf v0.0.9 that breaks patch requests.
    # If raw_body is not passed, the session code tries to automatically build the body, which
    # breaks on `item_id`.  If you build the body yourself and pass it in, this bypasses the
    # bug.  When the fix is released, switch to the commented-out block below this.
    raw_payload = {
        'data': {
            'type': 'node_addons',
            'id': provider,
            'attributes': {
                'external_account_id': external_account_id,
                'enabled': True,
            },
        },
    }
    addon = session.patch(
        url=url, item_type='node_addons', item_id=provider,
        raw_body=json.dumps(raw_payload),
    )
    # payload = {
    #     'external_account_id': external_account_id,
    #     'enabled': True,
    # }
    # addon = session.patch(url=url, item_type='node_addons', item_id=provider,
    #                      attributes=payload)

    # Assume the root folder is the first (and only) folder returned.  Get its id and update
    # the addon config
    root_folder = session.get(url + 'folders/')['data'][0]['attributes']['folder_id']
    raw_payload['data']['attributes']['folder_id'] = root_folder
    addon = session.patch(
        url=url, item_type='node_addons', item_id=provider,
        raw_body=json.dumps(raw_payload),
    )
    return addon
