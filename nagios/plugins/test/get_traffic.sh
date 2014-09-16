#!/usr/bin/perl -w
use Net::SNMP;
use Net::SNMP::Interfaces;

main:
{

my $session;
my $hostname = '192.168.11.254';
my $community = 'snmp4gdcloud.com';
my $error;
my $oid = '1.3.6.1.4.1.6486.801.1.2.1.5.1.1.2.2.1.10.1013';
my $result;

# RETRIEVING INTERFACES
my $interfaces = Net::SNMP::Interfaces->new(Hostname => $hostname, Community => $community);
my  @ifnames = $interfaces->all_interfaces();
foreach $interface (@ifnames) {
    my $name = $interface->name();
#    print "$name\n";    
}

# SNMP SESSION OPEN
($session, $error) = Net::SNMP->session(-hostname => $hostname, -community => $community);
print "SESSION ID: $session\n";
if (!defined $session) {
    print "!!!SESSION ERROR: $error\n";
    $session->close();
    exit(1);
}

# SNMP GET_REQUEST  
#xxxxxxxxxxxxxxxxxxxxxxx
$result = $session->get_request(-varbindlist => [ $oid ]);
if (!defined $result) {
    $error = $session->error();
    print "GET_REQUEST ERROR: $error\n";
    $session->close();
    exit(1);
}

$result = $result->{$oid};
print "!!!GET_REQUEST: $result\n";

# SNMP SESSION CLOSE
$session->close();
exit(0);

}
