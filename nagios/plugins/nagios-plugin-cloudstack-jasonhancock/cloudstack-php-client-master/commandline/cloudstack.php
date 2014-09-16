<?php
/*
 * This file is part of the CloudStack PHP Client.
 *
 * (c) Quentin Pleplé <quentin.pleple@gmail.com>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 */
 

/**************************
  File paths
 **************************/
define("CLOUDSTACKCLIENT_FILE", dirname(__FILE__) . "/../src/CloudStackClient.php");
define("CONFIG_FILE", dirname(__FILE__) . "/../config.php");

/**************************
  Initial checks
 **************************/
check(defined('STDIN'), "This script is supposed to be run from command line. Exiting.");
check(file_exists(CLOUDSTACKCLIENT_FILE), "Unable to find CloudStackClient file, looked for " . CLOUDSTACKCLIENT_FILE);
check(file_exists(CONFIG_FILE), "Unable to find config file, looked for " . CONFIG_FILE);
check($argc > 1, "Usage: php cloudstack.php command args...");

require CLOUDSTACKCLIENT_FILE;
$config = require CONFIG_FILE;
$command = $argv[1];
$args = array_slice($argv, 1);

/**************************
  Request
 **************************/
$cloudstack = new BaseCloudStackClient($config['endpoint'], $config['api_key'], $config['secret_key']);
try {
    $result = $cloudstack->request($command, $args);
} catch (Exception $e) {
    err($e->getMessage());
}

var_dump($result);

/**************************
  Helpers
 **************************/
function check($cond, $errorMessage) {
    if (!$cond) {
        err($errorMessage);
    }
}
function err($errorMessage) {
    die("Fatal Error: $errorMessage\n");
}

function var_dump_str($obj) {
    ob_start();
    var_dump($obj);
    return ob_get_clean();
}