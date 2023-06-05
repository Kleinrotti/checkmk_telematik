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

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
)
from cmk.gui.plugins.wato.utils import RulespecGroupCheckParametersApplications
from cmk.gui.valuespec import Dictionary, MonitoringState, Tuple, Integer


def _parameter_valuespec_telematik_konnektor_card():
    return Dictionary(
        elements=[
            (
                "verified",
                MonitoringState(
                    title=_("State when SMC card is verified"),
                    default_value=0,
                )
            ),
            (
                "verifiable",
                MonitoringState(
                    title=_("State when SMC card is verifiable"),
                    default_value=2,
                ),
            ),
            (
                "blocked",
                MonitoringState(
                    title=_("State when SMC card is blocked"),
                    default_value=2,
                ),
            ),
            (
                "transport_pin",
                MonitoringState(
                    title=_("State when SMC card is in transport PIN mode"),
                    default_value=1,
                ),
            ),
            (
                "empty_pin",
                MonitoringState(
                    title=_("State when SMC card PIN is empty"),
                    default_value=1,
                ),
            ),
            (
                "disabled",
                MonitoringState(
                    title=_("State when SMC card PIN is disabled"),
                    default_value=1,
                ),
            ),
            (
                "cert",
                Dictionary(
                    title=_("Check SMC cards certificate expiration"),
                    help=_(
                        "Set these values if you want to monitor the"
                        "certificate expiration of the SMC cards"
                    ),
                    elements=[
                        (
                            "cert_days",
                            Tuple(
                                title=_("Age"),
                                help=_(
                                    "Minimum number of days a certificate"
                                    " has to be valid."
                                ),
                                elements=[
                                    Integer(
                                        title=_("Warning at or below"),
                                        minvalue=0,
                                        unit=_("days"),
                                    ),
                                    Integer(
                                        title=_("Critical at or below"),
                                        minvalue=0,
                                        unit=_("days"),
                                    ),
                                ],
                            ),
                        ),
                    ],
                    required_keys=["cert_days"],
                ),
            ),
        ],
    )


rulespec_registry.register(
    (
        CheckParameterRulespecWithoutItem(
            check_group_name="telematik_card",
            group=RulespecGroupCheckParametersApplications,
            parameter_valuespec=_parameter_valuespec_telematik_konnektor_card,
            title=lambda: _("Telematikinfrastrukur SMC Card")
        )
    )
)
