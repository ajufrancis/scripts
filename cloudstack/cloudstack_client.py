#!/usr/bin/python
# coding: UTF-8
import CloudStack

def api():
  api = 'http://csm01:8080/client/api'
  #admin
  apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
  secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'
  api = CloudStack.Client(api, apikey, secret)
  return api
