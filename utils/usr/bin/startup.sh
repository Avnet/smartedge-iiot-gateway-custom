#!/bin/sh
cd /usr/bin
cd IoTConnectSDK_Py2.7_Testing/sample
size=0
zero=0
while true; do
       sudo -E python -u example.py >>/tmp/iot.log 2>&1
done &    

