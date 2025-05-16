#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright Sensors & Signals LLC https://www.snstac.com
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

"""PulseCOT Functions."""

import json
import warnings
import urllib.request

import xml.etree.ElementTree as ET

from configparser import SectionProxy
from typing import Optional, Union, Set

import pytak
import pulsecot  # pylint: disable=cyclic-import


def create_tasks(config: SectionProxy, clitool: pytak.CLITool) -> Set[pytak.Worker,]:
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
    return set([pulsecot.PulseWorker(clitool.tx_queue, config)])


def get_agency_info(agency) -> Union[dict, None]:
    """
    Get PulsePoint agencies.

    Returns
    -------
    `dict`
        Dictionary of PulsePoint agencies.
    """
    url: str = f"{pulsecot.DEFAULT_PP_URL}?resource=agencies&agencyid={agency}"
    req = urllib.request.Request(url)
    for key, value in pulsecot.PULSEPOINT_HEADERS.items():
        req.add_header(key, value)
    content = urllib.request.urlopen(req).read()
    if not content:
        return None

    data = json.loads(content)
    if not data:
        return None

    data = pulsecot.gnu.decode_pulse(data)
    if not data:
        return None

    return data.get("agencies", [])[0]


def incident_to_cot_xml(
    incident: dict,
    config: Union[SectionProxy, dict, None] = None,
    agency: Optional[dict] = None,
) -> Union[ET.Element, None]:
    """
    Serialize a PulsePoint Incidents as Cursor on Target XML.

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
    config = config or {}
    agency = agency or {}

    lat = incident.get("Latitude")
    lon = incident.get("Longitude")

    if lat is None or lon is None:
        return None

    if lat == "0.0000000000" or lon == "0.0000000000":
        return None

    remarks_fields = []

    pp_id: str = incident["ID"]

    pp_call_type: str = incident["PulsePointIncidentCallType"]
    call_type_meta = pulsecot.PP_CALL_TYPES.get(pp_call_type)
    if not call_type_meta:
        warnings.warn(
            f"No Call Type metadata for {pp_call_type=} from agency {agency.get('id')}: {agency.get('agencyname')}",
            SyntaxWarning,
        )
        call_type_meta = pulsecot.PP_CALL_TYPES.get("Default")

    call_type: str = call_type_meta.get("name")

    cot_stale: int = int(config.get("COT_STALE", pulsecot.DEFAULT_COT_STALE))

    cot_host_id: str = config.get("COT_HOST_ID", pytak.DEFAULT_HOST_ID)
    cot_uid: str = f"PulsePoint-{agency.get('agency_initials')}-{pp_id}"
    cot_type: str = "a-u-G"

    callsign = f"{call_type} - {incident['FullDisplayAddress']}"
    iconsetpath = "f7f71666-8b28-4b57-9fbb-e38e61d33b79/Google/caution.png"

    remarks_fields.append(callsign)
    remarks_fields.append(agency.get("short_agencyname"))

    live_radio: Union[list, None] = agency.get("live_radio")
    if live_radio:
        if "URL" in live_radio[0]:
            link = ET.Element("link")
            radio_url = live_radio[0].get("URL")
            remarks_fields.append(f"Radio: {radio_url}")

    remarks_fields.append(f"PPCallType: {pp_call_type}")
    remarks_fields.append(f"PPID: {pp_id}")

    point = ET.Element("point")
    point.set("lat", str(lat))
    point.set("lon", str(lon))

    point.set("ce", str("9999999.0"))
    point.set("le", str("9999999.0"))
    point.set("hae", str("9999999.0"))

    contact = ET.Element("contact")
    contact.set("callsign", str(callsign))

    usericon = ET.Element("usericon")
    _call_type = call_type.lower()

    if "fire" in _call_type:
        cot_type = "a-n-G"
        iconsetpath = "83198b4872a8c34eb9c549da8a4de5a28f07821185b39a2277948f66c24ac17a/GeoOps/Fire Location.png"
    elif "medical" in _call_type:
        cot_type = "a-n-G"
        iconsetpath = "83198b4872a8c34eb9c549da8a4de5a28f07821185b39a2277948f66c24ac17a/GeoOps/Medical.png"

    usericon.set("iconsetpath", iconsetpath)

    detail = ET.Element("detail")
    detail.append(contact)
    detail.append(usericon)

    remarks = ET.Element("remarks")

    remarks_fields.append(f"{cot_host_id}")

    _remarks = " -\n ".join(list(filter(None, remarks_fields)))

    remarks.text = _remarks
    detail.append(remarks)

    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", cot_type)
    root.set("uid", cot_uid)
    root.set("how", "m-g")
    root.set("time", pytak.cot_time())
    root.set("start", incident["CallReceivedDateTime"])
    root.set("stale", pytak.cot_time(cot_stale))

    root.append(point)
    root.append(detail)

    return root


def incident_to_cot(
    call: dict, config: Union[dict, None] = None, agency: Union[dict, None] = None
) -> Union[bytes, None]:
    """Wrapper that returns COT as an XML string."""
    cot: Union[ET.Element, None] = incident_to_cot_xml(call, config, agency)
    return (
        b"\n".join([pytak.DEFAULT_XML_DECLARATION, ET.tostring(cot)]) if cot else None
    )


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
