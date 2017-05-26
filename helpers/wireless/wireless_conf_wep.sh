#!/bin/bash
#
# Supported: WEP 64-bit key and 128-bit key.
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
# auth_alg: list of allowed IEEE 802.11 authentication algorithms
#	- OPEN = Open System authentication (required for WPA/WPA2)
#	- SHARED = Shared Key authentication (requires static WEP keys)
#	- LEAP = LEAP/Network EAP (only used with LEAP)
#
# group: list of accepted group (broadcast/multicast) ciphers for WPA
#	- CCMP = AES in Counter mode with CBC-MAC [RFC 3610, IEEE 802.11i/D7.0]
#	- TKIP = Temporal Key Integrity Protocol [IEEE 802.11i/D7.0]
#	- WEP104 = WEP (Wired Equivalent Privacy) with 104-bit key
#	- WEP40 = WEP (Wired Equivalent Privacy) with 40-bit key [IEEE 802.11]
#
# WEP40 equals to WEP 64-bit key  :  40 bits as key while 24 bits as initialization vector
# WEP104 equals to WEP 128-bit key: 104 bits as key while 24 bits as initialization vector 
#


cat <<__EOF__
#
##DRIVER: ${WPA_DRIVER}
##AUTH_TIMEOUT: ${WPA_AUTH_TIMEOUT}
#
network={
	auth_alg=SHARED
	key_mgmt=NONE
	group=WEP104 WEP40
	ssid="${SSID}"
	wep_key0="${PASSWORD}"
}
__EOF__
