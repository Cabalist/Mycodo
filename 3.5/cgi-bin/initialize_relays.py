#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  GPIO-initialize.py - Initialize GPIO pins connected to relays and
#                       sets them off.
#
#  Copyright (C) 2015  Kyle T. Gabriel
#
#  This file is part of Mycodo
#
#  Mycodo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Mycodo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Mycodo. If not, see <http://www.gnu.org/licenses/>.
#
#  Contact at kylegabriel.com

import RPi.GPIO as GPIO

from config import SQL_DATABASE_MYCODO
from databases.mycodo_db.models import Relays
from databases.utils import session_scope

# configure Session class with desired options

MYCODO_DB_PATH = 'sqlite://' + SQL_DATABASE_MYCODO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Start the session
with session_scope(MYCODO_DB_PATH) as the_session:
    # Get all them relays
    relays = the_session.query(Relays).all()

    for each_relay in relays:
        # Setup all the pins as an output
        GPIO.setup(each_relay.pin, GPIO.OUT)

        # If the relay is not set to start make sure it is set to OFF
        if not each_relay.start_state:
            GPIO.output(each_relay.pin, not each_relay.trigger)

        # Turn on relays that are set to startup on
        if each_relay.start_state:
            # Only push the trigger to the relay with the start_state
            GPIO.output(each_relay.pin, each_relay.trigger)


