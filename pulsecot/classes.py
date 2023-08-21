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

"""PulseCOT Class Definitions."""

import asyncio
import random

from typing import Union

import aiohttp

import pytak
import pulsecot

from pulsecot.gnu import decode_pulse

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


class CADWorker(pytak.QueueWorker):

    """Reads CAD Data, renders to CoT, and puts on Queue."""

    agency_details: dict = {}

    async def handle_data(self, data: list) -> None:
        """
        Transforms Data to COT and puts it onto TX queue.
        """
        if not data:
            return

        for incident in data.get("incidents", []):
            event: Union[str, None] = pulsecot.incident_to_cot(
                incident, config=self.config, agency=data["agency"]
            )

            if not event:
                self._logger.debug("Empty CoT")
                continue

            await self.put_queue(event)

    async def get_pp_feed(self, agency_id: str) -> dict:
        if not agency_id:
            self._logger.warning("No agency_id specified, try `find_agency()`?")
            return

        url: str = f"{pulsecot.DEFAULT_PP_URL}{agency_id}"
        async with self.session.get(url) as resp:
            if resp.status != 200:
                response_content = await resp.text()
                self._logger.error("Received HTTP Status %s for %s", resp.status, url)
                self._logger.error(response_content)
                return

            json_resp = await resp.json(content_type="text/html")
            if json_resp == None:
                return

            decoded_data = decode_pulse(json_resp)

            active: Union[dict, None] = decoded_data.get("incidents", {}).get("active")
            if not active:
                return

            data = {"incidents": active, "agency": self.agency_details[agency_id]}

            await self.handle_data(data)

    async def run(self, number_of_iterations=-1) -> None:
        """Runs this Thread, Reads from Pollers."""
        self._logger.info("Running %s", self.__class__)

        poll_interval: str = self.config.get(
            "POLL_INTERVAL", pulsecot.DEFAULT_POLL_INTERVAL
        )
        agency_ids: str = self.config.get("AGENCY_IDS", pulsecot.DEFAULT_AGENCY_IDS)

        # Populate the agency hints:
        agencies = pulsecot.gnu.get_agencies()
        for agency_id in agency_ids.split(","):
            self.agency_details[agency_id] = agencies[agency_id]

        async with aiohttp.ClientSession() as self.session:
            while 1:
                self._logger.info(
                    "%s polling %s every %ss", self.__class__, agency_ids, poll_interval
                )
                for agency_id in agency_ids.split(","):
                    await self.get_pp_feed(agency_id.strip())
                    await asyncio.sleep(random.random() * 10)
                await asyncio.sleep(int(poll_interval))
