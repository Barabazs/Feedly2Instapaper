from distutils.command.config import config
import sys
from pathlib import Path

import instapaper
from archivooor.archiver import Archiver
from dotenv import dotenv_values
from feedly.api_client.session import FeedlySession
from feedly.api_client.stream import StreamOptions


def add_to_instapaper(config: dict, entry_list: list, archive: bool = False) -> list:
    """
    Adds all entries in entry_list as a bookmark in Instapaper.
    :param config: Dictionary containing credentials
    :param entry_list: list of Feedly entries
    :return: True if successful or a list of failed entries
    """
    instapaper_session = instapaper.Instapaper(
        config.get("instapaper-token"), config.get("instapaper-token_secret")
    )
    instapaper_session.login(
        config.get("instapaper-username"), config.get("instapaper-password")
    )
    failed_entries = []
    for entry in entry_list:
        entry_url = entry.json.get("alternate")[0].get("href")
        if archive:
            try:
                archive_page(config=config, url=entry_url)
            except Exception as e:
                print(e)

        bookmark = instapaper.Bookmark(instapaper_session, {"url": entry_url})
        response = bookmark.save()
        if response.decode("utf-8").find("bookmark_id") < 0:
            failed_entries.append(entry)
    if len(failed_entries) == 0:
        return True
    return failed_entries


def mark_as_read(feedly_session, entry_list):
    """
    Marks all entries in entry_list as read in Feedly.
    :param feedly_session_: properly authenticated Feedly session.
    :param entry_list: list of Feedly entries
    :return: True if successful or a response containing more information
    """
    response = feedly_session.do_api_request(
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


def mark_as_unsaved(feedly_session, entry_list):
    """
    Marks all entries in entry_list as unsaved in Feedly.
    :param feedly_session_: properly authenticated Feedly session.
    :param entry_list: list of Feedly entries
    :return: True if successful or a response containing more information
    """
    response = feedly_session.do_api_request(
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


def archive_page(config: dict, url: str) -> None:
    """Saves a page to the wayback machine

    :param config: Dictionary containing credentials
    :param url: URL to save
    """
    archive = Archiver(
        s3_access_key=config.get("s3_access_key"),
        s3_secret_key=config.get("s3_secret_key"),
    )

    archive.save_page(
        url=url,
        capture_all=True,
        capture_outlinks=True,
        capture_screenshot=True,
        force_get=True,
        skip_first_archive=True,
        outlinks_availability=False,
        email_result=False,
    )


def main(env_file: str = ".env", archive: bool = False) -> None:
    config = dotenv_values(env_file)

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
            instapaper_response = add_to_instapaper(
                config=config,
                entry_list=entries,
                archive=archive,
            )
            if instapaper_response:
                mark_as_read(feedly_session=feedly_session, entry_list=entries)
                mark_as_unsaved(feedly_session=feedly_session, entry_list=entries)
            else:
                for _entry in instapaper_response:
                    entries.remove(_entry)
                mark_as_read(feedly_session=feedly_session, entry_list=entries)
                mark_as_unsaved(feedly_session=feedly_session, entry_list=entries)
