#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

# Class for creating a WebVTT subtitles file from the
# JSON subtitles format from www.TED.com

import json
import requests
import time


class WebVTTcreator:

    WebVTTdocument = "WEBVTT\n\n"

    def __init__(self, url, offset=11820):
        self.url = url
        self.offset = offset

    def time_string(self, ms):
        """Create the '00:00:00.000' string representation of the time"""

        hours, remainder = divmod(ms, 3600000)
        minutes, remainder = divmod(remainder, 60000)
        seconds, miliseconds = divmod(remainder, 1000)
        return "%.2d:%.2d:%.2d.%.3d" % (hours, minutes, seconds, miliseconds)

    def is_json(self, json_data):
        try:
            json.loads(json_data)
        except ValueError:
            return False
        return True

    def create_WebVtt(self, json):
        """Create the WebVTT file from the given decoded json.
        Structure of a WebVTT file:

        WebVTT

        00:00:00.000 --> 00:00:00.000
        [start time --> end time]

        'content'
        """

        if "captions" in json:
            for subtitle in json["captions"]:
                startTime = int(subtitle["startTime"]) + self.offset
                duration = int(subtitle["duration"])
                content = subtitle["content"].strip()

                self.WebVTTdocument += (
                    self.time_string(startTime)
                    + " --> "
                    + self.time_string(startTime + duration)
                    + "\n"
                )
                self.WebVTTdocument += content + "\n\n"
        return self.WebVTTdocument

    def getVTT(self):
        """Loads the json representation of the subtitles form the given URL and decodes it, and returns its WebVTT representation"""

        dl_ok = False
        while not dl_ok:
            r = requests.get(self.url)
            if r.status_code == 429:
                time.sleep(30)
            elif r.status_code == 404:
                return None
            else:
                dl_ok = True
                subtitles_json = r.text
        if self.is_json(subtitles_json):
            return self.create_WebVtt(json.loads(subtitles_json))
        return None
