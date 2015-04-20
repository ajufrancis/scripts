<html>  
 <head>  
 <title>CloudStack API Example</title>  
 </head>  
<body>
 <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">  
      <div id="wrapper" style="width: 500px;margin: auto;border: 1px solid black">  
           <div id="header">  
                <h1>Welcome</h1>  
                <p>This is the CloudStack API frontend. Please use the fields below to build your VMs in mass :-)</p>  
           </div>  
           <div id="content">  
                <div id="col1" style="float:left;width:248px;text-align:right">API KEY: </div>  
                <div id="col2" style="float:left;width:248px;"><input type="text" name="apikey" placeholder="Example: RACKPOOL"><br /></div>  
           </div>  
           <div id="content">  
                <div id="col1" style="float:left;width:248px;text-align:right">Secret KEY: </div>  
                <div id="col2" style="float:left;width:248px;"><input type="text" name="secretkey" placeholder="Example: 21"><br /></div>  
           </div>  
           <div id="content">  
                <div id="col1" style="float:left;width:248px;text-align:right">Endpoint </div>  
                <div id="col2" style="float:left;width:248px;"><input type="text" name="baseurl" placeholder="http://csm01:8096"><br /><br /></div>  
           </div>  
           <div id="footer" align="center">  
                <input type="submit" name="submit" value="Build 'em!">  
           </div>  
      </div>  
 </form>  
</body>
 </html>
