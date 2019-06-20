# TCD Helper Bot

A (not so) simple Discord bot that helps programmers find what they are looking for.

Written for the [TCD Discord server](https://discord.gg/code).

## Usage
To use the bot, mention it with your command.

```@helper help```

In direct messages the mention is optional.

Use the `help` command to list available commands, or `_help` to list all commands, even hidden ones.

## Installation
This bot requires Python 3.6+, as well as the [`requests`](https://pypi.org/project/requests/), [`discord.py`](https://pypi.org/project/discord.py/), and [`hjson`](https://pypi.org/project/hjson/) modules.
```sh
# Install dependencies
$ python3 -m pip install -U requests
$ python3 -m pip install -U discord.py[voice]
$ python3 -m pip install -U hjson

# Clone repo
$ git clone https://github.com/max-kamps/helper.git

# Create the config file
$ cd helper
$ cp example.config.hjson config.hjson

# Make sure to add your token to the config file

# Running
$ cd ..
$ python3 -m helper main
```

## Running
```sh
$ python3 -m helper <account>
```
