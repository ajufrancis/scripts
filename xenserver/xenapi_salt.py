#!/usr/bin/python
import sys
import XenAPI
import pprint

#http://docs.vmd.citrix.com/XenServer/6.2.0/1.0/en_gb/
class XE:
    def __init__(self, url='', password='', username='root'):
        self.username = username
        self.password = password

        if url == '' or password == '':
            self.s = XenAPI.xapi_local()
        else:
            self.s = XenAPI.Session(url)

    def make_session(self):
        self.s.xenapi.login_with_password(username, password)

    def vm_list(self, args={}):
        vm_records = []

        if len(args) == 0:
            try:
                vms = self.s.xenapi.VM.get_all()
                for vm in vms:
                    record = self.s.xenapi.VM.get_record(vm)
                    if not(record["is_a_template"]) and not(record["is_control_domain"]) and (record["power_state"] == "Running"):
                        vm_records += [ record ]

            finally:
                self.s.xenapi.session.logout()

        return vm_records


if __name__ == "__main__":
    xe = XE()
    vms = xe.vm_list()
    pp = pprint.PrettyPrinter()
    pp.pprint(vms)

