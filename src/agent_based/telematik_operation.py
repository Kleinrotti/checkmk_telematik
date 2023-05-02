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
# <condition>|<severity>|<type>|<value>|<validFrom>
# <<<telematik_operation:sep(124)>>>
# EC_No_Online_Connection|Error|Operation|false|2023-04-25T22:34:51.878Z

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


@dataclass(frozen=True)
class Operation():
    condition: str
    severity: str
    type: str
    value: bool
    validFrom: str


telematik_operation_factory_settings = {
    'fatal': 2,
    'error': 2,
    'warning': 1,
    'info': 1,
}


Section = List[Operation]


def parse_telematik_operation(string_table: StringTable) -> Section:
    return [
        Operation(condition, severity, type, value, validFrom)
        for condition, severity, type, value, validFrom in string_table
    ]


def discovery_telematik_operation(section: Section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item.condition)


def check_telematik_operation(item, params, section: Section) -> CheckResult:
    state = State.OK
    condition = None
    for sec in section:
        if item == sec.condition:
            condition = sec
            break
    if condition is None:
        return None
    text = f"Problem: {condition.value}, Severity: {condition.severity}"
    detail = f"Type: {condition.type}\n Valid from: {condition.validFrom}"
    if condition.value == "true":
        state = State(params[condition.severity.lower()])
    yield Result(state=state, summary=text, details=detail)


register.agent_section(
    name="telematik_operation",
    parse_function=parse_telematik_operation
)


register.check_plugin(
    name="telematik_operation",
    service_name="%s",
    sections=['telematik_operation'],
    discovery_function=discovery_telematik_operation,
    check_function=check_telematik_operation,
    check_ruleset_name="telematik_operation",
    check_default_parameters=telematik_operation_factory_settings,
)
