#/usr/bin/perl -w 

002 use strict; 

003 # Enabling strict with strict refs breaks the summary output (when ctrl+c is pressed) 

004 # because of the error Can't use string ("") as a HASH ref while "strict refs" in use. 

005 no strict 'refs'; 

006   

007 #Initialize an empty hashref 

008 my $hash_ref = {}; 

009   

010 #Catch CTRL+C and then call printsummary subroutine 

011 $SIG{'INT'} = \&printsummary; 

012   

013 #Pipe the output from iotop to a file handle 

014 open fh, "iotop -bt|" or die $!; 

015   

016 # Build the initial Total Value key/values 

017 $hash_ref->{'tsample'} = 0; 

018 $hash_ref->{'tread'} = 0; 

019 $hash_ref->{'twrite'} = 0; 

020   

021 # Divider of columns 

022 my $div = ","; 

023   

024 #Print the header 

025 print "#" x 50 . "\n"; 

026 print "Output from iotop -bt\n"; 

027 print "#" x 50 . "\n"; 

028 print "timestamp" . $div . "tid" . $div . "user" . $div . "read" . $div . "total read each tid" . $div . "write" . $div . "total write each tid" .$div . "cmd" . $div . "sample number" . $div . "Percent of Total Read" . $div . "Percent of Total Write" . "\n"; 

029   

030 #While data from iotop process it. Since we get lots of 0.00 read and write values 

031 #don't waste time storing/printing values that are useless. Only store lines that 

032 #have a value to read/write. 

033 while(<fh>) { 

034   my ($ts,$tid,$prio,$user,$read,undef,$write,undef,undef,undef,undef,undef,$cmd) = split(/\s+/, "$_"); 

035   chomp($cmd); 

036   

037   #Make sure we fill each tid with dummy values if the tid is a real valid number 

038   if ( !$hash_ref->{$tid} && ( $tid =~ m/^-?\d+$/ || $tid =~ m/^-?\d+[\/|\.]\d+$/ ) ) 

039   { 

040     $hash_ref->{$tid}->{'user'} = 'null'; 

041     $hash_ref->{$tid}->{'read'} = 0; 

042     $hash_ref->{$tid}->{'write'} = 0; 

043     $hash_ref->{$tid}->{'cmd'} = 'null'; 

044     $hash_ref->{$tid}->{'samples'} = 0; 

045   } 

046   

047   #Continue if we have already created a key for the tid and the tid is a real valid number 

048   if ( $hash_ref->{$tid} && ( $tid =~ m/^-?\d+$/ || $tid =~ m/^-?\d+[\/|\.]\d+$/ ) ) 

049   { 

050     $hash_ref->{$tid}->{'user'} = $user; 

051     $hash_ref->{$tid}->{'read'} += $read if $read =~ m/^-?\d+$/ || $read =~ m/^-?\d+[\/|\.]\d+$/; 

052     $hash_ref->{$tid}->{'write'} += $write if $write =~ m/^-?\d+$/ || $write =~ m/^-?\d+[\/|\.]\d+$/; 

053     $hash_ref->{$tid}->{'cmd'} = $cmd; 

054     $hash_ref->{$tid}->{'samples'}++; 

055   

056     # create totals key/value pair 

057     $hash_ref->{'tsample'}++; 

058     $hash_ref->{'tread'} += $read if $read =~ m/^-?\d+$/ || $read =~ m/^-?\d+[\/|\.]\d+$/; 

059     $hash_ref->{'twrite'} += $write if $write =~ m/^-?\d+$/ || $write =~ m/^-?\d+[\/|\.]\d+$/; 

060   

061     # Print values of the read/write as they happen 

062     if ( ( $read =~ m/^-?\d+$/ || $read =~ m/^-?\d+[\/|\.]\d+$/ || $write =~ m/^-?\d+$/ || $write =~ m/^-?\d+[\/|\.]\d+$/ ) && ( $read > 0 ||$write > 0 ) ) 

063     { 

064       my $ptr = 0; 

065       my $ptw = 0; 

066       $ptr = ( $hash_ref->{$tid}->{'read'} / $hash_ref->{'tread'} ) * 100 if ( $read > 0 ) && ( $hash_ref->{'tread'} > 0 ); 

067       $ptw = ( $hash_ref->{$tid}->{'write'} / $hash_ref->{'twrite'} ) * 100 if ( $write > 0 ) && ( $hash_ref->{'twrite'} > 0 ); 

068   

069       print $ts . "$div"; 

070       print $tid . "$div"; 

071       print $hash_ref->{$tid}->{'user'} . "$div"; 

072       print $read . "$div"; 

073       print "$hash_ref->{$tid}->{'read'}" . "$div"; 

074       print $write . "$div"; 

075       print "$hash_ref->{$tid}->{'write'}" . "$div"; 

076       print $hash_ref->{$tid}->{'cmd'} . "$div"; 

077       print $hash_ref->{$tid}->{'samples'} . "$div"; 

078       print sprintf("%.2f", $ptr) . "$div"; 

079       print sprintf("%.2f", $ptw) . "\n"; 

080     } 

081   } 

082 } 

083   

084 # Close the filehandle when we are done. 

085 close(fh); 

086   

087 #Sub routine to print out a summary of disk I/O. 

088 sub printsummary { 

089 print "#" x 50 . "\n"; 

090 print "Caught Ctrl+C. Printing Disk I/O summary.\n"; 

091 print "#" x 50 . "\n"; 

092 print "Total Bytes Read:  $hash_ref->{'tread'}\n"; 

093 print "Total Bytes Write: $hash_ref->{'twrite'}\n"; 

094 print "#" x 50 . "\n"; 

095   

096 for my $id ( keys %$hash_ref ) 

097   { 

098   if ( $hash_ref->{$id}->{'read'} > 0 || $hash_ref->{$id}->{'write'} > 0 ) 

099     { 

100       my $psptr = 0; 

101       my $psptw = 0; 

102       $psptr = ( $hash_ref->{$id}->{'read'} / $hash_ref->{'tread'} ) * 100 if ( $hash_ref->{'tread'} > 0 ); 

103       $psptw = ( $hash_ref->{$id}->{'write'} / $hash_ref->{'twrite'} ) * 100 if ( $hash_ref->{'twrite'} > 0 ); 

104   

105       print "$id" . " "; 

106       print $hash_ref->{$id}->{'user'} . " "; 

107       print $hash_ref->{$id}->{'read'} . " "; 

108       print $hash_ref->{$id}->{'write'} . " "; 

109       print $hash_ref->{$id}->{'cmd'} . " "; 

110       print $hash_ref->{$id}->{'samples'} . " "; 

111       print sprintf("%.2f", $psptr) . " "; 

112       print sprintf("%.2f", $psptw); 

113       print "\n" 

114     } 

115   } 

116   print "#" x 50 . "\n"; 

117 } 

