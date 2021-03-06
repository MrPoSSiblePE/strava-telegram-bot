#  -*- encoding: utf-8 -*-

from common.operations import Operations
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class Challenges2020:

    def __init__(self, bot, update):
        self.bot = bot
        self.update = update
        self.operations = Operations()
        self.strava_telegram_webhooks_resource = StravaTelegramWebhooksResource()

    def get_strava_data(self, athlete_id):
        return self.strava_telegram_webhooks_resource.get_athlete_stats_by_athlete_id(athlete_id)

    def cs_vs_sa(self):
        stats_cr = self.get_strava_data(877837)
        stats_sa = self.get_strava_data(5577083)

        cr_at_distance = round(self.operations.meters_to_kilometers(float(stats_cr['ride_at_distance'])), 2)
        sa_at_distance = round(self.operations.meters_to_kilometers(float(stats_sa['ride_at_distance'])), 2)

        cr_ytd_distance = round(self.operations.meters_to_kilometers(float(stats_cr['ride_ytd_distance'])), 2)
        sa_ytd_distance = round(self.operations.meters_to_kilometers(float(stats_sa['ride_ytd_distance'])), 2)

        cr_at_hundreds = int(stats_cr['ride_at_hundred'])
        sa_at_hundreds = int(stats_sa['ride_at_hundred'])

        message = "*Chethan Ram vs Satish Addanki*\n\n\n"

        if cr_at_distance > sa_at_distance:
            at_name = "Chethan Ram"
            at_distance = cr_at_distance - sa_at_distance
        else:
            at_name = "Satish Addanki"
            at_distance = sa_at_distance - cr_at_distance

        at_distance = "{0:.2f}".format(round(at_distance, 2))

        if cr_ytd_distance > sa_ytd_distance:
            ytd_name = "Chethan Ram"
            ytd_distance = cr_ytd_distance - sa_ytd_distance
        else:
            ytd_name = "Satish Addanki"
            ytd_distance = sa_ytd_distance - cr_ytd_distance

        ytd_distance = "{0:.2f}".format(round(ytd_distance, 2))

        if cr_at_hundreds > sa_at_hundreds:
            name = "Chethan Ram"
            hundreds = cr_at_hundreds - sa_at_hundreds
        else:
            name = "Satish Addanki"
            hundreds = sa_at_hundreds - cr_at_hundreds

        message += "_Distance All Time_: {at_name} leads by {at_distance} km\n\n".format(at_name=at_name,
                                                                                         at_distance=at_distance)
        message += "_Distance Year to Date_: {ytd_name} leads by {ytd_distance} km\n\n".format(ytd_name=ytd_name,
                                                                                               ytd_distance=ytd_distance)
        message += "_Hundreds_: {name} leads by {hundreds} hundreds\n\n\n".format(name=name, hundreds=hundreds)

        message += "*Chethan Ram*:\n\nDistance All Time: {cr_at_distance} km\nDistance Year to Date: {cr_ytd_distance} km\nTotal Hundreds: {cr_at_hundreds}\n\n".format(
            cr_at_distance=cr_at_distance, cr_ytd_distance=cr_ytd_distance, cr_at_hundreds=cr_at_hundreds)
        message += "*Satish Addankni*:\n\nDistance All Time: {sa_at_distance} km\nDistance Year to Date: {sa_ytd_distance} km\nTotal Hundreds: {sa_at_hundreds}\n\n".format(
            sa_at_distance=sa_at_distance, sa_ytd_distance=sa_ytd_distance, sa_at_hundreds=sa_at_hundreds)

        return message

    def main(self):
        message = self.cs_vs_sa()
        self.update.message.reply_text(message, parse_mode="Markdown")
        self.strava_telegram_webhooks_resource.send_message(message)
