#!/usr/bin/perl -w
use strict;
#use CGI qw(:all);

my $title = "Hello,World !";

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
<a href="run.pl">$title</a>
EOF
print &Template("templates/_footer.html");
