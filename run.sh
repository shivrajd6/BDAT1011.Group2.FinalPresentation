#!/bin/bash

cd '/home/shivd/studies/georgian/business_processes';
source venv/bin/activate;
python twitter-sentiment-analysis-process.py;
#sleep 30;
#rsync -azP -e "ssh -i /var/www/keys/tempdroplet/secure" /home/shivd/studies/georgian/business_processes/files/results/ recursing-thompson_q9unqmpm99l@recursing-thompson.146-190-252-85.plesk.page:/var/www/vhosts/recursing-thompson.146-190-252-85.plesk.page/httpdocs/files/
