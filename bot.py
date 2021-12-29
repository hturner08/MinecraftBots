import time 
import random
import argparse

from javascript import require, On, Once, AsyncTask, once, off
from unscramble import unscramble

HOST = 'play.manacube.com'
USERNAME = 'herbieturner@outlook.com'
mineflayer = require('mineflayer')
mineflayerViewer = require('prismarine-viewer')
parser = argparse.ArgumentParser(description='Mineflayer bot')
parser.add_argument('--host', default=HOST, help='server hostname')
parser.add_argument('--port', type=int, default=25565, help='server port')
parser.add_argument('--username', default=USERNAME, help='username')
parser.add_argument('--password', default=None, help='password')
parser.add_argument('--version', default = '1.8', help='minecraft version')

player_count = 1

if __name__ == '__main__':
    args = parser.parse_args()
    bot = mineflayer.createBot(
    {'auth': 'microsoft', 'host': HOST, 'username': USERNAME, 'version': '1.8', 'hideErrors': False})
    print('Bot created')
    once(bot, 'login')
    print('Logged in')


@Once(bot, 'spawn')
def setup(*args):
    # mineflayerViewer(bot, {'port': 3007, 'firstPerson': True})
    bot.chat('/factions')  # Move from hub to faction server
    time.sleep(10)  # Wait for server to load
    # You must move before you can type on server
    bot.setControlState('forward', True)
    time.sleep(1)
    bot.clearControlStates()
    # bot.addChatPattern('game_starts', "/^Game! First to .* wins$/")

@On(bot, 'resourcePack')
def acceptPack(url, hash):
    bot.acceptResourcePack()


@On(bot, 'messagestr')
def onChat(this, message, messagePosition, jsonMsg,*rest):
    # try:
    #     print(matches)
    # except Exception as e:
    #     pass
    # Check if message is from plugin
    print(f"{message}")
    if "First to" in message:
        words = message.split()
        answer = ''
        for word in get_words(words[4:]):
            answer += word + ' '
        # Unscramble answer if necessary
        if words[3] == 'unscramble':
            answer = unscramble(answer)[0]
        if answer is not None:
            if player_count == 1 or random.random() < 1:
                time.sleep(1.5)
                bot.chat(answer)
        print(answer)
        bot.setControlState('back', True)
        time.sleep(.1)
        bot.clearControlStates()

@On(bot, 'playerJoined')
def onPlayerJoined(*args):
    global player_count
    player_count += 1

@On(bot, 'playerLeft')
def onPlayerLeft(*args):
    global player_count
    player_count = max(1, player_count-1)

@On(bot, 'logout')
def relog(*args):
    once(bot, 'login')
    bot.chat('/factions')  # Move from hub to faction server
    time.sleep(10)  # Wait for server to load
    # You must move before you can type on server
    bot.setControlState('forward', True)
    time.sleep(1)
    bot.clearControlStates()


def get_words(word_list):
    for word in word_list:
        if word == 'wins':
            break
        yield word
