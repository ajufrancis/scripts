#! /usr/bin/python
"""
Extracts a template
"""
import handleurl.handleurl as hu
import argparse
import pprint
import urllib2
from xml.dom import minidom

if __name__ == "__main__":
    apikey=hu.getenv_apikey()
    secretkey=hu.getenv_secretkey()
    url=hu.getenv_url()

    parser = argparse.ArgumentParser(description="Extracts a template")
 
    parser.add_argument("id",help="the ID of the template")
    parser.add_argument("mode",help="the mode of extraction - HTTP_DOWNLOAD or FTP_UPLOAD")
    parser.add_argument("zoneid",help="the ID of the zone where the ISO is originally located")
    parser.add_argument("--url",dest="url",help="the url to which the ISO would be extracted")

    args = parser.parse_args()

    #Transform args to key=value list
    options = [ "%s=%s" % (key , value) for key, value in vars(args).items() if not value is None]

    command = "extractTemplate"

    formatted_url = hu.format_url(command=command, option_list=options,url=url, apikey=apikey, secretkey=secretkey)

    try:
        response = urllib2.urlopen(formatted_url).read()
        xmldoc = minidom.parseString(response)
        print xmldoc.toprettyxml()
    except Exception, e:
        print 'Error !', e
    
