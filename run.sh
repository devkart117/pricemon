Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
cd /home/kartik/Dev/pricemon/
rm capture-log.txt
exec &>> capture-log.txt
./script.py
