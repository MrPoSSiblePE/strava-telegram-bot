#  -*- encoding: utf-8 -*-

import logging
import traceback

import requests

from common.constants_and_variables import BotConstants, BotVariables


class ShadowMode(object):

    def __init__(self):
        self.bot_constants = BotConstants()
        self.bot_variables = BotVariables()
        self.api_send_message = self.bot_constants.API_TELEGRAM_SEND_MESSAGE.format(
            bot_token=self.bot_variables.telegram_bot_token)

    def send_message(self, message, parse_mode='Markdown', disable_web_page_preview=True, disable_notification=False,
                     reply_markup=None):
        try:
            if self.bot_variables.shadow_mode:
                data = {
                    'chat_id': '{chat_id}'.format(chat_id=self.bot_variables.shadow_mode_chat_id),
                    'text': '{message}'.format(message=message),
                    'parse_mode': parse_mode,
                    'disable_web_page_preview': disable_web_page_preview,
                    'disable_notification': disable_notification,
                    'reply_markup': reply_markup
                }
                requests.post(self.api_send_message, data=data)
        except Exception:
            logging.error("Something went wrong. Exception: {exception}".format(exception=traceback.format_exc()))