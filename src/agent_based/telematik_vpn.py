#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2025 Kleinrotti <kleinrotti@saltcloud.de>

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

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Service,
    State,
    Result,
    StringTable
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
    vpn = next((sec for sec in section if item == sec.name), None)
    if not vpn:
        return
    text = f"Status: {vpn.status}"
    state = STATE_MAPPING.get(vpn.status, State.WARN)
    yield Result(state=state, summary=text)


agent_section_telematik_vpn = AgentSection(
    name="telematik_vpn",
    parse_function=parse_telematik_vpn,
    parsed_section_name="telematik_vpn",
)

check_plugin_telematik_vpn = CheckPlugin(
    name="telematik_vpn",
    service_name="%s",
    discovery_function=discovery_telematik_vpn,
    check_function=check_telematik_vpn,
)
