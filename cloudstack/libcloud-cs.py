#!/usr/bin/env python
import sys
import os
import urlparse
from pprint import pprint
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security as sec
Driver = get_driver(Provider.CLOUDSTACK)
#admin
#        api_key         => 'f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q',
#        secret_key      => '8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g',
#apikey=os.getenv('API_KEY')
#secretkey=os.getenv('SECRET_KEY')
apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
secretkey='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'
#endpoint=os.getenv('ENDPOINT')
endpoint=os.getenv('http://192.168.11.2:8080/client/api')
host=urlparse.urlparse(endpoint).netloc
path=urlparse.urlparse(endpoint).path
#host='192.168.11.2:8080'
#path='/client/api'
conn=Driver(key=apikey,secret=secretkey,secure=True,host=host,path=path)
pprint(driver.list_sizes())
pprint(driver.list_nodes())
