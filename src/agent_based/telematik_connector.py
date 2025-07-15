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
# <productTypeVersion>|<productName>|<productVendorName>|<tlsMandatory>|<clientAuthMandatory>|<hwVersion>|<fwVersion>
# <<<telematik_connector:sep(124)>>>
# 5.0.2|secunet konnektor 2.1.0|secunet Security Networks AG|true|false|2.1.0|5.0.5

from dataclasses import dataclass
from typing import List

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


@dataclass(frozen=True)
class Connector():
    productTypeVersion: str
    productName: str
    productVendorName: str
    tlsMandatory: str
    clientAuthMandatory: str
    hwVersion: str
    fwVersion: str


Section = List[Connector]


def parse_telematik_connector(string_table: StringTable) -> Section:
    return [
        Connector(productTypeVersion, productName, productVendorName, tlsMandatory, clientAuthMandatory,
                  hwVersion, fwVersion) for productTypeVersion, productName, productVendorName, tlsMandatory, clientAuthMandatory,
        hwVersion, fwVersion in string_table
    ]


def discovery_telematik_connector(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item.productName)


def check_telematik_connector(item, section: Section) -> CheckResult:
    connector = next((sec for sec in section if item == sec.productName), None)
    if not connector:
        return
    text = f"Product version {connector.productTypeVersion}"
    detail = (f"TLS mandatory: {connector.tlsMandatory}\nClient auth mandatory: {connector.clientAuthMandatory}\n"
              f"Hardware version: {connector.hwVersion}\nFirmware version: {connector.fwVersion}")
    yield Result(state=State.OK, summary=text, details=detail)


agent_section_telematik_connector = AgentSection(
    name="telematik_connector",
    parse_function=parse_telematik_connector,
    parsed_section_name="telematik_connector",
)

check_plugin_telematik_connector = CheckPlugin(
    name="telematik_connector",
    service_name="%s",
    discovery_function=discovery_telematik_connector,
    check_function=check_telematik_connector,
)
