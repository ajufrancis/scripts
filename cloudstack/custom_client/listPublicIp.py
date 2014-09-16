#!/usr/bin/python

import CloudStack

api = 'http://192.168.11.2:8080/client/api'
#admin
apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'

#ruanjianyanfa
#apikey='Oe_0BsOGH6vbbqrvtGeq9pW3RRwKrNoBMxxAydlfKxgKrd1sIZE0SmUOQaYJ9ck_eO1eZpDsi5q2_ZlrrYVmKw'
#secret='GtIJxaJ6-8A1C6Y84uThak2BBw7jEP1BzC-fOFuvdVFHbHRpUeMWlkTIde3_hgyAp6YBE1By1LYk7qXbYg2pxw'

#erp
#apikey='wq0WjZduVlbxkVS4kw4pgT0h3tYOb-f03jD-0QAJ6YDsxv1CK5tyqwxFLcnPJLqs_X7Al_Ug0W_-R6jZWg4bJQ'
#secret='Aq__RSVBrCLkfik5bVj9pbGemP4iFWXmYXqy4Yqxi5VQY8qa7syuzmbke7G_LSTt0n4eM2ckOgu7M0vEm8SwPA'

#gdupc
#apikey='SZNoworaz5-hnX-b1RYjqbw5RCmJVF8BKSTj1XHqhMqR9K81mECXvmlfyjOd83NrGlQ9s0DVgZDt-y_vleWNtA'
#secret='f2Ng3w5epP5Dzla6t6L0dsral4x06I-OSrkkuIAGn502DHB3cuzKcJ8Mz7fJGu04tDVNdYRkB92KUOG3pjzrxw'

#fengce
#apikey='WtmzgK3xC2lN8Bi4-cfXCEXdWMZ_hXK23LefYqpbaBrYbG20GgzAd9p1rOjInIa-M0HYP89BUZ0JFzTisbhu-A'
#secret='8TTcgOkz9qL3OX7DDlTTalLOeK_vFXoRRuIrVxLpUku7WU9mEDAKAl9-6Li3FLBRQYHCEsa0L9-0WV8Bj9_9Uw'

cs_object = CloudStack.Client(api, apikey, secret)

vms = cs_object.listPublicIpAddresses({ 'listall':'true' })

for x in vms:
  print x
