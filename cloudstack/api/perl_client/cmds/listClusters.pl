#!/usr/bin/perl -w

use Net::CloudStack;
use JSON;

my $api = Net::CloudStack->new(
        base_url        => 'http://192.168.11.2:8080',
        api_path        => 'client/api?',
	#admin
        api_key         => 'f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q',
        secret_key      => '8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g',
        xml_json        => 'json', #response format.you can select json or xml. xml is default.
        send_request    => 'yes',  #yes or no.
                                   #When you select yes,you can get response.
                                   #If you don't want to get response(only generating url),please input no.
    );

my $clusters = $api->proc("listClusters");
print $clusters;
