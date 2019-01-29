#  -*- encoding: utf-8 -*-

from buttons.activity_summary import ActivitySummary
from buttons.auto_update_indoor_ride import AutoUpdateIndoorRide
from buttons.stats import Stats


class HandleButtons(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.query = self.update.callback_query
        self.chosen_option = self.query.data

    def process(self):
        if self.chosen_option.startswith('stats'):
            stats = Stats(self.bot, self.update, self.user_data)
            stats.process()

        elif self.chosen_option.startswith('auto_update_indoor_ride'):
            setup = AutoUpdateIndoorRide(self.bot, self.update, self.user_data, self.chosen_option)
            setup.process()

        elif self.chosen_option.startswith('activity_summary'):
            activity_summary = ActivitySummary(self.bot, self.update, self.user_data)
            activity_summary.process()
