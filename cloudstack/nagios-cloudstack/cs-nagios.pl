#!/usr/bin/perl
use strict;
use warnings;

use Net::CloudStack;
    my $api = Net::CloudStack->new(
        base_url        => 'http://10.24.4.12',
        api_path        => 'client/api?',
        api_key         => 'f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q',
        secret_key      => '31f691e9-d813-4caa-a2f3-86294db4aa46',
        xml_json        => 'json', #response format.you can select json or xml. xml is default.
        send_request    => 'yes',  #yes or no.
                                   #When you select yes,you can get response.
                                   #If you don't want to get response(only generating url),please input no. 
    );

    # CloudStack API Methods
    #$api->proc($cmd, $opt);
    $api->proc("listVirtualMachines");
#    $api->proc("listVirtualMachines","id=123");

#    $api->proc("deployVirtualMachine","serviceofferingid=1&templateid=1&zoneid=1"); # some IDs are depend on your environment.

    # Original Methods
    print $api->url;      # print generated url
    print $api->response; # print API response
