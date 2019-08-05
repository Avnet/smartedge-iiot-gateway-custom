cd /usr/bin
./do_iwlist &
sleep 1
sudo -E python -u server.py >/dev/null 2>&1 &
