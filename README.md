# CheckMK Special Agent for Monitoring a TI Konnektor

## Ensure the remote monitoring is enabled in the Konnektor!

## How to use
- I recommend to set the ipv4 address of the host in checkmk instead of using name resolution
- Create a new "Telematikinfrastruktur Konnektor Agent" rule for your host (Konnektor)
- There, you need one mandant id, clientsystem id and workplace id which is associated to that Konnektor

## What is monitored
- Connected Remote card terminals (Detailed information are available like Firmware, Hardware ...)
- SMC cards in connected remote card terminals, for SMC-B cards the verification state is also monitored
- Operation states of the Konnektor e.g. Update errors, encryption errors, certificate errors ...
- VPN states (VPNSIS, VPNTI)

## WATO rules
- SMC card states can be modified with the rule "Telematikinfrastrukur SMC Card"
- SMC card certificate checks can be configured with the rule "Telematikinfrastrukur SMC Card"
- Operation states can be modified with the rule "Telematikinfrastrukur Operation"


#### The specifications used to develop this plugin are from Gematik and described [here](https://fachportal.gematik.de/fachportal-import/files/gemSpec_Kon_V5.13.0.pdf)
