#!/usr/bin/env python
import sys
import XenAPI
import pprint

def new_xenapi(server='', username='root', password=''):
    session = XenAPI.Session("https://" + server)
    try:
        session.xenapi.login_with_password(username, password)
    except XenAPI.Failure, e:
        if e.details[0]=='HOST_IS_SLAVE':
            session=XenAPI.Session('https://'+e.details[1])
            session.login_with_password(username, password)
    except:
        print 'could not establish session'
        sys.exit()

    xenapi = session.xenapi
    return xenapi

def get_pools(xenapi):
    pools = xenapi.pool.get_all()
    pool = pools[0]
    print xenapi.pool.get_master(pool)
    print xenapi.pool.get_uuid(pool)
    print xenapi.pool.get_name_label(pool)
    print xenapi.pool.get_default_SR(pool)

def get_hosts(xenapi):
    hosts = xenapi.host.get_all_records()
    return hosts
#    for host in hosts:
#        print xenapi.host.get_name_label(host)
#        print xenapi.host.get_resident_VMs(host)
#        print xenapi.host.get_PIFs(host)
#        print xenapi.host.get_patches(host)
#        print xenapi.host.get_PBDs(host)
#        print xenapi.host.get_host_CPUs(host)
#        print xenapi.host.get_cpu_info(host)
#        print xenapi.host.get_hostname(host)
#        print xenapi.host.get_address(host)
#        print xenapi.host.get_license_params(host)
#        print xenapi.host.get_tags(host)
#        print xenapi.host.get_blobs(host)
#        print xenapi.host.get_edition(host)
#        print xenapi.host.get_bios_strings(host)
#        print xenapi.host.get_PCIs(host)
#        print xenapi.host.get_chip_info(host)

def get_objects(session):
    print xenapi.PIF.get_all()
    print xenapi.network.get_all()

    print xenapi.PBD.get_all()
    print xenapi.SR.get_all()

    print xenapi.host.get_all()
    print xenapi.pool.get_all()

    print xenapi.VDI.get_all()
    print xenapi.VBD.get_all()
    print xenapi.VIF.get_all()
    print xenapi.VM.get_all()
    print xenapi.VM_metrics.get_all()

    print xenapi.SM.get_all()

def logout(xenapi):
    xenapi.session.logout()

def printer(data):
    pp = pprint.PrettyPrinter()
    pp.pprint(data)

xenapi = new_xenapi(server='xstest2', password='Tianren.2011~m')

#get_objects(xenapi)
#get_pools(xenapi)
printer(get_hosts(xenapi))
logout(xenapi)
