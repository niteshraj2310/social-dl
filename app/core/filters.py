from urllib.parse import urlparse

from pyrogram import filters as _filters

from app import Config
from app.core.media_handler import url_map


def check_for_urls(text_list):
    for link in text_list:
        if match := url_map.get(urlparse(link).netloc):
            return True
        else:
            for key in url_map.keys():
                if key in link:
                    return True


def dynamic_chat_filter(_, __, message, cmd=False):
    if (
        not message.text
        or (not message.text.startswith("https") and not cmd)
        or message.chat.id not in Config.CHATS
        or (message.chat.id in Config.DISABLED_CHATS and not cmd)
        or message.forward_from_chat
    ):
        return False
    user = message.from_user
    if user and (user.id in Config.BLOCKED_USERS or user.is_bot):
        return False
    if cmd:
        return True
    url_check = check_for_urls(message.text.split())
    return bool(url_check)


def dynamic_allowed_list(_, __, message):
    if not dynamic_chat_filter(_, __, message, cmd=True):
        return False
    start_str = message.text.split(maxsplit=1)[0]
    cmd = start_str.replace("/", "", 1)
    cmd_check = cmd in {"download", "dl", "down"}
    reaction_check = not message.reactions
    return bool(cmd_check and reaction_check)


def dynamic_cmd_filter(_, __, message):
    if (
        not message.text
        or not message.text.startswith(Config.TRIGGER)
        or not message.from_user
        or message.from_user.id not in Config.USERS
    ):
        return False

    start_str = message.text.split(maxsplit=1)[0]
    cmd = start_str.replace(Config.TRIGGER, "", 1)
    cmd_check = cmd in Config.CMD_DICT
    reaction_check = not message.reactions
    return bool(cmd_check and reaction_check)


chat_filter = _filters.create(dynamic_chat_filter)
user_filter = _filters.create(dynamic_cmd_filter)
allowed_cmd_filter = _filters.create(dynamic_allowed_list)
