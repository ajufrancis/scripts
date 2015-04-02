#!/usr/bin/env python

# Author: Will Stevens - wstevens@cloudops.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib
import urllib2
import hmac
import hashlib
import base64
import pprint
import requests

class CloudstackAPI(object):
    """
    Login and run queries against the Cloudstack API.
    Example Usage: 
    cs_api = CloudstackAPI(api_key='api_key', secret_key='secret_key'))
    accounts = cs_api.request(dict({'command':'listAccounts'}))
    
    """
    
    def __init__(self, protocol='http', host='127.0.0.1:8080', uri='/client/api', api_key=None, secret_key=None, logging=True):        
        self.protocol = protocol
        self.host = host
        self.uri = uri
        self.api_key = api_key
        self.secret_key = secret_key
        self.errors = []
        self.logging = logging
        
    def request(self, params):
        """Builds a query from params and return a json object of the result or None"""
        if self.api_key and self.secret_key:
            # add the default and dynamic params
            params['response'] = 'json'
            params['apiKey'] = self.api_key

            # build the query string
            query_params = map(lambda (k,v):k+"="+urllib.quote(str(v)), params.items())
            query_string = "&".join(query_params)
            
            # build signature
            query_params.sort()
            signature_string = "&".join(query_params).lower()
            signature = urllib.quote(base64.b64encode(hmac.new(self.secret_key, signature_string, hashlib.sha1).digest()))

            # final query string...

            output = None
            url = self.protocol+"://"+self.host+self.uri+"?"+query_string+"&signature="+signature
            try:
                response = requests.get(url)
                output = response.json()
            except Exception, e:
                self.errors.append("Error: "+str(e.code))

            if output:
                output = output[(params['command']).lower()+'response']
            
            if self.logging:
                with open('request.log', 'a') as f:
                    f.write('request:\n')
                    f.write(url)
                    f.write('\n\n')
                    f.write('response:\n')
                    if output:
                        pprint.pprint(output, f, 2)
                    else:
                        f.write(repr(self.errors))
                    f.write('\n\n\n\n')
            
            # if the request was an async call, then poll for the result...
            if output and 'jobid' in output.keys() and \
                    ('jobstatus' not in output.keys() or ('jobstatus' in output.keys() and output['jobstatus'] == 0)):
                print 'polling...'
                time.sleep(self.async_poll_interval)
                output = self.request(dict({'command':'queryAsyncJobResult', 'jobId':output['jobid']}))

            return output
        else:
            self.errors.append("missing api_key and secret_key in the constructor")
            return None
            
            
if __name__ == "__main__":
    # comment out the following line to keep a history of the requests over multiple runs (request.log will get big).
    open('request.log', 'w').close() # cleans the 'request.log' before execution so it only includes this run.

    host = 'csm01:8080'
    api_key = 'f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
    secret_key = '8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'


    cs_api = CloudstackAPI(host=host, api_key=api_key, secret_key=secret_key)
    cs_api.request(dict({'command':'listUsers'}))
