SFPD CAD to Cursor-On-Target Gateway.
*************************************

.. image:: https://raw.githubusercontent.com/ampledata/pulsecot/main/docs/Screenshot_20201026-142037_ATAK-25p.jpg
   :alt: Screenshot of ADS-B PLI in ATAK.
   :target: https://github.com/ampledata/pulsecot/blob/main/docs/Screenshot_20201026-142037_ATAK.jpg


The SFPD CAD to Cursor-On-Target Gateway (SFPDCADCOT) transforms SFPD Computer 
Aided Dispatch (CAD) calls for service to Cursor-On-Target (COT) Events for 
display on Situational Awareness applications such as the Android Team 
Awareness Kit (ATAK), WinTAK, RaptorX, TAKX, iTAK, et al. More information on 
the TAK suite of tools cal be found at: https://www.tak.gov/

Support Development
===================

**Tech Support**: Email support@undef.net or Signal/WhatsApp: +1-310-621-9598

This tool has been developed for the Disaster Response, Public Safety and
Frontline Healthcare community. This software is currently provided at no-cost
to users. Any contribution you can make to further this project's development
efforts is greatly appreciated.

.. image:: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
    :target: https://www.buymeacoffee.com/ampledata
    :alt: Support Development: Buy me a coffee!


Installation
============

SFPDCADCOT's functionality provided by a command-line program called `pulsecot`.

Installing as a Debian / Ubuntu Package [Recommended]::

    $ sudo apt update
    $ wget https://github.com/ampledata/pytak/releases/latest/download/python3-pytak_latest_all.deb
    $ sudo apt install -f ./python3-pytak_latest_all.deb
    $ wget https://github.com/ampledata/pulsecot/releases/latest/download/python3-pulsecot_latest_all.deb
    $ sudo apt install -f ./python3-pulsecot_latest_all.deb


Install from the Python Package Index (PyPI) [Advanced Users]::

    $ python3 -m pip install pulsecot


Install from this source tree [Developers]::

    $ git clone https://github.com/ampledata/pulsecot.git
    $ cd pulsecot/
    $ python3 setup.py install


Usage
=====

The `pulsecot` command-line program has 2 runtime arguments::

    usage: pulsecot [-h] [-c CONFIG_FILE] 

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG_FILE, --CONFIG_FILE CONFIG_FILE. Default: config.ini


Configuration
=============

Configuration parameters can be specified either via environment variables or in
a INI-stile configuration file.

Parameters:

* **CAD_URL**: (*optional*) SFPD CAD Data URL.
* **COT_URL**: (*optional*) Destination for Cursor-On-Target messages. See `PyTAK <https://github.com/ampledata/pytak#configuration-parameters>`_ for options.
* **POLL_INTERVAL**: (*optional*) Period in seconds to poll API. Default: 30

There are other configuration parameters available via `PyTAK <https://github.com/ampledata/pytak#configuration-parameters>`_.

Configuration parameters are imported in the following priority order:

1. ``config.ini`` (if exists) or ``-c <filename>`` (if specified).
2. Environment Variables (if set).
3. Defaults.


Source
======
SFPDCADCOT source can be found on Github: https://github.com/ampledata/pulsecot


Author
======
SFPDCADCOT is written and maintained by Greg Albrecht W2GMD oss@undef.net

https://ampledata.org/


Copyright
=========
SFPDCADCOT is Copyright 2022 Greg Albrecht


License
=======
Copyright 2022 Greg Albrecht <oss@undef.net>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

