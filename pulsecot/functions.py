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

"""PulseCOT Functions."""

import xml.etree.ElementTree as ET

from configparser import SectionProxy
from typing import Union, Set

import pytak
import pulsecot  # pylint: disable=cyclic-import
import pulsecot.gnu

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


def create_tasks(
    config: SectionProxy, clitool: pytak.CLITool
) -> Set[pytak.Worker,]:
    """
    Creates specific coroutine task set for this application.

    Parameters
    ----------
    config : `ConfigParser`
        Configuration options & values.
    clitool : `pytak.CLITool`
        A PyTAK Worker class instance.

    Returns
    -------
    `set`
        Set of PyTAK Worker classes for this application.
    """
    return set([pulsecot.CADWorker(clitool.tx_queue, config)])


def incident_to_cot_xml(
    incident: dict, config: Union[SectionProxy, None] = None
) -> Union[ET.Element, None]:
    """
    Serializes a PulsePoint Incidents as Cursor-On-Target XML.

    Parameters
    ----------
    incident : `dict`
        Key/Value data struct of PulsePoint Incident.
    config : `configparser.SectionProxy`
        Configuration options and values.

    Returns
    -------
    `xml.etree.ElementTree.Element`
        Cursor-On-Target XML ElementTree object.
    """
    config: dict = config or {}

    lat = incident["Latitude"]
    lon = incident["Longitude"]

    if lat is None or lon is None:
        return None

    remarks_fields = []
    pp_id: str = incident["ID"]
    pp_call_type: str = incident["PulsePointIncidentCallType"]
    call_type: str = pulsecot.gnu.DEFAULT_INCIDENT_TYPES.get(pp_call_type, pp_call_type)

    cot_stale = int(config.get("COT_STALE"))
    cot_host_id = config.get("COT_HOST_ID", pytak.DEFAULT_HOST_ID)
    cot_uid = f"PulsePoint-{pp_id}"

    if "fire" in pp_call_type.lower():
        cot_type = "a-h-G"
    else:
        cot_type = "a-u-G"

    callsign = f"{call_type} - {incident['FullDisplayAddress']}"

    remarks_fields.append(callsign)
    remarks_fields.append(f"PP Call Type: {pp_call_type}")
    remarks_fields.append(f"PP ID: {pp_id}")

    point = ET.Element("point")
    point.set("lat", str(lat))
    point.set("lon", str(lon))

    point.set("ce", str("9999999.0"))
    point.set("le", str("9999999.0"))
    point.set("hae", str("9999999.0"))

    uid = ET.Element("UID")
    uid.set("Droid", str(callsign))

    contact = ET.Element("contact")
    contact.set("callsign", str(callsign))

    track = ET.Element("track")
    track.set("course", str("9999999.0"))
    track.set("speed", str("9999999.0"))

    detail = ET.Element("detail")
    detail.set("uid", cot_uid)
    detail.append(uid)
    detail.append(contact)
    detail.append(track)

    remarks = ET.Element("remarks")

    remarks_fields.append(f"{cot_host_id}")

    _remarks = " - ".join(list(filter(None, remarks_fields)))

    remarks.text = _remarks
    detail.append(remarks)

    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", cot_type)
    root.set("uid", cot_uid)
    root.set("how", "m-g")
    # FIXME: Convert CAD timestamp to UTC, and use here:
    root.set("time", pytak.cot_time())
    root.set("start", pytak.cot_time())
    root.set("stale", pytak.cot_time(cot_stale))

    root.append(point)
    root.append(detail)

    return root


def incident_to_cot(call: dict, config: Union[dict, None] = None) -> Union[bytes, None]:
    """Wrapper that returns COT as an XML string."""
    cot: Union[ET.Element, None] = incident_to_cot_xml(call, config)
    return ET.tostring(cot) if cot else None


#  [{'AddressTruncated': '1',
#   'AgencyID': 'EMS1384',
#   'CallReceivedDateTime': '2022-06-28T22:31:09Z',
#   'CommonPlaceName': '',
#   'FullDisplayAddress': 'POTRERO AVE, SAN FRANCISCO, CA',
#   'ID': '1229224755',
#   'IsShareable': '0',
#   'Latitude': '37.7554100000',
#   'Longitude': '-122.4063120000',
#   'MedicalEmergencyDisplayAddress': 'null',
#   'PublicLocation': '1',
#   'PulsePointIncidentCallType': 'ME',
#   'StreetNumber': 'null'},
#  {'AddressTruncated': '1',
#   'AgencyID': 'EMS1384',
#   'CallReceivedDateTime': '2022-06-28T22:06:40Z',
#   'CommonPlaceName': '',
#   'FullDisplayAddress': 'ALVARADO ST, SAN FRANCISCO, CA',
#   'ID': '1229205458',
#   'IsShareable': '0',
#   'Latitude': '0.0000000000',
#   'Longitude': '0.0000000000',
#   'MedicalEmergencyDisplayAddress': 'null',
#   'PublicLocation': '0',
#   'PulsePointIncidentCallType': 'ME',
#   'StreetNumber': 'null'}]
