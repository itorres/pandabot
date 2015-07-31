# -*- coding: utf-8 -*-
import os

from flask import Flask, request
import requests

app = Flask(__name__)


class Message:
    def __init__(self, d):
        vars(self).update(d)
        self.chat = self.message['chat']['id']

        try:
            self.parse()
        except Exception as e:
            app.logger.error("Cannot parse:\n %s\n %s", self.message, e)

    def parse(self):
        self.text = self.message['text']
        if any([k in self.text for k, v in triggers.items()]):
            print("Por ahora bien")
            self.trigger()

        if self.text[0] == "/":
            self.command, self.args = self.text.split(None, 1)
            self.command = self.command[1:].lower()
            try:
                print("Trying", self.command)
                getattr(self, self.command)()
            except Exception as e:
                print("Exception on", self.command, e)
                sendMessage(self.chat,
                            "{0}: command not found".format(self.command))

    def trigger(self):
        print("Parsing trigger")
        for k, v in triggers.items():
            if k in self.text:
                sendMessage(self.chat, v.format(
                    username=self.message['from']['username']))

    def ctcp(self):
        answers = {'PANDA': "Da Panda Crew Rulez. Somos miembros, mieeeeeeeembros!, mapashito, quiere un purito? o/"}
        ctcp = self.args.upper()
        sendMessage(self.chat, answers[ctcp])


def sendMessage(chat_id, text):
    payload = {'chat_id': chat_id, 'text': text}
    result = telegram('sendMessage', payload)
    app.logger.debug("Answering:\n %s\n%s" % (payload, result.text))


def telegram(action, payload):
    print("telegramming: |{}| {}".format(token, action))
    url = "https://api.telegram.org/bot{}/{}".format(token, action)
    app.logger.debug("url: %s" % url)
    return requests.post(url, data=payload)


@app.route('/telegram', methods=['POST'])
def telegramWebHook():
    Message(request.json)
    return ""

if __name__ == "__main__":
    triggers = {
        "gamba": "MARIPURI!",
        "orujo": "{username}: por el culo te la estrujo",
        "fanta": "{username}: por el culo te la estrujo",
        "!deseo": "{username}: tu deseo ha sido concedido",
    }
    token = os.environ['TELEGRAM_TOKEN']
    client = requests.Session()
    app.run(debug=True, port=18060, host="0.0.0.0")
