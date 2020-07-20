import sys

import instapaper
import yaml
from feedly.api_client.session import FeedlySession
from feedly.api_client.stream import StreamOptions

feedly = __import__('feedly')

with open('example_settings.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def add_to_instapaper(instapaper_session_, entry_list):
    failed_entries = []
    for entry in entry_list:
        entry_url = (entry.json['originId'])
        bookmark = instapaper.Bookmark(instapaper_session_, {"url": entry_url})
        response = bookmark.save()
        if response.decode("utf-8").find("bookmark_id") < 0:
            failed_entries.append(entry)
    if len(failed_entries) == 0:
        return True
    return failed_entries


def mark_as_read(feedly_session_, entry_list):
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
            instapaper_session = instapaper.Instapaper(
                config['production']['instapaper']['token'],
                config['production']['instapaper']['token_secret'])
            instapaper_session.login(
                config['production']['instapaper']['username'],
                config['production']['instapaper']['password'])
            instapaper_response = add_to_instapaper(instapaper_session, entries)
            if instapaper_response:
                mark_as_read(feedly_session, entries)
                mark_as_unsaved(feedly_session, entries)
            else:
                for _entry in instapaper_response:
                    entries.remove(_entry)
                mark_as_read(feedly_session, entries)
                mark_as_unsaved(feedly_session, entries)
