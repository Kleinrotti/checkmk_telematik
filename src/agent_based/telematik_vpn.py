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
# <name>|<status>
# <<<telematik_vpn:sep(124)>>>
# VPNTIStatus|Online

from dataclasses import dataclass
from typing import List, Final

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


STATE_MAPPING: Final = {
    "Online": State.OK,
    "Offline": State.CRIT
}


@dataclass(frozen=True)
class VPN():
    name: str
    status: str


Section = List[VPN]


def parse_telematik_vpn(string_table: StringTable) -> Section:
    return [
        VPN(name, status) for name, status in string_table
    ]


def discovery_telematik_vpn(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item.name)


def check_telematik_vpn(item: str, section: Section) -> CheckResult:
    state = State.OK
    vpn = None
    for sec in section:
        if item == sec.name:
            vpn = sec
            break
    if vpn is None:
        return None
    text = f"Status: {vpn.status}"
    state = STATE_MAPPING[vpn.status]
    yield Result(state=state, summary=text)


register.agent_section(
    name="telematik_vpn",
    parse_function=parse_telematik_vpn
)


register.check_plugin(
    name="telematik_vpn",
    service_name="%s",
    sections=['telematik_vpn'],
    discovery_function=discovery_telematik_vpn,
    check_function=check_telematik_vpn
)
