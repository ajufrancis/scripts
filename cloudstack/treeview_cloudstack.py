#!/usr/bin/python
import CloudStack
import os, sys, re
import json

class cloud:
    def __init__(self):
        self.url = 'http://csm01:8080/client/api'
        #admin
        self.apikey = 'f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
        self.secret = '8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'
        self.api = CloudStack.Client(self.url, self.apikey, self.secret)
        self.schema = self.listDomains()

    def listAccounts(self):
      domains = self.api.listDomains()
      accounts = [ ]
      for domain in domains:
        request = {
            'listall': 'true',
            'domainid': domain['id']
        }
        accounts += self.api.listAccounts(request)

      return accounts
    
    def listUsers(self):
      domains = self.api.listDomains()

      users = [ ]
      for domain in domains:
        request = {
        'domainid': domain['id']
        }
        users += self.api.listUsers(request)

      return users
    
    def listDomains(self, name=''):
        if name == '':
            name = 'ROOT'

        request = {
            'listall': 'true',
            'name': name
        }
        domains = self.api.listDomains(request)
        DOMAIN = {}
        for domain in domains:
            domain['zones'] = self.listZones(domain)
            key = domain['name']
            DOMAIN[key] = domain
        return DOMAIN

    def listDomainChildren(self):
        request = {
        'listall':'true'
        }
        return self.api.listDomainChildren(request)
    
    def listResourceLimits(self):
        request = {
        'listall':'true'
        }
        return self.api.listResourceLimits(request)
    
    def listVirtualMachines(self, request):
        VM = {}
        vms = self.api.listVirtualMachines(request)
        for vm in vms:
            VM[vm['instancename']] = vm
        return VM
    
    def listSnapshots(self):
        request = {
        'listall':'true'
        }
        return self.api.listSnapshots(request)
    
    def listTemplates(self):
        request = {
        'listall':'true'
        }
        return self.api.listTemplates(request)
    
    def listIsos(self):
        request = {
        'listall':'true'
        }
        return self.api.listIsos(request)
    
    def listOsTypes(self):
        request = {
        'listall':'true'
        }
        return self.api.listOsTypes(request)
    
    def listOsCategories(self):
        request = {
        'listall':'true'
        }
        return self.api.listOsCategories(request)
    
    def listServiceOfferings(self):
        request = {
        'listall':'true'
        }
        return self.api.listServiceOfferings(request)
    
    def listDiskOfferings(self):
        request = {
        'listall':'true'
        }
        return self.api.listDiskOfferings(request)
    
    def listVlanIpRanges(self):
        request = {
        'listall':'true'
        }
        return self.api.listVlanIpRanges(request)
    
    def listPublicIpAddresses(self):
        request = {
        'listall':'true'
        }
        return self.api.listPublicIpAddresses(request)
    
    def listPortForwardingRules(self):
        request = {
        'listall':'true'
        }
        return self.api.listPortForwardingRules(request)
    
    def listIpForwardingRules(self):
        request = {
        'listall':'true'
        }
        return self.api.listIpForwardingRules(request)
    
    def listLoadBalancerRules(self):
        request = {
        'listall':'true'
        }
        return self.api.listLoadBalancerRules(request)
    
    def listLBStickinessPolicies(self):
        request = {
        'listall':'true'
        }
        return self.api.listLBStickinessPolicies(request)
    
    def listLoadBalancerRuleInstances(self):
        request = {
        'listall':'true'
        }
        return self.api.listLoadBalancerRuleInstances(request)
    
    def listRouters(self):
        request = {
        'listall':'true'
        }
        return self.api.listRouters(request)
    
    def listSystemVms(self):
        request = {
        'listall':'true'
        }
        return self.api.listSystemVms(request)
    
    def listConfigurations(self):
        request = {
        'listall':'true'
        }
        return self.api.listConfigurations(request)
    
    def listCapabilities(self):
        request = {
        'listall':'true'
        }
        return self.api.listCapabilities(request)
    
    def listPods(self,zone):
        POD = {}
        request = {
            'zoneid': zone['id']
        }
        pods = self.api.listPods(request)
        for pod in pods:
            pod['clusters'] = self.listClusters(pod)
            key = pod['name']
            POD[key] = pod
        return POD
    
    def listZones(self,domain):
        request = {
            'listall':'true',
            'domainid': domain['id']
        }
        zones = self.api.listZones(request)
        ZONE = {}
        for zone in zones:
            zone['pods'] = self.listPods(zone)
            key = zone['name']
            ZONE[key] = zone
        return ZONE
    
    def listEvents(self):
        request = {
        'listall':'true'
        }
        return self.api.listEvents(request)
    
    def listEventTypes(self):
        request = {
        'listall':'true'
        }
        return self.api.listEventTypes(request)
    
    def listAlerts(self):
        request = {
        'listall':'true'
        }
        return self.api.listAlerts(request)
    
    def listCapacity(self):
        request = {
        'listall':'true'
        }
        return self.api.listCapacity(request)
    
    def listSwifts(self):
        request = {
        'listall':'true'
        }
        return self.api.listSwifts(request)
    
    def listHosts(self,cluster):
        HOST = {}
        request = {
            'clusterid': cluster['id']
        }
        hosts = self.api.listHosts(request)
        request = {'listall': 'true'}
        for host in hosts:
            request['hostid'] = host['id']
            host['vms'] = self.listVirtualMachines(request)
            HOST[host['name']] = host
        return HOST
    
    def listVolumes(self):
        request = {
        'listall':'true'
        }
        return self.api.listVolumes(request)
    
    def listAsyncJobs(self):
        request = {
        'listall':'true'
        }
        return self.api.listAsyncJobs(request)
    
    def listStoragePools(self):
        request = {
        'listall':'true'
        }
        return self.api.listStoragePools(request)
    
    def listClusters(self,pod):
        CLUSTER = {}
        request = {
           'podid': pod['id']
        }
        clusters = self.api.listClusters(request)
        for cluster in clusters:
            cluster['hosts'] = self.listHosts(cluster)
            CLUSTER[cluster['name']] = cluster
        return CLUSTER
    
    def listSecurityGroups(self):
        request = {
        'listall':'true'
        }
        return self.api.listSecurityGroups(request)
    
    def listInstanceGroups(self):
        request = {
        'listall':'true'
        }
        return self.api.listInstanceGroups(request)
    
    def listHypervisors(self):
        request = {
        'listall':'true'
        }
        return self.api.listHypervisors(request)
    
    def listRemoteAccessVpns(self):
        request = {
        'listall':'true'
        }
        return self.api.listRemoteAccessVpns(request)
    
    def listVpnUsers(self):
        request = {
        'listall':'true'
        }
        return self.api.listVpnUsers(request)
    
    def listNetworkOfferings(self):
        request = {
        'listall':'true'
        }
        return self.api.listNetworkOfferings(request)
    
    def listNetworks(self):
        request = {
        'listall':'true'
        }
        return self.api.listNetworks(request)
    
    def listSSHKeyPairs(self):
        request = {
        'listall':'true'
        }
        return self.api.listSSHKeyPairs(request)
    
    def listProjects(self):
        request = {
        'listall':'true'
        }
        return self.api.listProjects(request)
    
    def listProjectAccounts(domain):
        request = {
        'domainid': domain['id']
        }
        return self.api.listProjectAccounts(request)
    
    def listProjectInvitations(self):
        request = {
        'listall':'true'
        }
        return self.api.listProjectInvitations(request)
    
    def listFirewallRules(self):
        request = {
        'listall':'true'
        }
        return self.api.listFirewallRules(request)
    
    def listHypervisorCapabilities(self):
        request = {
        'listall':'true'
        }
        return self.api.listHypervisorCapabilities(request)
    
    def listPhysicalNetworks(self):
        request = {
        'listall':'true'
        }
        return self.api.listPhysicalNetworks(request)
    
    def listSupportedNetworkServices(self):
        request = {
        'listall':'true'
        }
        return self.api.listSupportedNetworkServices(request)
    
    def listNetworkServiceProviders(self):
        request = {
        'listall':'true'
        }
        return self.api.listNetworkServiceProviders(request)
    
    def listTrafficTypes(self):
        request = {
        'listall':'true'
        }
        return self.api.listTrafficTypes(request)
    
    def listTrafficTypeImplementors(self):
        request = {
        'listall':'true'
        }
        return self.api.listTrafficTypeImplementors(request)
    
    def listStorageNetworkIpRange(self):
        request = {
        'listall':'true'
        }
        return self.api.listStorageNetworkIpRange(request)
    
    def listNetworkDevice(self):
        request = {
        'listall':'true'
        }
        return self.api.listNetworkDevice(request)
    
def get_vms_record():
    accounts = cloud.listUsers()
    for account in accounts:
        name = account['account']
        print '{0:#^20}'.format(name)
        request = {'listall': '', 'account': 'fengce' }
        vms = cloud.api.listVirtualMachines(request)
        for vm in vms:
            if vm['state'] =='Running':
                try:
                    ip = vm['publicip']
                except:
                    for network in vm['nic']:
                        if network['type'] == 'Shared':
                            ip = network['ipaddress']

                print '{0} {1}'.format(ip, vm['instancename'])

cloud = cloud()
get_vms_record()
