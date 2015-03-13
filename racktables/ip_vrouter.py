import pprint

def read_ip_vrouter(file):
    lines = []
    with open(file) as fh:
        lines = fh.readlines()

    dict = {}
    name = None
    type = None
    id = None
    entry = {}
    comps = None
    for line in lines:
        line = line.strip('\n')
        comps = line.strip()
        if len(line) == 0:
            continue
        elif comps[0] in ['!', '#']:
            continue
        elif line.startswith('ip vrouter'):
            comps = line.split()
            name = comps[2].strip('"')
            dict[name] = {}
            continue
        elif name:
            comps = line.split()
            if comps[0] in ['snatrule', 'dnatrule']:
                type = comps[0]
                if not dict[name].has_key(type):
                    dict[name][type] = []
                elif type:
                    rule = ' '.join(comps[1:])
                    dict[name][type].append(rule)
                    continue
    return dict
