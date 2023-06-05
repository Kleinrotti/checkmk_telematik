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


def _parameter_valuespec_telematik_konnektor_operation():
    return Dictionary(
        elements=[
            (
                "fatal",
                MonitoringState(
                    title=_("Severity Fatal"),
                    default_value=2,
                )
            ),
            (
                "error",
                MonitoringState(
                    title=_("Severity Error"),
                    default_value=2,
                ),
            ),
            (
                "warning",
                MonitoringState(
                    title=_("Severity Warning"),
                    default_value=1,
                ),
            ),
            (
                "info",
                MonitoringState(
                    title=_("Severity Info"),
                    default_value=1,
                ),
            ),
        ],
    )


rulespec_registry.register(
    (
        CheckParameterRulespecWithoutItem(
            check_group_name="telematik_operation",
            group=RulespecGroupCheckParametersApplications,
            parameter_valuespec=_parameter_valuespec_telematik_konnektor_operation,
            title=lambda: _("Telematikinfrastrukur Operation")
        )
    )
)
