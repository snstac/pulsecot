#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright Sensors & Signals LLC https://www.snstac.com/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""PulseCOT Constants."""

import json
import os
import pkg_resources

DEFAULT_POLL_INTERVAL: int = 120
DEFAULT_COT_STALE: str = "600"
DEFAULT_AGENCY_IDS: str = "21105,EMS1384,41000"
DEFAULT_PP_URL: str = "https://api.pulsepoint.org/v1/webapp"

DEFAULT_PP_CALL_TYPES_FILE: str = os.getenv(
    "PP_CALL_TYPES_FILE",
    pkg_resources.resource_filename(__name__, "data/call_types.json"),
)

with open(DEFAULT_PP_CALL_TYPES_FILE, "r") as call_types_file:
    PP_CALL_TYPES: dict = json.load(call_types_file)


# Headers for the new PulsePoint API
PULSEPOINT_HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://web.pulsepoint.org/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}
