"""
This file can be used to add commands.  To create a new command, add it exactly as wanted in the chat then
have it take care of everything including sending another chat.

"""
import insult
import utility


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
        print(f'{k}: {v}')

    for user in kwargs['users']:
        print(f'@{user} has been tested')


def vibe(*args, **kwargs):
    if kwargs['sender'] == 'subzeb':
        utility.chat(kwargs['sock'], 'Subbie is always vibing at 100%')


def vibestats(*args, **kwargs):
    vibing_stats = utility.get_vibe_stats()
    try:
        chatter = vibing_stats[kwargs['sender']]
        num_vibes = len(chatter['vibe_values'])
        highest = max(chatter['vibe_values'])
        lowest = min(chatter['vibe_values'])
        avg = sum(chatter['vibe_values']) / num_vibes
        reply = '{} - Number of vibes: {} - Highest: {} - Lowest: {} - Average: {}'.format(username, num_vibes, highest, lowest, round(avg, 2))
        utility.chat(kwargs['sock'], reply)
    except KeyError:
        utility.chat(kwargs['sock'], 'You need to vibe first')
