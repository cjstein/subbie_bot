import requests
import random
import time
import config

file = config.INSULT_FILE


def check_insult_duplicate(insult: str):
    with open(file, 'r') as f:
        insults = f.readlines()
    insults = [i.strip().lower() for i in insults]
    return insult.strip().lower() in insults


def get_insult_from_api():
    # This would get the insult from the insult generator
    url = 'https://evilinsult.com/generate_insult.php?lang=en&type=text'
    r = requests.get(url)
    return r.text


def get_insult():
    # This funxction gets a random insult from the compiled insults from the generator
    with open(file, 'r') as f:
        insults = f.readlines()
    return random.choice(insults)


def add_insult(insult):
    # This function takes the insult and adds it to the list
    if not check_insult_duplicate(insult):
        with open(file, 'a') as f:
            f.write(insult.strip())
            f.write('\n')
