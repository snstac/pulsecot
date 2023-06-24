#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Greg Albrecht <oss@undef.net>
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
# Author:: Greg Albrecht W2GMD <oss@undef.net>
#

"""PulseCOT Constants."""

import json
import os
import pkg_resources

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


DEFAULT_POLL_INTERVAL: int = 120
DEFAULT_COT_STALE: str = "130"
DEFAULT_AGENCY_IDS: str = "21105,EMS1384,41000"
DEFAULT_PP_URL: str = "https://web.pulsepoint.org/DB/giba.php?agency_id="
DEFAULT_PP_AED_URL: str = "https://api.pulsepoint.org/v2/aed?apikey=mSwngLqWvSrQEVWu4eFF62Z2fZgsnCD5ZTaA8ZV&agencyid="
DEFAULT_PP_AED_API_USERNAME: str = "aedviewer"
DEFAULT_PP_AED_API_PASSWORD: str = "1ScOvupxfZ"


DEFAULT_PP_CALL_TYPES_FILE: str = os.getenv(
    "PP_CALL_TYPES_FILE",
    pkg_resources.resource_filename(__name__, "data/call_types.json"),
)

with open(DEFAULT_PP_CALL_TYPES_FILE, "r") as call_types_file:
    PP_CALL_TYPES: dict = json.load(call_types_file)
