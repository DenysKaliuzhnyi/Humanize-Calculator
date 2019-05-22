from flask import Flask
from flask import request
from flask_sslify import SSLify
import telebot
import time

from HumanizeCalculator import humanize_equation

TOKEN = '<TOKEN>'
bot = telebot.TeleBot(TOKEN, threaded=False)
MSGLIMIT = 4096

app = Flask(__name__)
sslify = SSLify(app)


bot.remove_webhook()
time.sleep(1)
bot.set_webhook(f'https://deniskakoderpro777.pythonanywhere.com/{TOKEN}')


@bot.message_handler(commands = ['start', 'help'])
def handle_start(message):
    msg = "hey, send me some math equation. Possible symbols are +-*/= and digits."\
        "White symbols will be ignored. Example of your message 1+2/4*100=0"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types = ['text'])
def handle_text(message):
    try:
        msg = humanize_equation(message.text)
        while len(msg) != 0:
            bot.reply_to(message, msg[:MSGLIMIT])
            msg = msg[MSGLIMIT:]
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, "ApiException!")


@app.route('/', methods=["GET"])
def GET():
    return "<h1>I'm working :)</h1>"


@app.route(f'/{TOKEN}', methods=["POST"])
def POST():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200


if __name__ == '__main__':
    app.run()
