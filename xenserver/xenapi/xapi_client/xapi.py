import XenAPI
import sys

class Session:
    def __init__(self):
        self.sess = XenAPI.xapi_local()

    def login(self):
        try:
            self.sess.login_with_password('', '')
       
            this_record = self.sess.xenapi.session.get_this_host(self.sess._session)
            this_host = self.sess.xenapi.host.get_record(this_record)
            self.this_host = this_host
        except Exception, e:
            sys.exit("Error: %s" % str(e))

    def logout(self):
        self.sess.logout()
