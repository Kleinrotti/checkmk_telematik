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

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    ServiceState,
    DefaultValue,
    DictElement
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostAndItemCondition


def _parameter_valuespec_telematik_konnektor_operation():
    return Dictionary(
        elements={
            "fatal": DictElement(
                parameter_form=ServiceState(
                    title=Title("Severity Fatal"),
                    prefill=DefaultValue(ServiceState.CRIT),
                )
            ),
            "error": DictElement(
                parameter_form=ServiceState(
                    title=Title("Severity Error"),
                    prefill=DefaultValue(ServiceState.CRIT),
                )
            ),
            "warning": DictElement(
                parameter_form=ServiceState(
                    title=Title("Severity Warning"),
                    prefill=DefaultValue(ServiceState.WARN),
                )
            ),
            "info": DictElement(
                parameter_form=ServiceState(
                    title=Title("Severity Info"),
                    prefill=DefaultValue(ServiceState.WARN),
                )
            )
        }
    )


rule_spec_telematik_konnektor_operation = CheckParameters(
    name="telematik_operation",
    title=Title("Telematikinfrastrukur Operation"),
    condition=HostAndItemCondition(item_title=Title("Operation name")),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_telematik_konnektor_operation
)
