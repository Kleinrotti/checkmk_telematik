#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Kleinrotti <kleinrotti@saltcloud.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# Sample agent output
# <cardHandle>|<cardType>|<slot>|<insertTime>|<certificateExpiration>|<holderName>|<iccsn>|<verified>
# <<<telematik_card:sep(124)>>>
# SMC-B-0000|SMC-B|4|2023-04-21T07:32:38.171Z|2025-11-06Z|Test Klinik|80376011731300016932|VERIFIED

from dataclasses import dataclass
from typing import List
from datetime import date, datetime

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    StringTable,
)

from .agent_based_api.v1 import (
    Result,
    State,
    Service,
    register
)


@dataclass(frozen=True)
class Card():
    cardHandle: str
    cardType: str
    slot: int
    insertTime: str
    certificateExpiration: str
    holderName: str
    iccsn: str
    verified: str


telematik_card_factory_settings = {
    'verified': 0,
    'verifiable': 2,
    'blocked': 2,
    'transport_pin': 1,
    'empty_pin': 1,
    'disabled': 1,
    '-': 0
}


Section = List[Card]


def parse_telematik_card(string_table: StringTable) -> Section:
    return [
        Card(cardHandle, cardType, slot, insertTime, certificateExpiration,
             holderName, iccsn, verified) for cardHandle, cardType, slot,
        insertTime, certificateExpiration, holderName,
        iccsn, verified in string_table
    ]


def discovery_telematik_card(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item.cardType + "-" + item.iccsn)


def check_telematik_card(item, params, section: Section) -> CheckResult:
    card = None
    for sec in section:
        if item == sec.cardType + "-" + sec.iccsn:
            card = sec
            break
    if card is None:
        return None
    state = State(params[card.verified.lower()])
    currentDate = date.today()
    # covert the string date to a date object
    # in the date is a 'Z' at the end which has to be cut off
    da = datetime.strptime(card.certificateExpiration.replace('Z', ''), '%Y-%m-%d').date()
    delta = (da - currentDate).days
    text = f"PIN Status: {card.verified}"
    # if thresholds were set in wato, check the expiricy
    if 'cert' in params:
        warn = params['cert']['cert_days'][0]
        crit = params['cert']['cert_days'][1]
        if delta <= crit:
            state = State.CRIT
            text += f", CRIT: Card certificate is expiring in {delta} days."
        elif delta <= warn:
            state = State.WARN
            text += f", WARN: Card certificate is expiring in {delta} days."
    detail = (f"Slot: {card.slot}\nInsert time: {card.insertTime}\nExpiration: "
              f"{card.certificateExpiration}\nOwner: {card.holderName}\nSerial: {card.iccsn}")
    yield Result(state=state, summary=text, details=detail)


register.agent_section(
    name="telematik_card",
    parse_function=parse_telematik_card
)


register.check_plugin(
    name="telematik_card",
    service_name="Card %s",
    sections=['telematik_card'],
    discovery_function=discovery_telematik_card,
    check_function=check_telematik_card,
    check_ruleset_name="telematik_card",
    check_default_parameters=telematik_card_factory_settings,
)
