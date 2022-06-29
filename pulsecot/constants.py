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

"""SFPDCADCOT Constants."""

import logging
import os

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


DEFAULT_POLL_INTERVAL: int = 300
DEFAULT_COT_STALE: str = "305"

DEFAULT_INCIDENT_TYPES: dict = {
    "AA": "Auto Aid",
    "MU": "Mutual Aid",
    "ST": "Strike Team/Task Force",
    "AC": "Aircraft Crash",
    "AE": "Aircraft Emergency",
    "AES": "Aircraft Emergency Standby",
    "LZ": "Landing Zone",
    "AED": "AED Alarm",
    "OA": "Alarm",
    "CMA": "Carbon Monoxide",
    "FA": "Fire Alarm",
    "MA": "Manual Alarm",
    "SD": "Smoke Detector",
    "TRBL": "Trouble Alarm",
    "WFA": "Waterflow Alarm",
    "FL": "Flooding",
    "LR": "Ladder Request",
    "LA": "Lift Assist",
    "PA": "Police Assist",
    "PS": "Public Service",
    "SH": "Sheared Hydrant",
    "EX": "Explosion",
    "PE": "Pipeline Emergency",
    "TE": "Transformer Explosion",
    "AF": "Appliance Fire",
    "CHIM": "Chimney Fire",
    "CF": "Commercial Fire",
    "WSF": "Confirmed Structure Fire",
    "WVEG": "Confirmed Vegetation Fire",
    "CB": "Controlled Burn/Prescribed Fire",
    "ELF": "Electrical Fire",
    "EF": "Extinguished Fire",
    "FIRE": "Fire",
    "FULL": "Full Assignment",
    "IF": "Illegal Fire",
    "MF": "Marine Fire",
    "OF": "Outside Fire",
    "PF": "Pole Fire",
    "GF": "Refuse/Garbage Fire",
    "RF": "Residential Fire",
    "SF": "Structure Fire",
    "VEG": "Vegetation Fire",
    "VF": "Vehicle Fire",
    "WCF": "Working Commercial Fire",
    "WRF": "Working Residential Fire",
    "BT": "Bomb Threat",
    "EE": "Electrical Emergency",
    "EM": "Emergency",
    "ER": "Emergency Response",
    "GAS": "Gas Leak",
    "HC": "Hazardous Condition",
    "HMR": "Hazmat Response",
    "TD": "Tree Down",
    "WE": "Water Emergency",
    "AI": "Arson Investigation",
    "HMI": "Hazmat Investigation",
    "INV": "Investigation",
    "OI": "Odor Investigation",
    "SI": "Smoke Investigation",
    "LO": "Lockout",
    "CL": "Commercial Lockout",
    "RL": "Residential Lockout",
    "VL": "Vehicle Lockout",
    "IFT": "Interfacility Transfer",
    "ME": "Medical Emergency",
    "MCI": "Multi Casualty",
    "EQ": "Earthquake",
    "FLW": "Flood Warning",
    "TOW": "Tornado Warning",
    "TSW": "Tsunami Warning",
    "CA": "Community Activity",
    "FW": "Fire Watch",
    "NO": "Notification",
    "STBY": "Standby",
    "TEST": "Test",
    "TRNG": "Training",
    "UNK": "Unknown",
    "AR": "Animal Rescue",
    "CR": "Cliff Rescue",
    "CSR": "Confined Space",
    "ELR": "Elevator Rescue",
    "RES": "Rescue",
    "RR": "Rope Rescue",
    "TR": "Technical Rescue",
    "TNR": "Trench Rescue",
    "USAR": "Urban Search and Rescue",
    "VS": "Vessel Sinking",
    "WR": "Water Rescue",
    "TCE": "Expanded Traffic Collision",
    "RTE": "Railroad/Train Emergency",
    "TC": "Traffic Collision",
    "TCS": "Traffic Collision Involving Structure",
    "TCT": "Traffic Collision Involving Train",
    "WA": "Wires Arcing",
    "WD": "Wires Down",
}
