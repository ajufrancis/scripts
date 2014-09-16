#!/bin/bash
sosreport --build --batch --tmp-dir=/var/www/html/sosreport/ --report
chmod -R a+r /var/www/html/sosreport
chmod a+x /var/www/html/sosreport/*
