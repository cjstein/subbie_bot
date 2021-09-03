"""
This file can be used to add commands.  To create a new command, add a function with a name exactly as wanted in the
chat then have it take care of everything including sending another chat.
The message that has all the commands and users removed is the first argument for each command
Here are the kwargs that are sent to every command:
sock : the socket used for chat.  How to send a chat reply use this: utility.chat(kwargs['sock'], reply)
users: a list of users that were found in the original message.
sender: this is who sent the original message

"""
import insult
import utility
import time
import config


def _command_template(stripped_message, *args, **kwargs):
    # This is a template function to create all commands, change the '_command_template'
    # to the command you want the bot to respond to in chat.
    users = kwargs['users']
    sender = kwargs['sender']
    # add logic, etc. here
    reply = 'make some message to respond with'
    utility.chat(kwargs['sock'], reply)

def addinsult(insult_to_add, *args, **kwargs):
    try:
        insult.add_insult(insult_to_add)
        utility.chat(kwargs['sock'], "Insult added!")
    except Exception as e:
        utility.chat(kwargs['sock'], 'Error adding insult!')
        print(e)


def test_command(message_to_print, *args, **kwargs):
    print(message_to_print)
    for k, v in kwargs.items():
        print('{}: {}'.format(k,v))

    for user in kwargs['users']:
        print('@{} has been tested'.format(user))


def vibe(*args, **kwargs):
    if kwargs['sender'] == 'subzeb':
        utility.chat(kwargs['sock'], 'Subbie is always vibing at 100%')


def vibestats(*args, **kwargs):
    vibing_stats = utility.get_vibe_stats()
    if not kwargs['users']:
        try:
            chatter = vibing_stats[kwargs['sender']]
            num_vibes = len(chatter['vibe_values'])
            highest = max(chatter['vibe_values'])
            lowest = min(chatter['vibe_values'])
            avg = sum(chatter['vibe_values']) / num_vibes
            reply = '{} - Number of vibes: {} - Highest: {} - Lowest: {} - Average: {}'.format(
                kwargs['sender'],
                num_vibes,
                highest,
                lowest,
                round(avg, 2),
            )
            utility.chat(kwargs['sock'], reply)
        except KeyError:
            utility.chat(kwargs['sock'], 'You need to vibe first')
    else:
        for user in kwargs['users']:
            try:
                chatter = vibing_stats[user.lower()]
                num_vibes = len(chatter['vibe_values'])
                highest = max(chatter['vibe_values'])
                lowest = min(chatter['vibe_values'])
                avg = sum(chatter['vibe_values']) / num_vibes
                reply = '{} - Number of vibes: {} - Highest: {} - Lowest: {} - Average: {}'.format(
                    user,
                    num_vibes,
                    highest,
                    lowest,
                    round(avg, 2),
                )
                utility.chat(kwargs['sock'], reply)
                time.sleep(1 / config.RATE)
            except KeyError:
                utility.chat(kwargs['sock'], '{} need to vibe first'.format(user))

def club100(*args, **kwargs):
