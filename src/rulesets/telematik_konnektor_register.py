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


from cmk.rulesets.v1 import Title, Help, Message
from cmk.rulesets.v1.form_specs import (
    DictElement,
    DefaultValue,
    Dictionary,
    Password,
    String,
    Integer,
    FixedValue,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import Topic, SpecialAgent
from cmk.rulesets.v1.form_specs.validators import LengthInRange


def _valuespec_special_agents_telematik_konnektor():
    return Dictionary(
        title=Title("Telematikinfrastruktur Konnektor Agent"),
        help_text=Help("This rule selects the Telematik Special Agent instead of the normal Check_MK Agent "
                       "which collects the data through the Konnektor API."),
        elements={
            "mandant": DictElement(
                parameter_form=String(
                    title=Title("Mandant"),
                ),
                required=True,
            ),
            "clientsystem": DictElement(
                parameter_form=String(
                    title=Title("Client system id"),
                ),
                required=True,
            ),
            "workplace": DictElement(
                parameter_form=String(
                    title=Title("Workplace id"),
                ),
                required=True,
            ),
            "port": DictElement(
                parameter_form=Integer(
                    title=Title("Port"),
                    prefill=DefaultValue(443)
                ),
                required=False,
            ),
            "client_auth": DictElement(
                parameter_form= CascadingSingleChoice(
                    title=Title("Use client authentication"),
                    help_text=Help("If your Konnektor is set to force client authentication you can provide "
                                   "your client certificate or credentials here."),
                    elements=[
                        CascadingSingleChoiceElement(
                            title=Title("With username and password"),
                            name="basic_auth",
                            parameter_form=Dictionary(
                                elements={
                                    "username": DictElement(
                                        parameter_form=String(
                                            title=Title("Username")
                                        ),
                                        required=True
                                    ),
                                    "password": DictElement(
                                        parameter_form=Password(
                                            title=Title("Password")
                                        ),
                                        required=True
                                    )
                                }
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            title=Title("With certificate"),
                            name="cert_auth",
                            parameter_form=Dictionary(
                                elements={
                                    "client_cert": DictElement(
                                        parameter_form=String(
                                            title=Title("Certificate path"),
                                            custom_validate=[
                                                LengthInRange(
                                                    min_value=1,
                                                    error_msg=Message("Please enter a valid path"),
                                                )
                                            ]
                                        ),
                                        required=True,
                                    ),
                                    "client_priv_key": DictElement(
                                        parameter_form=String(
                                            title=Title("Private key path"),
                                            custom_validate=[
                                                LengthInRange(
                                                    min_value=1,
                                                    error_msg=Message("Please enter a valid path"),
                                                )
                                            ]
                                        ),
                                        required=True
                                    )
                                }
                            )
                        )
                    ]
                )
            ),
            "verify_ssl": DictElement(
                parameter_form=FixedValue(
                    title=Title("Verify SSL certificate"),
                    value=True
                ),
                required=False,
            ),
            "mandant_wide": DictElement(
                parameter_form=FixedValue(
                    title=Title("Mandant wide"),
                    help_text=Help("Create services for all terminals and cards associated with the Konnektor for a mandant."
                                   "Leave this unchecked if you only want the terminal and cards from the remote card terminal."),
                    value= True,
                ),
                required=False,
            )
        }
    )


rule_spec_telematik_konnektor_datasource_programs = SpecialAgent(
    name="telematik_konnektor",
    title=Title("Telematikinfrastruktur Konnektor Agent"),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_special_agents_telematik_konnektor,
    help_text=(
        "This rule selects the Telematik Special Agent instead of the normal Check_MK Agent "
        "which collects the data through the Konnektor API."
    )
)
