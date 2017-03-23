#!/bin/bash
#

[ "" == "${SSID}" ] && SSID=$1 && shift
[ "" == "${SSID}" ] && exit 1
[ "" == "${WPA_DRIVER}" ] && WPA_DRIVER="wext"

# Plaintext connection (no WPA, no IEEE 802.1X)
#
cat <<__EOF__
#
##DRIVER: ${WPA_DRIVER}
#
network={
	ssid="${SSID}"
	key_mgmt=NONE
}
__EOF__
