<%@ page contentType="text/html;charset=windows-1252"%>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
    <title>MIB Browser - Login Page</title>
  </head>
  <script>
    function checkPath(){
      var path = window.parent.location+"";
      if(path.indexOf("index.jsp")==-1){
        window.parent.location = "index.jsp";
      }
    }
  </script>
  <body onload="checkPath()" bgcolor="#CDCDCD">
    <table width="100%" height="100%">
      <tr>
      <td valign="center" align="center">
        <table width="600" height="200" style="border:1px solid" bgcolor="#EFEFEF">
          <tr>
            <td valign="bottom" align="center">
              <font size="18" face="Courier">Login Page</font>
              <hr width="80%" style="border:1px solid"/>
            </td>
          </tr>
          <tr>
          <td align="center" valign="top">
          <form method="post" action="process">
            <table cellpadding=0 cellspacing=7 style="font-family:courier;font-weight:bold">
              <tr>
                <td width="100">User</td>
                <td width="5">:</td>
                <td><input type="text" name="user"/></td>
              </tr>
              <tr>
                <td>Password</td>
                <td>:</td>
                <td><input type="password" name="pass"/></td>
              </tr>
              <tr>
                <td colspan="2"></td>
                <td style="padding-top:2px"><input type="submit" value="Login" style="width:100;font-size:16;font-weight:bold"/></td>
              </tr>
            </table>
          </form>
          </td>
          </tr>
        </table>
      </td>
      </tr>
    </table>    
  </body>
</html>
