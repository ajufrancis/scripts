#!/usr/bin/perl
#use Encode;
use Net::CloudStack;
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


my $api = Net::CloudStack->new(
        base_url        => 'http://192.168.11.2:8080',
        api_path        => 'client/api?',
        #admin
        api_key         => 'f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q',
        secret_key      => '8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g',
        xml_json        => 'json', #response format.you can select json or xml. xml is default.
        send_request    => 'yes',  #yes or no.
    );

my $hosts = $api->proc("listHosts");

open(OUTFILE,">./listHosts.log");
  print OUTFILE $hosts;
close(OUTFILE);

if(open(MYFILE, "./listHosts.log")) 
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
close(MYFILE);

$json_obj = $json->decode($data);
my $count = $json_obj->{'listhostsresponse'}->{'count'};
my $hosts = $json_obj->{'listhostsresponse'}->{'host'};

print "name,ipaddress,state,cpunumber,cpuallocated,cpuspeed,memerytotal,memoryused,zonename,podname,clustername,hosttags,created\n";
for($i=0;$i<$count;$i++)
{ 
  my $js = @{$hosts}[$i];
#  SecondaryStorage
  if($js->{'type'} eq "Routing")
  {
    print $js->{'name'} . ",";
    print $js->{'ipaddress'} . ",";
    print $js->{'state'} . ",";
    print $js->{'cpunumber'} . ",";
    print $js->{'cpuallocated'} . ",";
    print $js->{'cpuspeed'} . ",";
    print $js->{'memorytotal'} . ",";
    print $js->{'memoryused'} . ",";
    print $js->{'zonename'} . ",";
    print $js->{'podname'} . ",";
    print $js->{'clustername'} . ",";
    print $js->{'hosttags'} . ",";
    print $js->{'created'};
    print "\n";
  }
}
