#!/usr/bin/python

cs_objects = [
    'Accounts',
    'Users',
    'Domains',
    'DomainChildren',
    'ResourceLimits',
    'VirtualMachines',
    'Snapshots',
    'Templates',
    'Isos',
    'OsTypes',
    'OsCategories',
    'ServiceOfferings',
    'DiskOfferings',
    'VlanIpRanges',
    'PublicIpAddresses',
    'PortForwardingRules',
    'IpForwardingRules',
    'LoadBalancerRules',
    'LBStickinessPolicies',
    'LoadBalancerRuleInstances',
    'Routers',
    'SystemVms',
    'Configurations',
    'Capabilities',
    'Pods',
    'Zones',
    'Events',
    'EventTypes',
    'Alerts',
    'Capacity',
    'Swifts',
    'Hosts',
    'Volumes',
    'AsyncJobs',
    'StoragePools',
    'Clusters',
    'SecurityGroups',
    'InstanceGroups',
    'Hypervisors',
    'RemoteAccessVpns',
    'VpnUsers',
    'NetworkOfferings',
    'Networks',
    'SSHKeyPairs',
    'Projects',
    'ProjectAccounts',
    'ProjectInvitations',
    'FirewallRules',
    'HypervisorCapabilities',
    'PhysicalNetworks',
    'SupportedNetworkServices',
    'NetworkServiceProviders',
    'TrafficTypes',
    'TrafficTypeImplementors',
    'StorageNetworkIpRange',
    'NetworkDevice'
]

for obj in cs_objects:
    print "def list" + obj + "():"
    print "    request = {"
    print "    'listall':'true'"
    print "    }"
    print "    return api.list" + obj + "VirtualMachines(request)"
    print ""
