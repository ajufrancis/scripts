  /*@lineinfo:filename=/system/infoMib.jsp*/
  /*@lineinfo:generated-code*/
package _system;

import oracle.jsp.runtime.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import com.dwipal.*;
import javax.swing.JTree;
import java.util.HashMap;
import javax.swing.tree.*;


public class _infoMib extends com.orionserver.http.OrionHttpJspPage {

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
    _infoMib page = this;
    ServletConfig config = pageContext.getServletConfig();

    try {
      // global beans
      // end global beans


      out.write(__oracle_jsp_text[0]);
      /*@lineinfo:user-code*//*@lineinfo:4^1*/      
          DwSnmpMibTreeGUI tree1 = (DwSnmpMibTreeGUI)application.getAttribute("snmpMibTree");
          JTree myTree = tree1.getTree();    
          myTree.setSelectionRow(Integer.parseInt(request.getParameter("row")));
          DefaultMutableTreeNode node = (DefaultMutableTreeNode) myTree.getLastSelectedPathComponent();
          DwSnmpMibRecord nodeTree = tree1.getSelectedTreeNode();
      
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[1]);
      /*@lineinfo:user-code*//*@lineinfo:50^42*/      out.print(request.getParameter("row"));
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[2]);
      /*@lineinfo:user-code*//*@lineinfo:56^9*/      out.print(session.getAttribute("ip"));
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[3]);
      /*@lineinfo:user-code*//*@lineinfo:64^46*/      out.print(tree1.getOid(node));
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[4]);
      /*@lineinfo:user-code*//*@lineinfo:71^9*/      out.print(nodeTree.name);
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[5]);
      /*@lineinfo:user-code*//*@lineinfo:78^9*/      out.print(nodeTree.parent);
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[6]);
      /*@lineinfo:user-code*//*@lineinfo:85^9*/      out.print(nodeTree.number);
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[7]);
      /*@lineinfo:user-code*//*@lineinfo:92^9*/      out.print(nodeTree.access);
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[8]);
      /*@lineinfo:user-code*//*@lineinfo:100^11*/      
                  String syn = nodeTree.syntax;
                  if(nodeTree.syntax.length()>0){
                    if(nodeTree.syntax.charAt(0) == '\n'){
                      syn = nodeTree.syntax.substring(1);
                    }
                  }
                  out.println(syn.replaceAll("\n","<br>"));
                
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[9]);
      /*@lineinfo:user-code*//*@lineinfo:116^9*/      out.print(nodeTree.status);
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[10]);
      /*@lineinfo:user-code*//*@lineinfo:123^57*/      out.print(nodeTree.description);
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[11]);
      /*@lineinfo:user-code*//*@lineinfo:130^9*/      out.print(nodeTree.recordType);
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[12]);
      /*@lineinfo:user-code*//*@lineinfo:139^55*/      out.print(session.getAttribute("cGet"));
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[13]);
      /*@lineinfo:user-code*//*@lineinfo:144^48*/      out.print(nodeTree.isWritable()?"":"disabled");
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[14]);
      /*@lineinfo:user-code*//*@lineinfo:144^96*/      out.print(session.getAttribute("cSet"));
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[15]);
      /*@lineinfo:user-code*//*@lineinfo:145^74*/      out.print(nodeTree.isWritable()?"":"disabled");
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[16]);
      /*@lineinfo:user-code*//*@lineinfo:162^3*/      
          if(nodeTree.isWritable()){
        
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[17]);
      /*@lineinfo:user-code*//*@lineinfo:172^3*/      
          }
        
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[18]);


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
  private static final char __oracle_jsp_text[][]=new char[19][];
  static {
    try {
    __oracle_jsp_text[0] = 
    "\n<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n".toCharArray();
    __oracle_jsp_text[1] = 
    "\n  <style>\n   TD {\n     font-size: 10pt;\n     font-family: verdana,helvetica;\n     text-decoration: none;\n     white-space: nowrap;}\n  </style>\n\n<script src=\"js/sarissa.js\"></script>\n<script>\n  function setValueMib(){\n    getValueMib(true);\n  }\n  \n  function getValueMib(set){\n\t\tvar xmlhttp =  new XMLHttpRequest();\n\t\txmlhttp.open('POST', 'mibValue.jsp', true);\n\t\txmlhttp.onreadystatechange = function() {\n\t\t  if (xmlhttp.readyState == 4) {\n\t\t\t  if (xmlhttp.status == 0 || xmlhttp.status == 200){\n\t\t\t\t  \tif(xmlhttp.responseXML.getElementsByTagName(\"val\").length!=0){\n              document.forms[0].val.value = xmlhttp.responseXML.getElementsByTagName(\"val\")[0].firstChild.data;\n            }else{\n              alert(xmlhttp.responseXML.getElementsByTagName(\"err\")[0].firstChild.data);\n            }\n\t\t\t  }\n\t\t  }\n\t\t}\n\t\txmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');\n    if(set){\n      xmlhttp.send(\"cGet=\"+document.forms[0].cGet.value+\"&cSet=\"+document.forms[0].cSet.value+\"&set=true&row=\"+document.forms[0].row.value+\"&value=\"+escape(document.forms[0].valSet.value)+\"&oid=\"+escape(document.forms[0].oid.value));\n    }\n    else{\n      xmlhttp.send(\"cGet=\"+document.forms[0].cGet.value+\"&cSet=\"+document.forms[0].cSet.value+\"&oid=\"+escape(document.forms[0].oid.value));\n    }\n  }\n</script>\n<body bgcolor=\"#CDCDCD\">\n<form>\n  <input type=\"hidden\" name=\"row\" value=\"".toCharArray();
    __oracle_jsp_text[2] = 
    "\"/>\n  <table style=\"border:1px solid;padding-left:30px;padding-right:30px;\" cellpadding=\"5\" cellspacing=\"0\" bgcolor=\"#FEFEFE\">\n    <tr>\n      <td valign=\"top\" colspan=\"3\" align=\"center\">\n        <font size=\"5\" face=\"Courier\" style=\"font-weight:bold\"><br>\n        MIB Information on<br>\n        ".toCharArray();
    __oracle_jsp_text[3] = 
    "</font><br>\n        <hr width=\"80%\" style=\"border:1px solid\"/><br>\n      </td>\n    </tr>\n    <tr>\n      <td valign=\"top\">OID</td>\n      <td valign=\"top\" width=\"10\">:</td>\n      <td valign=\"top\">\n        <input type=\"text\" name=\"oid\" value=\"".toCharArray();
    __oracle_jsp_text[4] = 
    "\" readonly/>\n      </td>\n    </tr>\n    <tr bgColor=\"#EFEFEF\">\n      <td valign=\"top\">Name</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        ".toCharArray();
    __oracle_jsp_text[5] = 
    "\n      </td>\n    </tr>\n    <tr>\n      <td valign=\"top\">Parent</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        ".toCharArray();
    __oracle_jsp_text[6] = 
    "\n      </td>\n    </tr>\n    <tr bgColor=\"#EFEFEF\">\n      <td valign=\"top\">Number</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        ".toCharArray();
    __oracle_jsp_text[7] = 
    "\n      </td>\n    </tr>\n    <tr>\n      <td valign=\"top\">Access</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        ".toCharArray();
    __oracle_jsp_text[8] = 
    "\n      </td>\n    </tr>\n    <tr bgColor=\"#EFEFEF\">\n      <td valign=\"top\">Syntax</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        <div style=\"width:300;height:100;overflow:auto\">\n          ".toCharArray();
    __oracle_jsp_text[9] = 
    "\n        </div>\n      </td>\n    </tr>\n    <tr>\n      <td valign=\"top\">Status</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        ".toCharArray();
    __oracle_jsp_text[10] = 
    "\n      </td>\n    </tr>\n    <tr bgColor=\"#EFEFEF\">\n      <td valign=\"top\">Description</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        <div style=\"width:500;height:100;overflow:auto\">".toCharArray();
    __oracle_jsp_text[11] = 
    "</div>\n      </td>\n    </tr>\n    <tr>\n      <td valign=\"top\">Type</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        ".toCharArray();
    __oracle_jsp_text[12] = 
    "\n      </td>\n    </tr>\n    <tr>\n      <td colspan=\"2\"></td>\n      <td colspan=\"2\">\n        <table>\n          <tr>\n            <td>Get Community</td>\n            <td><input type=\"text\" name=\"cGet\" value=\"".toCharArray();
    __oracle_jsp_text[13] = 
    "\"/></td>\n            <td><input type=\"button\" value=\"GET\" onclick=\"getValueMib()\"/></td>\n          </tr>\n          <tr>\n            <td>Set Community</td>\n            <td><input type=\"text\" name=\"cSet\" ".toCharArray();
    __oracle_jsp_text[14] = 
    " value=\"".toCharArray();
    __oracle_jsp_text[15] = 
    "\"/></td>\n            <td><input type=\"button\" value=\"SET\" onclick=\"setValueMib()\" ".toCharArray();
    __oracle_jsp_text[16] = 
    "/></td>\n          </tr>     \n          <tr>\n            <td colspan=\"3\">       \n              <input type=\"button\" value=\"CHANGE HOST\" onclick=\"window.parent.location='hosts.jsp'\"/>\n            </td>\n          </tr>\n        </table>\n      </td>\n    </tr>\n    <tr bgColor=\"#EFEFEF\">\n      <td valign=\"top\">Value</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        <textarea name=\"val\" cols=\"58\" rows=\"5\" readOnly></textarea>\n      </td>\n    </tr>\n  ".toCharArray();
    __oracle_jsp_text[17] = 
    "\n    <tr bgColor=\"#EFEFEF\">\n      <td valign=\"top\">Value SET</td>\n      <td valign=\"top\">:</td>\n      <td valign=\"top\">\n        <textarea name=\"valSet\" cols=\"58\" rows=\"5\"></textarea>\n      </td>\n    </tr>  \n  ".toCharArray();
    __oracle_jsp_text[18] = 
    "\n  </table>  \n</form>\n</body>".toCharArray();
    }
    catch (Throwable th) {
      System.err.println(th);
    }
}
}
