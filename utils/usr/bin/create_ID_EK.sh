cd /usr/bin
sudo ./tpm_device_provision <crlf.txt >provisioning.txt
sudo cat provisioning.txt | tr -d "\r\n" | cut -d ':' -f2 | cut -b 1-52 | tr -d "\r\n" >tmp4.txt
sudo cat provisioning.txt | tr -d "\r\n" | cut -d ':' -f2 | cut -b 1-52 | tr -d "\r\n" >deviceid.txt
sudo cat provisioning.txt | tr -d "\r\n" | cut -d ':' -f3 | cut -b 1-424 | tr -d "\r\n" >tmp3.txt
cat /proc/cpuinfo | grep Serial | cut -d ':' -f2 | cut -b 10-17 | tr -d "\r\n" | tr -d " " >tmp0.txt
cat hostapd.conf tmp0.txt >/etc/hostapd/hostapd.conf
