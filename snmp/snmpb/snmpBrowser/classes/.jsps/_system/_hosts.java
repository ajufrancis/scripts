  /*@lineinfo:filename=/system/hosts.jsp*/
  /*@lineinfo:generated-code*/
package _system;

import oracle.jsp.runtime.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.net.InetAddress;
import java.util.HashMap;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.InputStreamReader;


public class _hosts extends com.orionserver.http.OrionHttpJspPage {

  public final String _globalsClassName = null;

  // ** Begin Declarations


  // ** End Declarations

  public void _jspService(HttpServletRequest request, HttpServletResponse response) throws java.io.IOException, ServletException {

    response.setContentType( "text/html;charset=windows-1252");
    /* set up the intrinsic variables using the pageContext goober:
    ** session = HttpSession
    ** application = ServletContext
    ** out = JspWriter
    ** page = this
    ** config = ServletConfig
    ** all session/app beans declared in globals.jsa
    */
    PageContext pageContext = JspFactory.getDefaultFactory().getPageContext( this, request, response, null, true, JspWriter.DEFAULT_BUFFER, true);
    // Note: this is not emitted if the session directive == false
    HttpSession session = pageContext.getSession();
    if (pageContext.getAttribute(OracleJspRuntime.JSP_REQUEST_REDIRECTED, PageContext.REQUEST_SCOPE) != null) {
      pageContext.setAttribute(OracleJspRuntime.JSP_PAGE_DONTNOTIFY, "true", PageContext.PAGE_SCOPE);
      JspFactory.getDefaultFactory().releasePageContext(pageContext);
      return;
}
    int __jsp_tag_starteval;
    ServletContext application = pageContext.getServletContext();
    JspWriter out = pageContext.getOut();
    _hosts page = this;
    ServletConfig config = pageContext.getServletConfig();

    try {
      // global beans
      // end global beans


      out.write(__oracle_jsp_text[0]);
      out.write(__oracle_jsp_text[1]);


    }
    catch( Throwable e) {
      try {
        if (out != null) out.clear();
      }
      catch( Exception clearException) {
      }
      pageContext.handlePageException( e);
    }
    finally {
      OracleJspRuntime.extraHandlePCFinally(pageContext,false);
      JspFactory.getDefaultFactory().releasePageContext(pageContext);
    }

  }
  private static final char __oracle_jsp_text[][]=new char[2][];
  static {
    try {
    __oracle_jsp_text[0] = 
    "\n".toCharArray();
    __oracle_jsp_text[1] = 
    "\n<html>\n  <head>\n    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=windows-1252\">\n    <title>Web Based MIB Browser - List Worksation</title>\n  </head>\n  <script src=\"js/sarissa.js\"></script>\n  <script>\n    function refreshHost(){\n  \t\tvar xmlhttp =  new XMLHttpRequest();\n      xmlhttp.open('POST', 'hostStatus.jsp', true);\n      xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');\n      xmlhttp.onreadystatechange = function() {\n        if (xmlhttp.readyState == 4) {\n          if (xmlhttp.status == 0 || xmlhttp.status == 200){\n            var hosts = xmlhttp.responseXML.getElementsByTagName(\"host\");\n            for(var i=0; i<hosts.length; i++){\n              var ip = hosts[i].firstChild.data;\n              var objId = document.getElementById(ip);\n              var stat = hosts[i].getAttribute(\"stat\");\n              if(objId){\n                objId.childNodes[0].childNodes[0].src = \"img/\"+stat+\".gif\";\n                objId.childNodes[2].childNodes[0].disabled = (stat=='act'?false:true);\n              }else{\n                manList(document.forms[0].btnAdd, ip, \"add\", stat);\n              }\n            }\n          }\n        }\n      }\n      xmlhttp.send(\"flag=all\");\n      setTimeout(\"refreshHost()\", 10000);\n    }\n    \n    function isValidFormat(ip){\n      var add = ip.split(\".\");\n      if(add.length != 4){\n        return false;\n      }\n      for(var i=0;i<add.length;i++){\n        if(isNaN(add[i])){\n          return false;\n        }\n        if((add[i]>0||(i!=0&&i!=3))&&add[i]<255){\n          continue;\n        }else{\n          return false;\n        }\n      }\n      return true;\n    }\n    \n    function manList(obj, ip, opr, stat){\n      if(opr == \"delete\"){\n        obj.parentNode.parentNode.parentNode.removeChild(obj.parentNode.parentNode);\n      }else if(opr == \"add\"){\n        if(!ip){\n          ip = document.forms[0].host.value;\n          document.forms[0].host.value = \"\";\n        }\n        if(!ip){\n          alert('Please input the ip!');\n          return false;\n        }else if(!isValidFormat(ip)){\n          alert('Format ip: x.x.x.x!');\n          return false;\n        }\n        if(document.getElementById(ip)!=null){\n          alert(\"It's already on the list!\");\n          return false;\n        }\n        var tr = document.createElement(\"tr\");\n//        tr.style.border = \"1px solid\";\n        tr.id = ip;\n        var td1 = document.createElement(\"td\");\n        if(stat){\n          td1.innerHTML = \"<img src='img/\"+stat+\".gif' width='35' height='35'/>\";\n        }else{\n          td1.innerHTML = \"<img src='img/dact.gif' width='35' height='35'/>\";\n        }\n        var td2 = document.createElement(\"td\");\n        td2.innerHTML = ip;\n        td2.width = 200;\n        var td3 = document.createElement(\"td\");\n        if(stat){\n          td3.innerHTML = \"<input type='button' value='mib status' \"+(stat==\"act\"?\"\":\"disabled\")+\" onclick=\\\"document.forms[0].ip.value='\"+ip+\"';document.forms[0].submit()\\\"/>\";\n        }else{\n          td3.innerHTML = \"<input type='button' value='mib status' disabled \"+(stat==\"act\"?\"\":\"disabled\")+\" onclick=\\\"document.forms[0].ip.value='\"+ip+\"';document.forms[0].submit()\\\"/>\";\n        }\n        var td4 = document.createElement(\"td\");\n        td4.innerHTML = \"<input type='button' value='delete' onclick=\\\"if(confirm('Delete \"+ip+\" from list?'))manList(this, '\"+ip+\"', 'delete')\\\"/>\";\n        tr.appendChild(td1);\n        tr.appendChild(td2);\n        tr.appendChild(td3);\n        tr.appendChild(td4);\n        obj.parentNode.parentNode.parentNode.insertBefore(tr, obj.parentNode.parentNode.nextSibling);\n        //return false;\n      }\n      if(!stat){\n        var xmlhttp =  new XMLHttpRequest();\n        xmlhttp.open('POST', 'hostProcess.jsp', true);\n        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');\n        xmlhttp.send(\"event=\"+opr+\"&ip=\"+escape(ip));\n      }\n    }\n\n    function check(event){\n      if(event.keyCode==13){\n        document.forms[0].btnAdd.click();\n        return false;\n      }\n    }\n  </script>\n\n  <body bgcolor=\"#CDCDCD\">\n    <table width=\"100%\" height=\"100%\">\n      <tr>\n      <td valign=\"center\" align=\"center\">\n        <table width=\"600\" style=\"border:1px solid\" bgcolor=\"#EFEFEF\">\n          <tr>\n            <td valign=\"bottom\" align=\"center\">\n              <font size=\"6\" face=\"Courier\">List Workstation</font>\n              <hr width=\"80%\" style=\"border:1px solid\"/>\n            </td>\n            <td valign=\"top\" align=\"right\" title=\"logout\"><img src=\"img/logout.gif\" onclick=\"window.location='./../process?logout=true'\"/></td>\n          </tr>\n          <tr>\n          <td align=\"center\" valign=\"top\" colspan=\"2\">\n          <div style=\"width:600;height:220;overflow:auto\">\n          <form method=\"post\" action=\"mainMib.jsp\" onsubmit=\"return false\">\n            <table border=0 cellpadding=0 cellspacing=0 style=\"font-family:courier;font-size:2\">\n              <tr>\n                <td colspan=\"4\" align=\"center\"><b>Host IP: </b><input maxlength=\"20\" type=\"text\" name=\"host\" onkeydown=\"return check(event)\"/> <input type=\"button\" name=\"btnAdd\" value=\"Add\" onclick=\"manList(this,null,'add')\"/><br/><br/></td>\n              </tr>\n            </table>\n            <input type=\"hidden\" name=\"ip\"/>\n          </form>\n          </div>\n          </td>\n          </tr>\n        </table>\n      </td>\n      </tr>\n    </table>    \n  </body>\n  <script>    \n    refreshHost();\n  </script>\n</html>".toCharArray();
    }
    catch (Throwable th) {
      System.err.println(th);
    }
}
}
