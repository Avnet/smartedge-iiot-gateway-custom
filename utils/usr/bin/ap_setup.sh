#!/bin/sh
sudo systemctl enable hostapd.service
sudo systemctl enable dnsmasq.service
sudo systemctl start hostapd.service
sudo systemctl start dnsmasq.service

