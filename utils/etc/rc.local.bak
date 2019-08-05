#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi
_cpuid=$(vcgencmd otp_dump | grep 28: | cut -d: -f2)
if [ "$_cpuid" ]; then
  printf "IotGateway %s\n" "$_cpuid"
fi
./usr/bin/create_ID_EK.sh
#above must be done before this script
./usr/bin/ap_setup.sh
./usr/bin/rest.sh &
exit 0
