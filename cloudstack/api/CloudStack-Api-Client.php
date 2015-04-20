<?php
/**
 * Class Request
 *
 * Allows the developer generate http request to Cloudstack api.
 * This application needs the php5-curl module installed.
 *
 * @package Cloudstack
 * @author Daniel Pereira
 */
class Request
{   
    /**
     * User cloudstack api key.
     *
     * @var string
     * @access protected
     */
    protected $api_key      = '';
    
    /**
     * User cloudstack secret key.
     *
     * @var string 
     * @access protected
     */
    protected $secret_key   = '';
    
    /**
     * Base url of cloudstack management server
     *
     * @var string
     * @access protected
     */
    protected $base_url     = '';
    
    /**
     * Api endpoint of cloudstack management server
     *
     * @var string 
     * @access protected
     */
    protected $endpoint     = '/client/api'; // Default value
    
    /**
     * Api command
     *
     * @var string
     * @access protected
     */
    protected $command      = '';
    
    /**
     * Request signature
     * 
     * @var string
     * @access protected
     */
    protected $signature   = '';
     
    /**
     * Constructor
     *
     * @access public
     * @param array
     * @return void
     */
    public function __construct($props = array())
    {
        if (count($props) > 0)
        {
            $this->initialize($props);
        }
        
        // Class initialized
    }
    
    /**
     * Clear the api properties.
     *
     * @access public
     * @return void
     */
    public function clear()
    {
        $props = array('api_key', 'secret_key', 'base_url', 'endpoint', 
                    'command', 'signature');
        foreach ($props as $val)
        {
            $this->$val = '';
        }
        
        // Set the default value for endpoint
        $this->endpoint = '/client/api';
    }
    
    /**
     * Initialize the api preferences.
     *
     * @access public
     * @param array
     * @return bool
     */
    public function initialize($props = array())
    {
        if (count($props) > 0)
        {
            foreach ($props as $key => $val)
            {
                $this->$key = $val;
            }
        }
        
        // Is there a base url?
        // If not, there's no reason to continue
        if ($this->base_url == '')
        {
            error_log("No base url", 0);
            return FALSE;
        }
        
        // Is there a api key?
        // If not, there's no reason to continue
        if ($this->api_key == '')
        {
            error_log("No user api key", 0);
            return FALSE;
        }
        
        // Is there a secret key?
        // If not, there's no reason to continue
        if ($this->secret_key == '')
        {
            error_log("No user secret key", 0);
            return FALSE;
        }
        
        // Is there a command?
        // If not, there's no reason to continue
        if ($this->command == '')
        {
            error_log("No api command", 0);
            return FALSE;
        }
        
        // If you are here that means it's all right
        return TRUE;
    }
    
    /**
     * Build query to generate signature.
     *
     * @access public
     * @param string
     * @return string
     */
    public function build_query($response = 'xml')
    {
        $strcmd = array(
            'apikey'    => $this->api_key,
            'command'   => $this->command 
        );
        
        // Is a json response?
        // If not, there's no reason to put in command string
        if (strcmp($response, 'json') == 0)
        {
            $strcmd['response'] = $response;
        }
        
        // Sort command string by key
        ksort($strcmd);
        
        $query = http_build_query($strcmd);
        $query = urldecode($query);
        $query = str_replace("+", "%20", $query);
        
        return $query;
    }
    
    /**
     * Generate request signature.
     *
     * @access public
     * @param string
     * @return string
     */
    public function generate_sign($query)
    {
        $hash = hash_hmac('sha1', strtolower($query), $this->secret_key, TRUE);
        $base64encoded = base64_encode($hash);
        return urlencode($base64encoded);
    }
    
    /**
     * Generate the http request.
     * 
     * @access public
     * @param string 
     * @return string
     */
    public function request($url)
    {
        $ch = curl_init($url);
        $response = curl_exec($ch);
        curl_close($ch);
        
        return $response;
    }
}

/* End of file request.php */
/* Location: ./request.php */
