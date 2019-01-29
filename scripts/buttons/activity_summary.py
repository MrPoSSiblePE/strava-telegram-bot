#  -*- encoding: utf-8 -*-

from collections import defaultdict

from clients.database import DatabaseClient
from common.constants_and_variables import BotConstants
from common.shadow_mode import ShadowMode


class ActivitySummary(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_constants = BotConstants()
        self.query = self.update.callback_query
        self.chosen_option = self.query.data
        self.chat_id = self.query.message.chat_id
        self.message_id = self.query.message.message_id
        self.telegram_username = self.query.message.chat.username
        self.shadow_mode = ShadowMode(bot)
        self.database_client = DatabaseClient()

    def activity_summary_enable_button(self):
        self.database_client.write_operation(self.bot_constants.QUERY_ACTIVITY_SUMMARY_ENABLE.format(
            chat_id=self.chat_id,
            athlete_id=self.user_data['ride_summary']['athlete_id']))
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_ACTIVITY_SUMMARY_ENABLED
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.shadow_mode.send_message(message=message)

    def activity_summary_disable_button(self):
        self.database_client.write_operation(self.bot_constants.QUERY_ACTIVITY_SUMMARY_DISABLE.format(
            athlete_id=self.user_data['ride_summary']['athlete_id']))
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_ACTIVITY_SUMMARY_DISABLED
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.shadow_mode.send_message(message=message)

    def activity_summary_ignore_button(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_ACTIVITY_SUMMARY_IGNORE
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.shadow_mode.send_message(message=message)

    def activity_summary_disable_ignore_button(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_ACTIVITY_SUMMARY_DISABLE_IGNORE
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.shadow_mode.send_message(message=message)

    def exit_button(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_EXIT_BUTTON
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.shadow_mode.send_message(message=message)
        self.shadow_mode.send_message(message=message)

    def process(self):
        options = defaultdict(lambda: self.exit_button, {
            'activity_summary_enable': self.activity_summary_enable_button,
            'activity_summary_ignore': self.activity_summary_ignore_button,
            'activity_summary_disable': self.activity_summary_disable_button,
            'activity_summary_disable_ignore': self.activity_summary_disable_ignore_button
        })

        options[self.chosen_option]()