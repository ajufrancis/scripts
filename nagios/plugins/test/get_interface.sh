#!/usr/bin/perl -w
use Net::SNMP;
use Net::SNMP::Interfaces;

my $session;
my $hostname = '192.168.11.254';
my $community = 'snmp4gdcloud.com';
my $error;
my $oid = '';
my $result;

# RETRIEVING INTERFACES
my $interfaces = Net::SNMP::Interfaces->new(Hostname => $hostname, Community => $community);
my  @ifnames = $interfaces->all_interfaces();
foreach $interface (@ifnames) {
    my $name = $interface->name();
    print "$name\n";    
}
