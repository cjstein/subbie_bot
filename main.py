#!/home/SubZeb/.virtualenvs/twitchbot/bin/python3
import config
import utility
import socket
import time
import re
import commands

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

try:
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
    connected = True  # Socket successfully connected
    print("Connected...")
except Exception as e:
    print(str(e))
    connected = False  # Socket failed to connect


def bot_loop():  # sourcery no-metrics
    while connected:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("Pong")
        else:
            sender = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            sender = sender.lower().strip()
            for pattern in config.BAN_PAT:
                if re.match(pattern, message):
                    utility.ban(s, sender)
                    break
            commands_to_execute = utility.find_commands(message)
            users_to_reference = utility.find_users(message)
            stripped_message = str(message)
            for i in commands_to_execute:
                stripped_message = stripped_message.replace(f'!{i}', '')
            for i in users_to_reference:
                stripped_message = stripped_message.replace(f'@{i}', '')
            # Get the list of commands
            commands_allowed = utility.get_commands()
            for command in commands_to_execute:
                if command in commands_allowed:
                    getattr(commands, command)(
                        stripped_message,
                        sock=s,
                        users=users_to_reference,
                        sender=sender,
                    )
            if "vibing at" in message.strip() and sender == "streamlabs":
                utility.vibing_stats_collection(
                    message,
                    sock=s,
                )
    time.sleep(1 / config.RATE)


if __name__ == "__main__":
    bot_loop()
