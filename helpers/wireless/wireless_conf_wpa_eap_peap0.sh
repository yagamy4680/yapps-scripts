#!/bin/bash

[ "" == "${SSID}" ] && SSID=$1 && shift
[ "" == "${IDENTITY}" ] && IDENTITY=$1 && shift
[ "" == "${PASSWORD}" ] && PASSWORD=$1 && shift

[ "" == "${SSID}" ] && exit 1
[ "" == "${IDENTITY}" ] && exit 2
[ "" == "${PASSWORD}" ] && exit 3

[ "" == "${WPA_DRIVER}" ] && WPA_DRIVER="wext"

cat <<__EOF__
#
##DRIVER: ${WPA_DRIVER}
#
network={
	auth_alg=OPEN
	proto=WPA2
	pairwise=CCMP
	group=CCMP
	key_mgmt=WPA-EAP
	eap=PEAP
	ssid="${SSID}"
	identity="${IDENTITY}"
	password="${PASSWORD}"

	# ca_cert="/etc/cert/ca.pem"
	
	phase1="peapver=0"
	phase2="auth=MSCHAPV2"
}
__EOF__
