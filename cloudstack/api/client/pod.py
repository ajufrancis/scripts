def list(cs, params={}):
    pods = cs.listPods(params)
    return pods
