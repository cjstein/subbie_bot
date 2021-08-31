"""
This file can be used to add commands.  To create a new command, add it exactly as wanted in the chat then
have it take care of everything including sending another chat.

"""
import insult
import utility


def addinsult(insult_to_add, *args, **kwargs):
    insult.add_insult(insult_to_add)
    utility.chat(kwargs['sock'], "Insult added!")
