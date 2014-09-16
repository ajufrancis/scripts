#!/usr/bin/perl
use Net::SNMP;
my $host = '192.168.11.254';
my $community = 'public';
my $in = '1.3.6.1.2.1.31.1.1.1.6.1013';

# 10G interface
my $speed = 18446744073709551616;
# dif_ps    50905842177802200
#my $speed = 10000000000 * 8;
my $speed_oct = $speed / 8;

my $session = Net::SNMP->session(
    -hostname=>$host,
    -version => 'v2c',
    -community => $community
);
my $old_time = undef;
my $old_val = undef;
while (1) {
    my $time = time;
    my $result = $session->get_request(
    -varbindlist => [$in]
    );
#    print "ifHCinOctets=".$result->{$in}."\n";
    if (defined $old_time) {
    my $tick = $time - $old_time;
    my $dif = $result->{$in} - $old_val;
    my $dif_ps = $dif / $tick / 8;
    my $percent = ($dif_ps * 100) / $speed_oct;
    $dif_ps = $dif / (1024 * 1024 * 1024);
    print "tick=$tick; speed=${speed_oct}bytes/s; dif=$dif; dif_ps=${dif_ps}GB/s; percent=${percent}%\n"
    }
    $old_time = $time;
    $old_val = $result->{$in};
    sleep(5);
}
