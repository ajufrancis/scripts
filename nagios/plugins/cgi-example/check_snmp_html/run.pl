#!/usr/bin/perl -w
use strict;
#use CGI qw(:all);

my $title = "Hello,World !";

#my @result = readpipe("snmptranslate -Tz -l /tmp");
#my @result = system("export mibs=ALL");
#my @result = system("snmptranslate -Tz >/tmp/snmptranslate-Tz.log");


sub Template {
  my $file;
  my $HTML;
  $file = $_[0] || die "Template: No template file specified.\n";
  open (FILE,"<$file") || die "Template: Couldn't open $file:$!\n";
  while (<FILE>) { $HTML .= $_; }
  close(FILE);
  $HTML =~ s/(\$\w+)/eval "$1"/ge;
  #$HTML =~ s/\$(\w+)/${$1}/g;
  return $HTML;
}

#print header( -charset => "GB18030");

print &Template("templates/_header.html");


print <<EOF;
<form action="index.pl" >
Name:<input type="text" name="namestring"><br>
Desc:<textarea name="comments"></textarea><br>
Food:
<input type="radio" name="choice" value="fish"/>Fish
<input type="radio" name="choice" value="steak"/>Steak
<input type="radio" name="choice" value="yogurt"/>Yogurt
<br>
<p>
<b>Choose a work place:</b> <br>
EOF

open(FILE,"/tmp/snmptranslate-Tz.log") || die "open /tmp/snmpstranslate-Tz.log failed!";
while(my $line = <FILE>)
{
  chomp($line);
  my $oid_name = (split /"/, $line)[1];;
  print <<EOF;
<input type="checkbox" name="oid_name" value="$oid_name"/>$oid_name<br>
EOF
}
close(FILE);

#<input type="checkbox" name="place" value="la"/>Los Angeles
#<input type="checkbox" name="place" value="sj"/>San Jose
#<input type="checkbox" name="place" value="sf" checked/>San Francisco

print <<EOF;
<select name="location"> 
<option selected value="hawaii"/> Hawaii
<option value="bali"/>Bali
<option value="maine"/>Maine
<option value="paris"/>Paris
</select>
</p>

<input type="submit" value="submit">
<input type="reset" value="clear">
</form>
EOF
print &Template("templates/_footer.html");
