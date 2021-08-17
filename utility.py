import re
import config

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
