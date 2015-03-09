#!/usr/bin/python
# Data to be defined in main.mk
checks                               = []
static_checks                        = {}
check_parameters                     = []
checkgroup_parameters                = {}
legacy_checks                        = [] # non-WATO variant of legacy checks
active_checks                        = {} # WATO variant for fully formalized checks
custom_checks                        = [] # WATO variant for free-form custom checks without formalization
all_hosts                            = []
host_paths                           = {}
#snmp_hosts                           = [ (['snmp'], ALL_HOSTS) ]
#tcp_hosts                            = [ (['tcp'], ALL_HOSTS), (NEGATE, ['snmp'], ALL_HOSTS), (['!ping'], ALL_HOSTS) ]
bulkwalk_hosts                       = []
snmpv2c_hosts                        = []
usewalk_hosts                        = []
dyndns_hosts                         = [] # use host name as ip address for these hosts
ignored_checktypes                   = [] # exclude from inventory
ignored_services                     = [] # exclude from inventory
ignored_checks                       = [] # exclude from inventory
host_groups                          = []
service_groups                       = []
service_contactgroups                = []
service_notification_periods         = [] # deprecated, will be removed soon.
host_notification_periods            = [] # deprecated, will be removed soon.
host_contactgroups                   = []
parents                              = []
define_hostgroups                    = None
define_servicegroups                 = None
define_contactgroups                 = None
contactgroup_members                 = {}
contacts                             = {}
timeperiods                          = {} # needed for WATO
clusters                             = {}
clustered_services                   = []
clustered_services_of                = {} # new in 1.1.4
datasource_programs                  = []
service_aggregations                 = []
service_dependencies                 = []
non_aggregated_hosts                 = []
aggregate_check_mk                   = False
aggregation_output_format            = "multiline" # new in 1.1.6. Possible also: "multiline"
summary_host_groups                  = []
summary_service_groups               = [] # service groups for aggregated services
summary_service_contactgroups        = [] # service contact groups for aggregated services
summary_host_notification_periods    = []
summary_service_notification_periods = []
ipaddresses                          = {} # mapping from hostname to ipaddress
only_hosts                           = None
distributed_wato_site                = None # used by distributed WATO
extra_host_conf                      = {}
extra_summary_host_conf              = {}
extra_service_conf                   = {}
extra_summary_service_conf           = {}
extra_nagios_conf                    = ""
service_descriptions                 = {}
donation_hosts                       = []
#donation_command                     = 'mail -r checkmk@yoursite.de  -s "Host donation %s" donatehosts@mathias-kettner.de' % check_mk_version
host_attributes                      = {} # needed by WATO, ignored by Check_MK
ping_levels                          = [] # special parameters for host/PING check_command
check_periods                        = []

#################################################
execfile('./treeview_cloudstack.py')
cloud = cloud()
FOLDER_PATH='None'
wato_conf_prefix ='/omd/sites/cloud/etc/check_mk/conf.d/wato/vm'
accounts = cloud.listUsers()
for account in accounts:
    cs_account = account['account']
    request = {'listall': 'true', 'account': cs_account }
    cs_vms = cloud.listVirtualMachines(request)
    wato_hosts_mk = wato_conf_prefix + '/' + cs_account + '/' + 'hosts.mk'
    execfile(wato_hosts_mk)
    
    for vm in cs_vms:
        if not vm['instancename'] in all_hosts:
            host_tags = [ 'lan', 'no_ttl', 'no_osfullname', 'no_devtype', 'no_sla', 'cmk-agent', 'no_cluster', 'up', 'cs_fengce', 'no_pod', 'Running', 'no_zone', 'no_mttf', 'tcp', 'prod', 'tcp_22', 'no_mttr', 'wato' ]
            host_tags = '|'.join(host_tags)
            all_hosts += [ '"{0}|{1}|/" + FOLDER_PATH + "/"'.format(vm['instancename'], host_tags)]
            print all_hosts
    
    #print extra_host_conf.keys()# parents, alias
#    for host in host_attributes.items(): #key by host
#        print host #('i-7-2009-VM', {'alias': u'zijinshan-file-upload', 'tag_state': 'Running', 'tag_port_tcp': 'tcp_3389'})
