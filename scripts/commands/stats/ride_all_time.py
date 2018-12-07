#  -*- encoding: utf-8 -*-

from os import sys, path

from stravalib import unithelper

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.operations import Operations


class RideAllTimeStats(object):

    def __init__(self):
        self.operations = Operations()

    def calculate(self, input_ride_all_time_stats, activity):
        if not self.operations.is_flagged_or_private(activity):
            input_ride_all_time_stats['rides'] += 1
            input_ride_all_time_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
            input_ride_all_time_stats['elevation_gain'] += int(activity.total_elevation_gain)
            input_ride_all_time_stats['distance'] += float(activity.distance)
            if self.operations.is_indoor(activity):
                input_ride_all_time_stats['indoor_distance'] += float(activity.distance)
                input_ride_all_time_stats['indoor_moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
                input_ride_all_time_stats['indoor_rides'] += 1
            if 50000.0 <= float(activity.distance) < 100000.0:
                input_ride_all_time_stats['fifties'] += 1
            elif 100000.0 <= float(activity.distance) < 150000.0:
                input_ride_all_time_stats['hundreds'] += 1
            elif 150000.0 < float(activity.distance) < 200000.0:
                input_ride_all_time_stats['one_hundred_fifties'] += 1
                input_ride_all_time_stats['hundreds'] += 1
            elif float(activity.distance) > 200000.0:
                input_ride_all_time_stats['two_hundreds'] += 1
                input_ride_all_time_stats['hundreds'] += 1

        return input_ride_all_time_stats

    def format(self, input_ride_all_time_stats, output_ride_all_time_stats):
        return output_ride_all_time_stats.format(
            rides=input_ride_all_time_stats['rides'],
            indoor_rides=input_ride_all_time_stats['indoor_rides'],
            distance=self.operations.meters_to_kilometers(input_ride_all_time_stats['distance']),
            indoor_distance=self.operations.meters_to_kilometers(input_ride_all_time_stats['indoor_distance']),
            moving_time=self.operations.seconds_to_human_readable(input_ride_all_time_stats['moving_time']),
            indoor_moving_time=self.operations.seconds_to_human_readable(
                input_ride_all_time_stats['indoor_moving_time']),
            elevation_gain=self.operations.meters_to_kilometers(input_ride_all_time_stats['elevation_gain']),
            fifties=input_ride_all_time_stats['fifties'],
            hundreds=input_ride_all_time_stats['hundreds'],
            one_hundred_fifties=input_ride_all_time_stats['one_hundred_fifties'],
            two_hundreds=input_ride_all_time_stats['two_hundreds'])
