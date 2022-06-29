#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADSBXCOT Module Tests."""

import csv
import io

import xml.etree.ElementTree as ET

import pytest
import pulsecot.gnu

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2022 Greg Albrecht"
__license__ = "Apache License, Version 2.0"


def test_get_agencies():
    agencies = pulsecot.gnu.get_agencies()
    # print(agencies)
    # assert agencies == False


def test_find_agency():
    name: str = "San Francisco EMS"
    name = "Marin County"
    agency = pulsecot.gnu.find_agency(name)
    print(agency)
    assert False == True
    # print(agencies)
    # assert agencies == False
