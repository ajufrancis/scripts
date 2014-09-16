#!/usr/bin/perl -w
use HTML::KTemplate;

$tpl = HTML::KTemplate->new('templates/');

$tpl->assign( TITLE  => 'Template Test Page'    );
$tpl->assign( TEXT   => 'Some welcome text ...' );

foreach (1 .. 3) {

    $tpl->assign( LOOP,
        TEXT => 'Just a test ...',
    );

}

$tpl->process('template.tpl');

$tpl->print();
