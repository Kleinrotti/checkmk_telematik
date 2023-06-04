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
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourcePrograms
from cmk.gui.valuespec import Dictionary, TextAscii, Integer, FixedValue
from cmk.gui.watolib.rulespecs import Rulespec


def _factory_default_special_agents_telematik_konnektor():
    # No default, do not use setting if no rule matches
    return Rulespec.FACTORY_DEFAULT_UNUSED


def _valuespec_special_agents_telematik_konnektor():
    return Dictionary(
        elements=[
            ("mandant",
             TextAscii(
                 title=_("Mandant ID"),
                 allow_empty=False,
             )
             ),
            ("clientsystem",
             TextAscii(
                 title=_("Client system ID"),
                 allow_empty=False,
             )
             ),
            ("workplace",
             TextAscii(
                 title=_("Workplace ID"),
                 allow_empty=False,
             )
             ),
            ("port",
             Integer(
                 title=_("Port"),
                 default_value=443,
             ),
             ),
            ("client_auth",
             Dictionary(
                 title=_("Client authentication (SSL)"),
                 help=_("If your Konnektor is set to force client authentication you can provide "
                        "your client certificate here."),
                 elements=[
                     ("client_cert",
                      TextAscii(
                          title=_("Certificate path"),
                          help=_("Full path to the client certificate."),
                          allow_empty=False,
                      )
                      ),
                     ("client_priv_key",
                      TextAscii(
                          title=_("Private key path"),
                          help=_("Full path to the unecrypted private key."),
                          allow_empty=False,
                      )
                      )
                 ],
                 optional_keys=[],
             ),
             ),
            ("verify_ssl",
             FixedValue(
                 value=True,
                 title=_("Verify SSL certificate"),
                 totext=_("Certificate validation enabled"),
             ),
             ),
        ],
        optional_keys=["client_auth", "verify_ssl"],
        title=_("Telematikinfrastruktur Konnektor Agent"),
        help=_("This rule selects the Telematik Special Agent instead of the normal Check_MK Agent "
               "which collects the data through the Konnektor API."),
    )


rulespec_registry.register(
    (
        HostRulespec(
            factory_default=_factory_default_special_agents_telematik_konnektor(),
            group=RulespecGroupDatasourcePrograms,
            name="special_agents:telematik_konnektor",
            valuespec=_valuespec_special_agents_telematik_konnektor,
        )
    )
)
