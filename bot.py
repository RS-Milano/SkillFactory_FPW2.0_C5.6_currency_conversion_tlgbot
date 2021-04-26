"""Importing third-party libraries"""
import telebot

"""Importing standard library modules"""
import json

"""Importing extensions"""
from my_config import TOKEN, URL, PRECISE
from my_extensions import Exchange_Rates, input_validation
from my_exceptions import *

"""Read the instruction from the file"""
instruction = ""
with open("instruction.txt", encoding = "UTF-8") as f:
    for line in f.readlines():
        instruction += line

"""Read the currencies dictionary"""
currencies_dict = {}
with open("currencies.txt", encoding = "UTF-8") as f:
    service_str = ""
    for line in f.readlines():
        service_str += line
    currencies_dict = json.loads(service_str)

"""Creat currencies prompt"""
currencies_prompt = ""
for key, value in currencies_dict.items():
    currencies_prompt += f"{key} - {value}\n"

"""Bot initialize"""
bot = telebot.TeleBot(TOKEN)

"""Command handlers"""
@bot.message_handler(commands=["start", "help"])
def start_handler(message):
    bot.reply_to(message, f"Hi, {message.chat.username}!\n{instruction}")

@bot.message_handler(commands=["values"])
def start_handler(message):
    bot.reply_to(message, str(currencies_prompt))

"""Message handlers"""
@bot.message_handler(content_types=["text"])
def text_handler(message):
    rates = Exchange_Rates(URL)
    message.text = message.text.upper()
    try:
        input_validation(message.text)
    except ConvertingCurrencyBotException as exc:
        bot.reply_to(message, exc)
    else:
        inquiry = message.text.split()
        if inquiry[0] == "RUB":
            result = round(rates.rates[inquiry[1]]["Nominal"] / rates.rates[inquiry[1]]["Rate"] * int(inquiry[2]), PRECISE)
            bot.reply_to(message, f"{inquiry[2]} {inquiry[0]} = {result} {inquiry[1]}")
        elif inquiry[1] == "RUB":
            result = round(rates.rates[inquiry[0]]["Rate"] / rates.rates[inquiry[0]]["Nominal"] * int(inquiry[2]), PRECISE)
            bot.reply_to(message, f"{inquiry[2]} {inquiry[0]} = {result} {inquiry[1]}")
        else:
            result = round(int(inquiry[2]) * ((rates.rates[inquiry[0]]["Rate"] / rates.rates[inquiry[0]]["Nominal"]) / (rates.rates[inquiry[1]]["Rate"] / rates.rates[inquiry[1]]["Nominal"])), PRECISE)
            bot.reply_to(message, f"{inquiry[2]} {inquiry[0]} = {result} {inquiry[1]}")

@bot.message_handler(content_types=["animation", "audio", "document", "photo", "sticker", "video", "voice", "contact", "dice"])
def text_handler(message):
    bot.reply_to(message, "I don't understend this")

bot.polling(none_stop=True)
