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
from cmk.gui.valuespec import Dictionary, MonitoringState


def _parameter_valuespec_telematik_konnektor_terminal():
    return Dictionary(
        elements=[
            (
                "false",
                MonitoringState(
                    title=_("Status not connected"),
                    default_value=1,
                )
            ),
            (
                "true",
                MonitoringState(
                    title=_("Status connected"),
                    default_value=0,
                )
            )
        ]
    )


rulespec_registry.register(
    (
        CheckParameterRulespecWithoutItem(
            check_group_name="telematik_terminal",
            group=RulespecGroupCheckParametersApplications,
            parameter_valuespec=_parameter_valuespec_telematik_konnektor_terminal,
            title=lambda: _("Telematikinfrastrukur Terminal")
        )
    )
)
