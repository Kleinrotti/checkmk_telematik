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
# <name>|<ipv4>|<connected>|<slots>|<mac>|<productName>|<vendor>|<productVersion>|<hwVersion>|<fwVersion>|<physical>|<workplaces>
# <<<telematik_terminal:sep(124)>>>
# ST-1506-A00031472|10.110.122.167|true|4|10-1c-B3-16-f8-b4|ST1506|DECHY|1.7.1|4.0.0|3.0.0|true|test1;test2;test3

from dataclasses import dataclass
from typing import List

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

telematik_terminal_factory_settings = {
    'true': 0,
    'false': 1
}


@dataclass(frozen=True)
class Terminal():
    name: str
    ipv4: str
    connected: str
    slots: int
    mac: str
    productName: str
    vendor: str
    productVersion: str
    hwVersion: str
    fwVersion: str
    isPhysical: str
    workplaceids: str


Section = List[Terminal]


def parse_telematik_terminal(string_table: StringTable) -> Section:
    return [
        Terminal(name, ipv4, connected, slots, mac, productName,
                 vendor, productVersion, hwVersion, fwVersion, isPhysical, workplaceids)
        for name, ipv4, connected, slots, mac, productName, vendor,
        productVersion, hwVersion, fwVersion, isPhysical, workplaceids in string_table
    ]


def discovery_telematik_terminal(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item.name)


def check_telematik_terminal(item: str, params, section: Section) -> CheckResult:
    # search for the corresponding item in the section
    term = next(filter(lambda x: x.name == item, section), None)
    if term is None:
        return None
    # get the state from the connected value
    state = State(params[term.connected.lower()])
    text = f"Vendor: {term.vendor}, Model: {term.productName}, Connected: {term.connected}"
    detail = f"Ipv4: {term.ipv4}\nMAC: {term.mac}\nProduct version: {term.productVersion}\nHW version: {term.hwVersion}\nFW version: {term.fwVersion}\nSlots: {term.slots}\nPhysical: {term.isPhysical}\n"
    # split every colon to get it as list and remove the last element because its empty due to the colon at the end
    workplaces = term.workplaceids.split(';')[:-1]
    for workplace in workplaces:
        detail += f"\nWorkplace: {workplace}"
    yield Result(state=state, summary=text, details=detail)


register.agent_section(
    name="telematik_terminal",
    parse_function=parse_telematik_terminal
)


register.check_plugin(
    name="telematik_terminal",
    service_name="Card terminal %s",
    sections=['telematik_terminal'],
    discovery_function=discovery_telematik_terminal,
    check_function=check_telematik_terminal,
    check_ruleset_name="telematik_terminal",
    check_default_parameters=telematik_terminal_factory_settings,
)
