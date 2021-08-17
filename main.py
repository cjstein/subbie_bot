#!/home/SubZeb/.virtualenvs/twitchbot/bin/python3
import config
import utility
import socket
import time
import re
import insult
import json

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
    with open(config.VIBE_JSON, 'r') as f:
        vibing_stats = json.load(f)
    while connected:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("Pong")
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(response)
            print(username)
            print(message, "\n")
            for pattern in config.BAN_PAT:
                if re.match(pattern, message):
                    utility.ban(s, username)
                    break
            if message.strip().lower() == "!vibe" and username.lower() == "subzeb":
                utility.chat(s, "Subbie is always vibing at 100%")
            # if message.strip().lower() == "!insult":
            #    chat_out = insult.get_insult()
            #    print(chat_out)
            #    utility.chat(s, chat_out)
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
                chatter = message.split(" is")[0].strip().lower()
                percent = int(message.split("at ")[1].strip()[:-1])
                reply = "Because you're vibin so low, you get an insult: {}".format(insult.get_insult())
                if percent < 51:
                    utility.chat(s, reply)
                if chatter not in vibing_stats.keys():
                    vibing_stats[chatter] = {
                        'vibe_values': [percent],
                        }
                else:
                    vibing_stats[chatter]['vibe_values'].append(percent)
                with open(config.VIBE_JSON, 'w') as f:
                    json.dump(vibing_stats, f)
            if message.strip().lower().startswith("!vibestats"):
                print(vibing_stats)
                try:
                    print(username)
                    chatter = vibing_stats[username.lower().strip()]
                    print('Chatter: {}'.format(chatter))
                    print(chatter['vibe_values'])
                    num_vibes = len(chatter['vibe_values'])
                    print(num_vibes)
                    highest = max(chatter['vibe_values'])
                    print(highest)
                    lowest = min(chatter['vibe_values'])
                    print(lowest)
                    avg = sum(chatter['vibe_values']) / num_vibes
                    print(avg)
                    reply = '{} - Number of vibes: {} - Highest: {} - Lowest: {} - Average: {}'.format(username, num_vibes, highest, lowest, round(avg, 2))
                    print(reply)
                    utility.chat(s, reply)
                except KeyError:
                    utility.chat(s,'You need to vibe first')
    time.sleep(1 / config.RATE)


if __name__ == "__main__":
    bot_loop()
