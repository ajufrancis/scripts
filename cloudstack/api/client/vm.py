def list(cs, params={}):
    params.update({'listall': 'true'})
    vms = cs.listVirtualMachines(params)
    return vms
