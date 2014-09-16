#!/usr/bin/perl -w
# License: GPL

use netdisco qw/:all/;  
tryuse('SNMP::Info', ver => '1.09', die => 1);

config('/usr/local/netdisco/netdisco.conf');
dbh();

$devices = sql_rows('device', ['*']) ;
my $row;

foreach $row (@$devices) {
	$names{$$row{'ip'}}=(split(/\./,$$row{'name'}))[0];
}

print "# Automatically created by script parents.pl\n\n";
print "all_hosts += [\n";

for $row (@$devices) {
	$hname=(split(/\./,$$row{'name'}))[0];
	$line=" '" . $hname;
	$line.=($$row{'vendor'} eq 'cisco' || $$row{'vendor'} eq 'hp' ) ? "|bulk|" . $$row{'vendor'} : "";
	$line.=($$row{'model'} ne '') ? "|" . $$row{'model'} : "";
	$line.=($$row{'model'} =~ /^8[37]7$/) ? '|adsl-rtr' : "";
	$line.="|net|snmp|netdisco.mk|wato',\n";
	print $line;
}
print "]\n\n";

print "ipaddresses.update({\n";
for my $row (@$devices) {
	$hname=(split(/\./,$$row{'name'}))[0];
        $line=" '" . $hname . "': '" . $$row{'ip'} . "',\n";
        print $line;
}
print "})\n\n";

print "if \'alias\' not in extra_host_conf:\n";
print "    extra_host_conf['alias'] = []\n";

print "extra_host_conf['alias'] += [\n";
for my $row (@$devices) {
        $hname=(split(/\./,$$row{'name'}))[0];
	$hloc=$$row{'location'};
        $line=" ('" . $hloc . "', ['" . $hname . "']),\n";
        if ($hloc ne "") {print $line;};
}
print "]\n\n";

print "parents = [\n";
my %nodes;

sub addnode($$);
sub topdown($$);
	    
topdown "", root_device("172.16.0.248");

# save data sbout a node
sub addnode ($$) {
    my $parent=shift;
    my $node=shift;
    my @subnodes;
    my $tempkeys;

    # Get the subnodes
    $matches = sql_rows('device_port', ['remote_ip'], { 'ip' => $node });
    foreach $element (@$matches)
    {
	$subnode = root_device($$element{'remote_ip'});
        if( defined $subnode and $subnode ne "" and $subnode ne $parent and !defined($nodes{$subnode}))
	{
	    push @subnodes, $subnode;
	}
    }
    $nodes{$node}= [ @subnodes ];
}
    
# the recursive function
# topdown(parent,child)
sub topdown ($$){
    my $parent=shift;
    my $this=shift;
    my $nodechild;

    addnode $parent, $this;
    foreach $nodechild (@{$nodes{$this}}) {
	# dont jump to a node if it already exists
	unless ( defined $nodes{$nodechild} ) {
	    topdown $this, $nodechild;
	}
    }
}

foreach my $node (keys %nodes) {
    if (scalar @{$nodes{$node}}) {
        $line = " ('$names{$node}', [";
        $first=1;
        foreach $nodechild (@{$nodes{$node}}) {
            $line .= ($first ? "" : ", ") . "'" . $names{$nodechild} . "'";
            $first=0;
        }
        print $line . "]),\n";
    }
}
print "]\n\n";

print "if '_WATO' not in extra_service_conf:\n";
print "    extra_service_conf['_WATO'] = []\n";

print "extra_service_conf['_WATO'] += [\n";
print "  ('network.mk', [ 'wato', 'network.mk' ], ALL_HOSTS, [ 'Check_MK inventory' ] ) ]\n";

