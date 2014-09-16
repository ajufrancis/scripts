#!/usr/bin/env perl
use App::Cmd;
use strict;
use warnings;
use lib '/opt/nagios-cloudstack/lib';

use Cloudstack;
Cloudstack->run;
