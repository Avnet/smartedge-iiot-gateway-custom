#!/bin/bash

if [[ ! -e ./rpiboot ]]; then
  echo "You need to make rpiboot first"
else
  sudo ./rpiboot -s -d avnet/
fi

