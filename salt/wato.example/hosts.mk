# Written by WATO
# encoding: utf-8

all_hosts += [
    "i-21-1887-VM|lan|no_ttl|no_osfullname|tcp_none|no_devtype|no_sla|ping|no_cluster|up|no_pod|Running|no_zone|no_mttf|cs_test|prod|no_mttr|wato|/" + FOLDER_PATH + "/",
]


# Settings for alias
extra_host_conf.setdefault('alias', []).extend(
    [(u'wxp3-1', ['i-21-1896-VM'])]
)

# Settings for parents
extra_host_conf.setdefault('parents', []).extend(
    [('access-sw01,access-sw02', ['i-21-2015-VM'])]
)

# Settings for contatgroups
host_contactgroups.append(
    ( ['test'], [ '/' + FOLDER_PATH + '/' ], ALL_HOSTS )
)

# Settings for ipaddress
ipaddresses.update(
   {'localpred-03': u'10.24.64.14'}
)

# Host attributes (needed for WATO)
host_attributes.update(
{
    'i-21-2015-VM': {
        'alias': u'test01',
        'tag_state': 'Running'
    }
}
)
