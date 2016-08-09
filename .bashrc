
function setup_prompt_yac {
	local CONFIG=$1
	# local BOARD_PROFILE=$(cat ${CONFIG} | grep -P "^profile\t" | awk '{print $2}')
	local BOARD_PROFILE_ENV=$(cat ${CONFIG} | grep -P "^profile_env\t" | awk '{print $2}')
	local BOARD_PROFILE_VERSION=$(cat ${CONFIG} | grep -P "^profile_version\t" | awk '{print $2}')
	local BOARD_SERIAL_NUMBER=$(cat ${CONFIG} | grep -P "^sn\t" | awk '{print $2}')
	export PS1="${BOARD_SERIAL_NUMBER} \[\e[36m\]${BOARD_PROFILE_ENV}\[\e[m\]#\[\e[35m\]${BOARD_PROFILE_VERSION}\[\e[m\] ${PS1}"
}

[ -f "/tmp/ttt_system" ] && setup_prompt_yac "/tmp/ttt_system"
