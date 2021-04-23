https://stackoverflow.com/questions/23908319/run-selenium-with-crontab-python

Cron line:
```sh
0 */1 * * * perl -le 'sleep rand 600' && DISPLAY=:0 /usr/bin/python3 /home/pi/anais-bus/anais_bus.py >> /home/pi/anais-bus/stdout.log 2>> /home/pi/anais-bus/error.log
```
