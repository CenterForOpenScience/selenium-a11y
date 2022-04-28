import imaplib


class EmailAccess:
    def get_latest_email_body_by_imap(
        imap_host, email_address, password, mailbox, search_key, search_value
    ):
        """This method uses Internet Message Access Protocol (IMAP) to login to an IMAP
        enabled email address and retrieve the body of the latest email that matches the
        provided search criteria.
            Parameters:
            - imap_host: host imap email server
            - email_address: IMAP enabled email address
            - password: password for the IMAP enabled email address
            - mailbox: mailbox (a.k.a. label) from which you wish to retieve emails
                (ex: 'Inbox', 'Sent', or any created labels for a gmail account)
            - search_key: key used to filter list of retirieved emails - used as part
                of key value pair - see search_value below
                (ex: 'FROM', 'CC', 'SUBJECT', etc)
            - search_value: value used to filter list of retrieved emails - used as part
                of key value pair - see search_key above
                (ex: 'openscienceframework-noreply@osf.io' when used with 'FROM' key)
            Returns body text of requested email
        """
        imap = imap_connect_and_login(imap_host, email_address, password)
        # retrieve the emails in the given mailbox (a.k.a. label)
        imap.select(mailbox)
        # filter the email list by searching for the given key value pair
        result_uids = search(search_key, search_value, imap)
        # create a list of email uids
        uids_list = result_uids[0].split()
        # get the latest email uid from the list
        latest_uid = int(uids_list[-1])
        # fetch the body of the latest email
        res, email_body = imap.fetch(str(latest_uid), '(UID BODY[TEXT])')
        imap_close(imap)
        return email_body

    def get_count_of_unseen_emails_by_imap(imap_host, email_address, password):
        """This method uses Internet Message Access Protocol (IMAP) to login to an IMAP
        enabled email address and retrieve the count of unseen emails in the account inbox.
            Parameters:
            - imap_host: host imap email server
            - email_address: IMAP enabled email address
            - password: password for the IMAP enabled email address
            Returns the count of unseen emails in the account's inbox
        """
        imap = imap_connect_and_login(imap_host, email_address, password)
        # select mail from the Inbox
        imap.select('Inbox')
        # filter the email list for any UNSEEN emails
        result_uids = search('UNSEEN', None, imap)
        uids_list = result_uids[0].split()
        imap_close(imap)
        return len(uids_list)

    # TODO: Create methods to return other pieces of email besides just body as above
    #       or to return multiple emails.


def imap_connect_and_login(imap_host, email_address, password):
    """Function to make SSL connection to IMP host and login with the given credentials
    Parameters:
    - imap_host: host imap email server
    - email_address: IMAP enabled email address
    - password: password for the IMAP enabled email address
    Returns IMAP connected object
    """
    imap = imaplib.IMAP4_SSL(imap_host)
    imap.login(email_address, password)
    return imap


def imap_close(imap):
    """Function that closes the current email mailbox and logs out of the email account
    Parameters:
    - imap: IMAP connected object
    """
    imap.close()
    imap.logout()


def search(key, value, imap):
    """Function to search through emails for a given key value pair and return a
    filtered email list.
    EX: result_uids = search('FROM', 'openscienceframework-noreply@osf.io', con)
        Parameters:
        - key: key used to filter list of retirieved emails - used as part of key value
            pair - see value below
            (ex: 'FROM', 'CC', 'SUBJECT', etc)
        - value: value used to filter list of retrieved emails - used as part of key
            value pair - see key above
            (ex: 'openscienceframework-noreply@osf.io' when used with 'FROM' key)
        - imap: imap object that has already been logged into email account
        Returns collection of unique identifiers (uids) for emails that match search
           criteria
    """
    if value is None:
        # If no value is passed in then just search with the key - for use with
        # special search parameters like UNSEEN or FLAGGED
        response, uids = imap.search(None, key)
    else:
        response, uids = imap.search(None, key, '"{}"'.format(value))
    return uids
