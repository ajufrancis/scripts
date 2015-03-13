def pprinter(data):
    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(data)

def csv_object(data):
    for entry in data:
        try:
            vm_csv = "OBJECT;VM;{0[instancename]};{0[displayname]};{0[id]}".format(entry)
            print vm_csv
        except:
            pass

def csv_objectip(data):
    for entry in data:
        osif_type = 'regular'
        osif_name = 'eth0'
        try:
            realip = entry['publicip']
        except:
            nics = entry['nic']
            for nic in nics:
                if nic['type'] == 'Shared':
                    realip = nic['ipaddress']
                    break
        
        if len(realip) > 0:
            ip_csv = "OBJECTIP;{0[instancename]};{1};{2};{3}".format(entry, osif_name, realip, osif_type)
            print ip_csv
