def get_grains_core():
    import salt.client

    local = salt.client.LocalClient()
    ret = local.cmd('xsm01', 'grains.item', ['os'])
    return ret

print get_grains_core()
