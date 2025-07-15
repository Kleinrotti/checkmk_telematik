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


from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    ServiceState,
    DefaultValue,
    SimpleLevels,
    LevelDirection,
    Integer
)
from cmk.rulesets.v1.rule_specs import HostAndServiceCondition, CheckParameters, Topic


def _parameter_valuespec_telematik_konnektor_card():
    return Dictionary(
        elements={
            "verified": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when SMC card is verified"),
                    prefill=DefaultValue(ServiceState.OK),
                ),
            ),
            "verifiable": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when SMC card is verifiable"),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),),
            "blocked": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when SMC card is blocked"),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),),
            "transport_pin": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when SMC card is in transport PIN mode"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),),
            "empty_pin": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when SMC card PIN is empty"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),),
            "disabled": DictElement(
                parameter_form=ServiceState(
                    title=Title("State when SMC card PIN is disabled"),
                    prefill=DefaultValue(ServiceState.WARN),
                ),),
            "cert": DictElement(
                parameter_form=Dictionary(
                    title=Title("Check SMC cards certificate expiration"),
                    help_text=Help(
                        "Set these values if you want to monitor the"
                        "certificate expiration of the SMC cards"
                    ),
                    elements={
                        "cert_days": DictElement(
                            parameter_form=SimpleLevels[int](
                                title=Title("Age"),
                                form_spec_template=Integer(),
                                level_direction=LevelDirection.LOWER,
                                prefill_fixed_levels=DefaultValue(value=(60, 30))
                            ),
                            required=True,
                        )
                    }
                )
            )
        }
    )


rule_spec_telematik_konnektor_card = CheckParameters(
    name="telematik_card",
    title=Title("Telematikinfrastrukur SMC Card"),
    condition=HostAndServiceCondition,
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_telematik_konnektor_card,
)
