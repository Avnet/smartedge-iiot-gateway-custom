#!/bin/sh
cat /usr/bin/IoTConnectSDK_Py2.7_Testing/sample/cpid1.txt |cut -d ':' -f2| cut -d '}' -f1 | tr -d "\"" |tr -d "{"|tr -d "\r\n" >/usr/bin/IoTConnectSDK_Py2.7_Testing/sample/cpid.txt
file=/tmp/iotconnect.txt
if test -f $file; then
    echo "SDK not running"
else
    sudo pkill startup
    sudo pkill example
    sudo ./startup.sh
fi

