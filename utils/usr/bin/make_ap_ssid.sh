cat /proc/cpuinfo | grep Serial | cut -d ':' -f2 | tr -d "\r\n" | tr -d " " >tmp0.txt
echo "ssid=IoTGatewayDevice" | tr -d "\r\n" >tmp1.txt
cat /etc/hostapd/hostapd.ap tmp1.txt tmp0.txt >/etc/hostapd/hostapd.conf
 
