#!/home/SubZeb/.virtualenvs/twitchbot/bin/python3
import config
import utility
import socket
import time
import re
import insult

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


def bot_loop():
    while connected:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("Pong")
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(username)
            print(message, "\n")
            for pattern in config.BAN_PAT:
                if re.match(pattern, message):
                    utility.ban(s, username)
                    break
            if message.strip().lower() == "!vibe" and username.lower() == "subzeb":
                utility.chat(s, "Subbie is always vibing at 100%")
            if message.strip().lower() == "!insult":
                chat_out = insult.get_insult()
                print(chat_out)
                utility.chat(s, chat_out)
            if message.strip().lower().startswith("!addinsult"):
                try:
                    addition = message[11:]
                    insult.add_insult(addition)
                    utility.chat(s, 'Insult added')
                    print("Added insult: " + addition)
                except Exception as e:
                    utility.chat(s, 'There was an error adding the insult')
                    print(e)
            if "vibing at" in message.strip() and username.lower() == "streamlabs":
                percent = int(message.split("at ")[1].strip()[:-1])
                message = "Because you're vibin so low, you get an insult: {}".format(insult.get_insult())
                if percent < 51:
                    utility.chat(s, message)

    time.sleep(1 / config.RATE)


if __name__ == "__main__":
    bot_loop()
