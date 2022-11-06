import sys
from pathlib import Path

import instapaper
from dotenv import dotenv_values
from feedly.api_client.session import FeedlySession
from feedly.api_client.stream import StreamOptions

config = dotenv_values(".env")


def add_to_instapaper(instapaper_session_, entry_list):
    """
    Adds all entries in entry_list as a bookmark in Instapaper.
    :param instapaper_session_: properly authenticated in Instapaper session
    :param entry_list: list of Feedly entries
    :return: True if successful or a list of failed entries
    """
    failed_entries = []
    for entry in entry_list:
        entry_url = entry.json.get("alternate")[0].get("href")
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
    response = feedly_session_.do_api_request(
        relative_url="/v3/markers/",
        method="post",
        data={
            "action": "markAsRead",
            "type": "entries",
            "entryIds": [entry_id.json.get("id") for entry_id in entry_list],
        },
    )
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
    response = feedly_session_.do_api_request(
        relative_url="/v3/markers/",
        method="post",
        data={
            "action": "markAsUnsaved",
            "type": "entries",
            "entryIds": [entry_id.json.get("id") for entry_id in entry_list],
        },
    )
    if response is None:
        return True
    return response


def establish_instapaper_session() -> instapaper.Instapaper:
    """
    Establishes an authenticated session with an Instapaper account.
    :return: properly authenticated Instapaper session
    """
    instapaper_session_ = instapaper.Instapaper(
        config.get("instapaper-token"), config.get("instapaper-token_secret")
    )
    instapaper_session_.login(
        config.get("instapaper-username"), config.get("instapaper-password")
    )

    return instapaper_session_


with FeedlySession(
    auth=config.get("feedly-access_token"),
    user_id=config.get("feedly-client_id"),
    api_host=config.get("feedly-url"),
) as feedly_session:
    feedly_session.user.get_tag("global.saved")
    entries = feedly_session.user.get_tag("global.saved").stream_contents(
        options=StreamOptions(max_count=sys.maxsize)
    )
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
