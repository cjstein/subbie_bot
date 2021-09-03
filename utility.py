import re
import config
import inspect
import commands
import insult
import json

COMMAND_PATTERN = r'!{1}(?P<command>[\w]+)'
USER_PATTERN = r'@{1}(?P<user>[\w]+)'


def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sock.send(("PRIVMSG {} :{}\r\n".format(config.CHAN, msg)).encode("UTF-8"))


def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user))


def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs))


def find_commands(message: str) -> list:
    """
    This functions takes the message and returns a list of found commands
    Args:
        message: string; message in twitch chat

    Returns: list of commands, does not include the "!"
    """
    p = re.compile(COMMAND_PATTERN)
    m = p.findall(message)
    return list(m)


def find_users(message: str) -> list:
    """
    This functions takes the message and returns a list of found users
    Args:
        message: string; message in twitch chat

    Returns: list of users, does not include the "@"
    """
    p = re.compile(USER_PATTERN)
    m = p.findall(message)
    return list(m)


def is_mod_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod):
    return [func.__name__ for func in mod.__dict__.values() if is_mod_function(mod, func)]


def get_commands():
    return list_functions(commands)


def get_vibe_stats():
    with open(config.VIBE_JSON, 'r') as f:
        vibing_stats = json.load(f)
    return vibing_stats


def vibing_stats_collection(message, *args, **kwargs):
    vibing_stats = get_vibe_stats()
    chatter = message.split(" is")[0].strip().lower()
    percent = int(message.split("at ")[1].strip()[:-1])
    if percent < 51:
        reply = "Because you're vibin' so low, you get an insult: {}".format(insult.get_insult())
        chat(kwargs['sock'], reply)
    if chatter not in vibing_stats.keys():
        vibing_stats[chatter] = {
            'vibe_values': [percent],
        }
    else:
        vibing_stats[chatter]['vibe_values'].append(percent)
    with open(config.VIBE_JSON, 'w') as f:
        json.dump(vibing_stats, f)
