import sys
from pathlib import Path

import instapaper
import yaml
from feedly.api_client.session import FeedlySession
from feedly.api_client.stream import StreamOptions

path = Path(__file__).parent / './settings.yaml'
with path.open() as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def add_to_instapaper(instapaper_session_, entry_list):
    """
    Adds all entries in entry_list as a bookmark in Instapaper.
    :param instapaper_session_: properly authenticated in Instapaper session
    :param entry_list: list of Feedly entries
    :return: True if successful or a list of failed entries
    """
    failed_entries = []
    for entry in entry_list:
        entry_url = (entry.json['alternate'][0]['href'])
        bookmark = instapaper.Bookmark(instapaper_session_, {"url": entry_url})
        response = bookmark.save()
        if response.decode("utf-8").find("bookmark_id") < 0:
            failed_entries.append(entry)
    if len(failed_entries) == 0:
        return True
    return failed_entries


def mark_as_read(feedly_session_, entry_list):
    """
    Marks all entries in entry_list as read in Feedly.
    :param feedly_session_: properly authenticated Feedly session.
    :param entry_list: list of Feedly entries
    :return: True if successful or a response containing more information
    """
    response = feedly_session_.do_api_request(relative_url='/v3/markers/',
                                              method='post',
                                              data={'action': 'markAsRead',
                                                    'type': 'entries',
                                                    'entryIds': [
                                                        entry_id.json['id'] for
                                                        entry_id in
                                                        entry_list]})
    if response is None:
        return True
    return response


def mark_as_unsaved(feedly_session_, entry_list):
    """
    Marks all entries in entry_list as unsaved in Feedly.
    :param feedly_session_: properly authenticated Feedly session.
    :param entry_list: list of Feedly entries
    :return: True if successful or a response containing more information
    """
    response = feedly_session_.do_api_request(relative_url='/v3/markers/',
                                              method='post',
                                              data={'action': 'markAsUnsaved',
                                                    'type': 'entries',
                                                    'entryIds': [
                                                        entry_id.json['id'] for
                                                        entry_id in
                                                        entry_list]})
    if response is None:
        return True
    return response


def establish_instapaper_session():
    """
    Establishes an authenticated session with an Instapaper account.
    :return: properly authenticated Instapaper session
    """
    instapaper_session_ = instapaper.Instapaper(
        config['production']['instapaper']['token'],
        config['production']['instapaper']['token_secret'])
    instapaper_session_.login(
        config['production']['instapaper']['username'],
        config['production']['instapaper']['password'])

    return instapaper_session_


with FeedlySession(
        auth=config['production']['feedly']['access_token'],
        user_id=config['production']['feedly']['client_id'],
        api_host=config['production']['feedly']['url']) as feedly_session:
    feeds = feedly_session.user.get_tags()
    keep = []
    for feed in feeds:
        if feeds[feed].json['id'].find('global.saved') >= 0:
            keep = feeds[feed]
        category_id = keep.stream_id.content_id
        entries = feedly_session.user.get_tag(category_id).stream_contents(
            options=StreamOptions(max_count=sys.maxsize))
        entries = list(entries)
        if len(entries) > 0:
            instapaper_session = establish_instapaper_session()
            instapaper_response = add_to_instapaper(instapaper_session, entries)
            if instapaper_response:
                mark_as_read(feedly_session, entries)
                mark_as_unsaved(feedly_session, entries)
            else:
                for _entry in instapaper_response:
                    entries.remove(_entry)
                mark_as_read(feedly_session, entries)
                mark_as_unsaved(feedly_session, entries)
