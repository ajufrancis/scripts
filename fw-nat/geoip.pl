#!/usr/bin/perl -w
 use Geo::IP;
  my $gi = Geo::IP->new(GEOIP_MEMORY_CACHE);
  # look up IP address '24.24.24.24'
  # returns undef if country is unallocated, or not defined in our database
  my $country = $gi->country_code_by_addr('24.24.24.24');
  $country = $gi->country_code_by_name('yahoo.com');
  # $country is equal to "US"
  

  use Geo::IP;
  my $gi = Geo::IP->open("/usr/local/share/GeoIP/GeoIPCity.dat", GEOIP_STANDARD);
  my $record = $gi->record_by_addr('24.24.24.24');
  print $record->country_code,
        $record->country_code3,
        $record->country_name,
        $record->region,
        $record->region_name,
        $record->city,
        $record->postal_code,
        $record->latitude,
        $record->longitude,
        $record->time_zone,
        $record->area_code,
        $record->continent_code,
        $record->metro_code;


  # the IPv6 support is currently only avail if you use the CAPI which is much
  # faster anyway. ie: print Geo::IP->api equals to 'CAPI'
  use Socket;
  use Socket6;
  use Geo::IP;
  my $g = Geo::IP->open('/usr/local/share/GeoIP/GeoIPv6.dat') or die;
  print $g->country_code_by_ipnum_v6(inet_pton AF_INET6, '::24.24.24.24');
  print $g->country_code_by_addr_v6('2a02:e88::');
