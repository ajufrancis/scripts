<script>./lib/sha1.js</script>
<script>
var apiUrl = 'http://10.24.4.12:50481/client/api';
var apiKey = '';
var secretKey = '';
var cmd = 'listVirutalMachines';
var opt = 'json';
var Url = function(apiUrl,apiKey,secretKey,cmd,opt){
		var signature ="";

		if(opt){
			opt = "&" + opt;
		}
		cmd = "command=" + cmd + opt + "&apiKey=" +apiKey ;
		var cmdOrig = cmd;

		//Step1 & 2
		cmdArray = cmd.split("&");
		cmd = encodeURI(cmdArray.sort().join("&").toLowerCase());
		//Ti.API.info(cmd);

		var sig = b64_hmac_sha1(secretKey, cmd);
		sig = encodeURIComponent(sig);

		var url = apiUrl+"?"+cmdOrig+"&signature="+sig;
	
		return url;
};
</script>
