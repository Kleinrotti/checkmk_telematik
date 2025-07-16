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

from collections.abc import Iterator
from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


class Params(BaseModel):
    """Params validator"""
    port: int | None = None
    mandant: str | None = None
    clientsystem: str | None = None
    workplace: str | None = None
    verify_ssl: bool | None = None
    client_auth: tuple[str, dict] | None = None
    mandant_wide: bool | None = None


def _agent_telematik_konnektor_arguments(
    params: Params, host_config: HostConfig
) -> Iterator[SpecialAgentCommand]:
    command_arguments: list[str | Secret] = []
    command_arguments += ["-u", host_config.primary_ip_config.address or host_config.name]
    command_arguments += ["-p", str(params.port)]
    command_arguments += ["-m", params.mandant]
    command_arguments += ["-c", params.clientsystem]
    command_arguments += ["-w", params.workplace]
    if params.verify_ssl:
        command_arguments += ["--ssl_verify"]
    if params.client_auth:
        if "cert_auth" in params.client_auth:
            command_arguments += ['-cert', params.client_auth[1]["client_cert"]]
            command_arguments += ['-certkey', params.client_auth[1]["client_priv_key"]]
        elif "basic_auth" in params.client_auth:
            command_arguments += ['-username', params.client_auth[1]["username"]]
            command_arguments += ['-password', params.client_auth[1]["password"].unsafe()]
    if params.mandant_wide:
        command_arguments += ["--mandant_wide"]
    yield SpecialAgentCommand(command_arguments=command_arguments)


special_agent_telematik_konnektor = SpecialAgentConfig(
    name="telematik_konnektor",
    parameter_parser=Params.model_validate,
    commands_function=_agent_telematik_konnektor_arguments,
)
