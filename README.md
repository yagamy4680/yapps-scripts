# yapps-scripts
Yapps Scripts

## System Configuration

The system configuration file `/tmp/yapps.conf.sh` is generated when `yac boot` is invoked from init process. The system configuration file is generated by merging with following 3 files:

| file | purpose | real-path |
|---|---|---|
| `${YAC_DIR}/files/system.conf` | as default configurations that yapps-scripts support | `/opt/yapps-scripts/files/system.conf` |
| `${YS_DIR}/system.conf` | the configurations from yapps-env when building the OS image | `/opt/ys/system.conf` |
| `${PROFILE_CURRENT_DIR}/etc/system.conf` | the configurations from the loaded profile | E.g. `/dhvac/current/etc/system.conf` |

Here are currently supported configurations:

```python
## system configurations (default)
##--------------------------------------------------------


## Initiate ethernet interfaces except `eth0` if any.
#
# For some SBC, there might be more than 1 ethernet interfaces, e.g. USB-Ethernet adapter.
# Then, these extra ethernet interfaces (eth1, eht2, ...) shall be initiated with 
# dhcp client.
#
# [[VALUES]]
#
# `true` : initiate ethernet interfaces except `eth0`
# `false`: skip to initiate extra ethernet interfaces
#
INITIATE_EXTRA_ETHERNET_IFS: "true"


## Restore system time from various sources.
#
# After cool boot, the system time shall be adjusted to global
# time. Here are supported sources to adjust:
#
# [[VALUES]]
#
# `ntp` : using internet time as source to adjust system time.
# `rtc` : using rtc to adjust system time.
# `emmc`: using timestamp file on emmc/sd media to adjust system time.
#
# Please note that, when the restore time source is `ntp` and hardware
# RTC is available, the hardware RTC shall be also adjusted as well.
#
RESTORE_SYSTEM_TIME_WITH_SOURCE: "emmc"
```
