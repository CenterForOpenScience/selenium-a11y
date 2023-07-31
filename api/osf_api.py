import json
import logging
import os

import requests
from pythosf import client

import settings

logger = logging.getLogger(__name__)


def get_default_session():
    return client.Session(
        api_base_url=settings.API_DOMAIN,
        auth=(settings.USER_ONE, settings.USER_ONE_PASSWORD),
    )


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


def get_all_institutions(session=None, data_type='names'):
    if not session:
        session = get_default_session()
    url = '/v2/institutions/'
    data = session.get(url)
    institutions = []
    if data_type == 'names':
        for institution in data['data']:
            institutions.append(institution['attributes']['name'])
    elif data_type == 'ids':
        for institution in data['data']:
            institutions.append(institution['id'])
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
            error_message = "node '{}' errored with exception: '{}'".format(
                error_tuple[0], error_tuple[1]
            )
            error_message_list.append(error_message)
        logger.error('\n'.join(error_message_list))


def delete_project(session, guid, user=None):
    """Delete a single project. Simply pass in the guid"""
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
    """Create a new custom collection. You can modify the title of the collection here as well."""
    collections_url = '{}/v2/collections/'.format(session.api_base_url)

    payload = {
        'title': 'Selenium API Custom Collection',
    }

    session.post(collections_url, item_type='collections', attributes=payload)


def delete_custom_collections(session):
    """Delete all custom collections for the current user."""
    collections_url = '{}/v2/collections/'.format(session.api_base_url)
    data = session.get(collections_url)

    for collection in data['data']:
        if not collection['attributes']['bookmarks']:
            collection_self_url = collections_url + collection['id']
            session.delete(url=collection_self_url, item_type=None)


# TODO rename this to get_node_providers, and create new function that actually IS get_node_addons -
#  note, this is confusing, talk to BrianG before we change this
def get_node_addons(session, node_id):
    """Return a list of the names of all the addons connected to the given node."""
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


def upload_fake_file(
    session,
    node=None,
    name='osf selenium test file for testing because its fake.txt',
    upload_url=None,
    provider='osfstorage',
):
    """Upload an almost empty file to the given node. Return the file's name.

    Note: The default file has a very long name because it makes it easier to click a link to it.
    """
    if not upload_url:
        if not node:
            raise TypeError('Node must not be none when upload URL is not set.')
        upload_url = '{}/v1/resources/{}/providers/{}/'.format(
            settings.FILE_DOMAIN, node.id, provider
        )

    metadata = session.put(
        url=upload_url, query_parameters={'kind': 'file', 'name': name}, raw_body={}
    )

    return name, metadata


def delete_addon_files(session, provider, current_browser, guid):
    """Delete all files for the given addon."""
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
    """Return the providers list data. The default is the preprint providers list."""
    if not session:
        session = get_default_session()
    url = '/v2/providers/' + type
    return session.get(url)['data']


def get_provider(session=None, type='registrations', provider_id='osf'):
    """Return the data for an individual provider. The default type is registrations but
    it can also be used for a preprints or collections provider.  The default provider_id
    is 'osf'
    """
    if not session:
        session = get_default_session()
    url = '/v2/providers/' + type + '/' + provider_id
    return session.get(url)['data']


def get_provider_submission_status(provider):
    """Return the boolean attribute `allow_submissions` from the dictionary object (provider)"""
    return provider['attributes']['allow_submissions']


def get_providers_total(provider_name, session):
    """Return the total number of preprints for a given service provider.
    Note: Reformat provider names to all lowercase and remove white spaces.
    """
    provider_url = '/v2/providers/preprints/{}/preprints/'.format(
        provider_name.lower().replace(' ', '')
    )
    return session.get(provider_url)['links']['meta']['total']


def connect_provider_root_to_node(
    session,
    provider,
    external_account_id,
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
        url=url,
        item_type='node_addons',
        item_id=provider,
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
        url=url,
        item_type='node_addons',
        item_id=provider,
        raw_body=json.dumps(raw_payload),
    )
    return addon


def get_registration_schemas_for_provider(session=None, provider_id='osf'):
    """Returns a list of allowed registration schemas for an individual provider.  The
    list will be a paired list of schema names and ids.  The The default provider_id is
    'osf'.
    """
    if not session:
        session = get_default_session()
    url = 'v2/providers/registrations/{}/schemas/'.format(provider_id)
    # NOTE: Using '50' as the page size query parameter here. We don't actually have 50
    # total registration schemas. It's under 30 at this time, but using 50 here gives us
    # plenty of room to add more schemas without having to update this function.
    data = session.get(url, query_parameters={'page[size]': 50})['data']
    if data is None:
        return None
    return [[schema['attributes']['name'], schema['id']] for schema in data]


def create_draft_registration(session, node_id=None, schema_id=None):
    """Create a new draft registration for a given project node."""
    if not session:
        session = get_default_session()
    url = '/v2/nodes/{}/draft_registrations/'.format(node_id)
    raw_payload = {
        'data': {
            'type': 'draft_registrations',
            'relationships': {
                'registration_schema': {
                    'data': {
                        'id': schema_id,
                        'type': 'registration-schemas',
                    }
                }
            },
        },
    }
    session.post(
        url=url, item_type='draft_registrations', raw_body=json.dumps(raw_payload)
    )


def get_most_recent_preprint_node_id(session=None):
    """Return the most recently published preprint node id"""
    if not session:
        session = get_default_session()
    url = '/v2/preprints/'
    data = session.get(url)['data']
    if data:
        for preprint in data:
            if preprint['attributes']['is_published']:
                return preprint['id']
    return None


def get_most_recent_registration_node_id(session=None):
    """Return the most recently approved public registration node id. The
    /v2/registrations endpoint currently returns the most recently modified
    registration sorted first. But we still need to check for a public and
    approved registration that has not been withdrawn in order to get a
    registration that is fully accessible.
    """
    if not session:
        session = get_default_session()
    url = '/v2/registrations/'
    data = session.get(url)['data']
    if data:
        for registration in data:
            if (
                registration['attributes']['public']
                and (registration['attributes']['revision_state'] == 'approved')
                and not registration['attributes']['withdrawn']
            ):
                return registration['id']
    return None
