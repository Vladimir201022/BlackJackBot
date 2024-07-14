import telebot
import requests

API_TOKEN = '7491444367:AAGEWx9k9orlP2MOExxgmVsVGtP1hEXfBvw'
bot = telebot.TeleBot(API_TOKEN)

DECK_API_URL = 'https://deckofcardsapi.com/api/deck'


def create_deck():
    response = requests.get(f'{DECK_API_URL}/new/shuffle/?deck_count=1')
    deck = response.json()
    return deck['deck_id']


def draw_card(deck_id, count=1):
    response = requests.get(f'{DECK_API_URL}/{deck_id}/draw/?count={count}')
    cards = response.json()
    return cards['cards']


def calculate_score(hand):
    score = 0
    aces = 0
    values = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 10,
        'Q': 10,
        'K': 10,
        'ACE': 11
    }

    for card in hand:
        score += values[card['value']]
        if card['value'] == 'ACE':
            aces += 1

    while score > 21 and aces:
        score -= 10
        aces -= 1

    return score


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Добро пожаловать в игру блэкджек! Напишите /play чтобы начать.")


@bot.message_handler(commands=['play'])
def play_game(message):
    deck_id = create_deck()

