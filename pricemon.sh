#!/bin/bash
cd /home/asyncxeno/Dev/price-monitoring/
rm capture-log.txt
exec &>> capture-log.txt
./script.py