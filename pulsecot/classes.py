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

"""PulseCOT Class Definitions."""

import asyncio
import json
import random

from typing import Optional, Union

import aiohttp

import pytak
import pulsecot

from pulsecot.gnu import decode_pulse


class PulseWorker(pytak.QueueWorker):
    """Read CAD Data, renders to CoT, and puts on Queue."""

    agency_details: dict = {}

    async def handle_data(self, data: dict) -> None:
        """Transform Data to COT and puts it onto TX queue."""

        if not data:
            return None

        for incident in data.get("incidents", []):
            event: Optional[bytes] = pulsecot.incident_to_cot(
                incident, config=self.config, agency=data.get("agency")
            )

            if not event:
                self._logger.debug("Empty CoT")
                continue

            await self.put_queue(event)

    async def get_pp_feed(self, agency_id: str) -> Optional[dict]:
        """Get PulsePoint feed."""
        url: str = f"{pulsecot.DEFAULT_PP_URL}?resource=incidents&agencyid={agency_id}"

        self._logger.debug("Getting PulsePoint feed from %s", url)

        if not self.session:
            self._logger.error("Session not created")
            return None
        if self.session.closed:
            self._logger.error("Session closed")
            return None

        async with self.session.get(url) as resp:
            if resp.status != 200:
                response_content = await resp.text()
                self._logger.error("Received HTTP Status %s for %s", resp.status, url)
                self._logger.error(response_content)
                self._logger.error(resp.headers)
                self._logger.error(resp.request_info.headers)
                return None

            json_resp = await resp.json()  # content_type="text/html")
            if json_resp is None:
                return None

            decoded_data: Optional[dict] = None
            try:
                decoded_data = decode_pulse(json_resp)
            except json.decoder.JSONDecodeError as exc:
                self._logger.error("Unable to decode JSON")
                # self._logger.info(json_resp)
                self._logger.exception(exc)

            if not decoded_data:
                return None

            incidents: Optional[dict] = decoded_data.get("incidents", {})
            if not incidents:
                return None

            active: Optional[dict] = incidents.get("active")
            if not active:
                return None

            data = {
                "incidents": active,
                "agency": self.agency_details.get(agency_id, {}),
            }

            await self.handle_data(data)
        return None

    async def run(self) -> None:
        """Run this Thread, Reads from Pollers."""
        self._logger.info("Running %s", self.__class__)

        poll_interval: str = self.config.get(
            "POLL_INTERVAL", pulsecot.DEFAULT_POLL_INTERVAL
        )
        agency_ids: str = self.config.get("AGENCY_IDS", pulsecot.DEFAULT_AGENCY_IDS)

        # Populate the agency hints:
        if not self.config.get("DONT_UPDATE_AGENCY"):
            for agency in agency_ids.split(","):
                self._logger.info("Populating PulsePoint agency details for %s", agency)
                self.agency_details[agency] = {}
                agency_info = pulsecot.get_agency_info(agency)
                if not agency_info:
                    self._logger.warning(
                        "Agency %s not found in PulsePoint agency list", agency
                    )
                    continue
                self.agency_details[agency] = agency_info

        async with aiohttp.ClientSession(
            headers=pulsecot.PULSEPOINT_HEADERS
        ) as self.session:
            while True:
                self._logger.info(
                    "%s polling %s every %ss", self.__class__, agency_ids, poll_interval
                )

                agencies = agency_ids.split(",")
                random.shuffle(agencies)
                for agency in agencies:
                    self._logger.info(
                        "Polling agency %s: %s",
                        agency,
                        self.agency_details.get(agency, {}).get("agencyname"),
                    )
                    await self.get_pp_feed(agency.strip())
                    await asyncio.sleep(random.random() * 10)
                await asyncio.sleep(int(poll_interval))
