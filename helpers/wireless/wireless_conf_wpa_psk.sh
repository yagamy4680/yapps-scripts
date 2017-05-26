#!/bin/bash
#
# Supported: WPA/WPA2
#

[ "" == "${SSID}" ] && SSID=$1 && shift
[ "" == "${PASSWORD}" ] && PASSWORD=$1 && shift

[ "" == "${SSID}" ] && exit 1
[ "" == "${PASSWORD}" ] && exit 3

[ "" == "${WPA_DRIVER}" ] && WPA_DRIVER="wext"
[ "" == "${WPA_AUTH_TIMEOUT}" ] && WPA_AUTH_TIMEOUT="30"

# proto: list of accepted protocols
#	- WPA = WPA/IEEE 802.11i/D3.0
#	- RSN = WPA2/IEEE 802.11i (also WPA2 can be used as an alias for RSN)
#
# key_mgmt: list of accepted authenticated key management protocols
#	- WPA-PSK = WPA pre-shared key (this requires 'psk' field)
#	- WPA-EAP = WPA using EAP authentication (this can use an external program, e.g., Xsupplicant, for IEEE 802.1X EAP Authentication
#	- IEEE8021X = IEEE 802.1X using EAP authentication and (optionally) dynamically generated WEP keys
#	- NONE = WPA is not used; plaintext or static WEP could be used
#

cat <<__EOF__
#
##DRIVER: ${WPA_DRIVER}
##AUTH_TIMEOUT: ${WPA_AUTH_TIMEOUT}
#
network={
	auth_alg=OPEN
	proto=WPA RSN
	key_mgmt=WPA-PSK
	ssid="${SSID}"
	psk="${PASSWORD}"
}
__EOF__
