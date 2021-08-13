# subbie_bot
This is my twitch bot code.  I followed along from the tutorial site [pimylifeup](https://pimylifeup.com/raspberry-pi-twitch-bot/).

### Installation
Create a virtual environment.  Follow my blog post [here](https://www.subzeb.com/blog/creating-virtual-environment/) to do that.

Then install the necessary packages:
```pip install requirements.txt```

Create a copy of the `config_example.py` file but rename it `config.py`.
This will need the twitch account name, the oauth token, the channel it is used for, and the location of the insult file

You will need to create a twitch account for your bot, then go to the applications page to get your oauth token and place that in the `config.py` file.

For an insult command: You will also need to create an `insults.txt` file with an insult on each line.  I used [this generator](https://evilinsult.com/api/) and it's api to create a long list.

### Usage
Once everything is setup and running, users in the twitch chat can use the current commands:


* `!insult`  his picks a random line from the `insults.txt` file
* `!addinsult` This adds a new insult to the `insults.txt` file
