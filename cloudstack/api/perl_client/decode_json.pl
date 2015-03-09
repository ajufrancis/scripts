#!/usr/bin/perl
#use Encode;
use JSON;
use Data::Dumper;
use utf8;
binmode(STDIN, ':encoding(utf8)');
binmode(STDOUT, ':encoding(utf8)');
binmode(STDERR, ':encoding(utf8)');

my $json = new JSON;
my $json = JSON->new->utf8;

my $json_obj;
my $data;

if(open(MYFILE, "listVMs_all.log")) 
{
  while(<MYFILE>) 
  {
    $data .= "$_";
  }
}
else
{
  print "fail\n";
}

$json_obj = $json->decode($data);
my $count = $json_obj->{'listvirtualmachinesresponse'}->{'count'};
my $vms = $json_obj->{'listvirtualmachinesresponse'}->{'virtualmachine'};
#print Dumper($json_obj->{'listvirtualmachinesresponse'}->{'virtualmachine'}[0]);

print "id,instancename,name,state,haenable,created,cpunumber,cpuspeed,memory,rootdeviceid,rootdeivcetype,serviceofferingid,serviceofferingname,domain,domainid,zoneid,zonename,account,hypervisor,macaddress,ipaddress,networkid,publicipid,publicip,hostname,hostid,displayname\n";

for($i=0;$i<$count;$i++)
{ 
  my $js = @{$vms}[$i];

  print $js->{'id'} . ",";
  print $js->{'instancename'} . ",";
  print $js->{'name'} . ",";
  print $js->{'state'} . ",";
  print $js->{'haenable'} . ",";
  print $js->{'created'} . ",";
  print $js->{'cpunumber'} . ",";
  print $js->{'cpuspeed'} . ",";
  print $js->{'memory'} . ",";
  print $js->{'rootdeviceid'} . ",";
  print $js->{'rootdevicetype'} . ",";
  print $js->{'serviceofferingid'} . ",";
  print $js->{'serviceofferingname'} . ",";
  print $js->{'domain'} . ",";
  print $js->{'domainid'} . ",";
  print $js->{'zoneid'} . ",";
  print $js->{'zonename'} . ",,";
  print $js->{'account'} . ",";
  print $js->{'hypervisor'} . ",";
  print $js->{'nic'}[0]->{'macaddress'} . ",";
  print $js->{'nic'}[0]->{'ipaddress'} . ",";
  print $js->{'nic'}[0]->{'networkid'} . ",";
  print $js->{'publicipid'} . ",";
  print $js->{'publicip'} . ",";
  print $js->{'hostname'} . ",";
  print $js->{'hostid'} . ",";
  print $js->{'displayname'} . ",\n";

#    while(my ($key,$value) = each(%$js))
#    {
#      if($key eq 'nic')
#      {
#	my $hash= @{$value}[0];
#	while(my ($k,$v) = each(%$hash))
#	{
#	  print $key . "_" . $v . ",";
#	  print $i . ":" . $key . "_" . $k . ":" . $v . "\n";
#	}
#      }
#      elsif($key eq 'securitygroup')
#      {
#	next;
#      }
#      else
#      {
#	#print $i . ":" . $key . ":" . $value . "\n";
#	print $value . ",";
#      }
#    }
#    print "\n";
}
