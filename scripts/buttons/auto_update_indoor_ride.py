#  -*- encoding: utf-8 -*-

from collections import defaultdict

import ujson
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from common.constants_and_variables import BotConstants
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class AutoUpdateIndoorRide:

    def __init__(self, bot, update, user_data, chosen_option):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_constants = BotConstants()
        self.query = self.update.callback_query
        self.chosen_option = chosen_option
        self.chat_id = self.query.message.chat_id
        self.message_id = self.query.message.message_id
        self.strava_telegram_webhooks_resource = StravaTelegramWebhooksResource()

    def auto_update_indoor_ride_disable(self):
        self.strava_telegram_webhooks_resource.disable_auto_update_indoor_ride(
            athlete_id=self.user_data['auto_update_indoor_ride']['athlete_id'])
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_UPDATE_INDOOR_RIDE_DISABLED
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.strava_telegram_webhooks_resource.send_message(message)

    def auto_update_indoor_ride_ignore(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_UPDATE_INDOOR_RIDE_DISABLE_CANCEL
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.strava_telegram_webhooks_resource.send_message(message)

    def auto_update_indoor_ride_name_indoor_ride(self):
        self.user_data['auto_update_indoor_ride'].update({'name': 'Indoor Ride'})
        self.get_bikes()

    def auto_update_indoor_ride_name_indoor_cycling(self):
        self.user_data['auto_update_indoor_ride'].update({'name': 'Indoor Cycling'})
        self.get_bikes()

    def auto_update_indoor_ride_name_automatic(self):
        self.user_data['auto_update_indoor_ride'].update({'name': 'Automatic'})
        self.get_bikes()

    def auto_update_indoor_ride_name_skip(self):
        self.user_data['auto_update_indoor_ride'].update({'name': None})
        self.get_bikes()

    def get_bikes(self):
        bikes = self.strava_telegram_webhooks_resource.get_bikes_list(
            self.user_data['auto_update_indoor_ride']['athlete_token'])
        if len(bikes) > 0:
            bikes_list = []
            for sl_no in bikes:
                bikes_list += [InlineKeyboardButton(text=sl_no,
                                                    callback_data="auto_update_indoor_ride_gear_id_{gear_id}".format(
                                                        gear_id=bikes[sl_no]['bike_id']))]
            keyboard_bikes = InlineKeyboardMarkup(inline_keyboard=[bikes_list])
            list_bikes = ""
            for sl_no in bikes:
                list_bikes += "{sl_no}. {bike_name}\n".format(sl_no=sl_no, bike_name=bikes[sl_no]['bike_name'])
            self.user_data['auto_update_indoor_ride'].update({'gear_id': bikes})
            self.bot.send_message(text=list_bikes, chat_id=self.chat_id)
            self.strava_telegram_webhooks_resource.send_message(list_bikes)
            message = self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CHOOSE_BIKE
            self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                       reply_markup=keyboard_bikes)
        else:
            self.user_data['auto_update_indoor_ride'].update({'gear_id': None})
            self.auto_update_indoor_ride_setup_confirmation()

    def auto_update_indoor_ride_setup_confirmation(self):
        found = True
        if not self.user_data['auto_update_indoor_ride']['name']:
            if not self.user_data['auto_update_indoor_ride']['gear_id']:
                found = False
        self.bot.deleteMessage(self.chat_id, self.message_id)
        if found:
            configured_data = ""
            if self.user_data['auto_update_indoor_ride']['name']:
                configured_data += "Activity Name: {activity_name}\n".format(
                    activity_name=self.user_data['auto_update_indoor_ride']['name'])
            if self.user_data['auto_update_indoor_ride']['gear_id']:
                bike_name = self.strava_telegram_webhooks_resource.get_gear_name(
                    self.user_data['auto_update_indoor_ride']['athlete_token'],
                    self.user_data['auto_update_indoor_ride']['gear_id'])
                configured_data += "Bike: {bike_name}".format(bike_name=bike_name)
            message = self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CONFIRMATION.format(
                configuration=configured_data)
            self.bot.send_message(text=message, chat_id=self.chat_id,
                                  reply_markup=self.bot_constants.KEYBOARD_AUTO_UPDATE_INDOOR_RIDE_CONFIRMATION)
            self.strava_telegram_webhooks_resource.send_message(message)
        else:
            self.user_data.clear()
            message = self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_INSUFFICIENT_INFORMATION
            self.bot.send_message(text=message, chat_id=self.chat_id)
            self.strava_telegram_webhooks_resource.send_message(message)

    def auto_update_indoor_ride_update_confirm_yes(self):
        update_indoor_ride_data = dict()
        if 'name' in self.user_data['auto_update_indoor_ride']:
            update_indoor_ride_data.update({'name': self.user_data['auto_update_indoor_ride']['name']})
        if 'gear_id' in self.user_data['auto_update_indoor_ride']:
            update_indoor_ride_data.update({'gear_id': self.user_data['auto_update_indoor_ride']['gear_id']})

        self.strava_telegram_webhooks_resource.database_write(self.bot_constants.QUERY_UPDATE_INDOOR_RIDE_ENABLE.format(
            update_indoor_ride_data=ujson.dumps(update_indoor_ride_data),
            chat_id=self.chat_id,
            athlete_id=self.user_data['auto_update_indoor_ride']['athlete_id']))

        self.user_data.clear()
        message = self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_ENABLED
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.strava_telegram_webhooks_resource.send_message(message)

    def auto_update_indoor_ride_confirm_no(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_AUTO_UPDATE_INDOOR_RIDE_CANCELLED
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.strava_telegram_webhooks_resource.send_message(message)

    def exit_button(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_EXIT_BUTTON
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.strava_telegram_webhooks_resource.send_message(message)

    def process(self):
        if 'auto_update_indoor_ride_gear_id_' in self.chosen_option:
            gear_id = self.chosen_option.split("auto_update_indoor_ride_gear_id_")[1]
            self.user_data['auto_update_indoor_ride']['gear_id'] = gear_id
            self.chosen_option = "auto_update_indoor_ride_setup_confirmation"

        options = defaultdict(lambda: self.exit_button, {
            'auto_update_indoor_ride_disable': self.auto_update_indoor_ride_disable,
            'auto_update_indoor_ride_ignore': self.auto_update_indoor_ride_ignore,
            'auto_update_indoor_ride_name_indoor_ride': self.auto_update_indoor_ride_name_indoor_ride,
            'auto_update_indoor_ride_name_indoor_cycling': self.auto_update_indoor_ride_name_indoor_cycling,
            'auto_update_indoor_ride_name_automatic': self.auto_update_indoor_ride_name_automatic,
            'auto_update_indoor_ride_name_skip': self.auto_update_indoor_ride_name_skip,
            'auto_update_indoor_ride_setup_confirmation': self.auto_update_indoor_ride_setup_confirmation,
            'auto_update_indoor_ride_update_confirm_yes': self.auto_update_indoor_ride_update_confirm_yes,
            'auto_update_indoor_ride_confirm_no': self.auto_update_indoor_ride_confirm_no
        })

        options[self.chosen_option]()
