"""
skill iss-tracker
Copyright (C) 2018  Andreas Lorensen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mycroft import MycroftSkill, intent_file_handler
import requests
import json


class IssTracker(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('tracker.iss.intent')
    def handle_tracker_iss(self, message):
        # get the 'current' latitude and longitude of the ISS from open-notify.org in JSON
        reqISSLocation = requests.get("http://api.open-notify.org/iss-now.json")
        issObj = json.loads(reqISSLocation.text)  # JSON payload of ISS location data
        latISS = issObj['iss_position']['latitude']
        lngISS = issObj['iss_position']['longitude']

        # construct a string witj ISS lat & long to determine a geographic object/toponym associated with it
        # This is "Reverse Gecoding" availbe from geonames.org
        # Sign up for a free user name at http://www.geonames.org/ and repalce YourUserName with it
        # !! remember to activate web servoces for your user name !!
        oceanGeoNamesReq = "http://api.geonames.org/oceanJSON?lat=" + latISS + "&lng=" + lngISS + "&username=mycroft_iss_tracker"
        landGeoNamesReq = "http://api.geonames.org/countryCodeJSON?formatted=true&lat=" + latISS + "&lng=" + lngISS + "&username=mycroft_iss_tracker&style=full"

        self.log.info(oceanGeoNamesReq)
        self.log.info(landGeoNamesReq)

        # Since the Earth is 3/4 water, we'll chek to see if the ISS is over water first;
        # in the case where this is not so, we handle the exception by  searching for a country it is
        # over, and is this is not coded for on GenNames, we just we say we don't know

        oceanGeoNamesRes = requests.get(oceanGeoNamesReq)
        toponymObj = json.loads(oceanGeoNamesRes.text)
        try:
            toponym = "the " + toponymObj['ocean']['name']
        except KeyError:
            landGeoNamesRes = requests.get(landGeoNamesReq)
            toponymObj = json.loads(landGeoNamesRes.text)
            toponym = toponymObj['countryName']
        except Exception:
            toponym = "unknown"

        # print "the ISS is over: " + toponym
        if toponym == "unknown":
            self.speak_dialog("location.unknown", {"latitude": latISS, "longitude": lngISS})
        else:
            self.speak_dialog("location.current", {"latitude": latISS, "longitude": lngISS, "toponym": toponym})


def create_skill():
    return IssTracker()
