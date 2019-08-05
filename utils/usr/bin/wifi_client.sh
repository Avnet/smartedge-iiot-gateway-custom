#/!bin/sh

#start Station/client mode
./tpm_device_provision <crlf.txt >provisioning.txt
cat provisioning.txt | tr -d "\r\n" | cut -d ':' -f2 | cut -b 1-52 | tr -d "\r\n" >tmp4.txt
cat provisioning.txt | tr -d "\r\n" | cut -d ':' -f2 | cut -b 1-52 | tr -d "\r\n" >deviceid.txt
cat provisioning.txt | tr -d "\r\n" | cut -d ':' -f2 | cut -b 1-424 | tr -d "\r\n" >tmp3.txt
sudo pkill python
sudo cp /etc/rc.local.normal /etc/rc.local
sudo -E python server.py >/dev/null 2>&1 &
sudo ./startup.sh &

