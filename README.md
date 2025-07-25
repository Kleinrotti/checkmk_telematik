# CheckMK Special Agent - Monitor a TI Konnektor

## Preamble
This plugin was developed without a "real" SOAP client. Therefore, it is a little bit hacky and if a new WSDL version is available, it has to be adapted in the source code.
The advantage is that the plugin works immediately and no further Python packages like zeep need to be installed.
As this plugin is only meant for simple monitoring purposes, I went this way.
Maybe I will rewrite it in the future, when it is no longer necessary to manually download the WSDL files from the Gematik github and the connector provides them itself instead.

## Check these requirements:
- If client side authentication is enabled in the Konnektor, you have to provide the certificate or credentials in the WATO rule
- The special agent is developed with the WSDL version 7.2 from the EventService and 8.1 from the CardService, if your Konnektor has an older version this will likely not work

## How to use
- I recommend to set the IPv4 address of the host in checkmk instead of using name resolution
- Create a new "Telematikinfrastruktur Konnektor Agent" rule for your host (Konnektor)
- There, you need one mandant id, clientsystem id and workplace id which is associated to that Konnektor

## What is monitored
- Connected Remote card terminals (Detailed information are available like Firmware, Hardware, Workplaces ...)
- All assosciated cards and terminals for that mandant if mandant-wide request is enabled in the WATO rule
- SMC cards in connected remote card terminals, for SMC-B cards the verification state is also monitored
- Operation states of the Konnektor e.g. Update errors, encryption errors, certificate errors ...
- VPN states (VPNSIS, VPNTI)

## WATO rules
- SMC card states can be modified with the rule "Telematikinfrastrukur SMC Card"
- SMC card certificate checks can be configured with the rule "Telematikinfrastrukur SMC Card"
- Operation states can be modified with the rule "Telematikinfrastrukur Operation"
- Connected states from terminals can be modified with the rule "Telematikinfrastrukur Terminal"

## Debugging
The special agent provides a debug mode which you can use to debug errors. Run the special agent from the command line with the additional parameter --debug.

#### The specifications used to develop this plugin are from Gematik and described [here](https://gemspec.gematik.de/docs/gemSpec/gemSpec_Kon/gemSpec_Kon_V5.13.0/)
