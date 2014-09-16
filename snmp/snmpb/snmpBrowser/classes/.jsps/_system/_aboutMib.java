  /*@lineinfo:filename=/system/aboutMib.jsp*/
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


public class _aboutMib extends com.orionserver.http.OrionHttpJspPage {

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
    _aboutMib page = this;
    ServletConfig config = pageContext.getServletConfig();

    try {
      // global beans
      // end global beans


      out.write(__oracle_jsp_text[0]);


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
  private static final char __oracle_jsp_text[][]=new char[1][];
  static {
    try {
    __oracle_jsp_text[0] = 
    "\n<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n<META HTTP-EQUIV=\"Expires\" CONTENT=\"-1\">\n<style>\n TD {\n   font-size: 10pt;\n   font-family: verdana,helvetica;\n   text-decoration: none;\n   white-space: nowrap;}\n</style>\n\n<body bgcolor=\"#CDCDCD\">\n<form>\n  <table width=\"680\" height=\"500\" style=\"border:1px solid;padding-left:30px;padding-right:30px;\" cellpadding=\"5\" cellspacing=\"0\" bgcolor=\"#FEFEFE\">\n    <tr>\n      <td valign=\"top\" colspan=\"3\" align=\"center\"><br/>\n        <font size=\"5\" face=\"Courier\" style=\"font-weight:bold\">\n        Web Based MIB Browser</font>\n        <hr width=\"80%\" style=\"border:1px solid\"/>\n      </td>\n    </tr>\n    <tr>\n      <td valign=\"top\" align=\"center\">\n   Network management frameworks were more different than anticipated.<br>\n   As such, the requirement for compatibility between the SMI/MIB and<br>\n   both frameworks was suspended.  This action permitted the operational<br>\n   network management framework, the SNMP, to respond to new operational<br>\n   needs in the Internet community by producing this document.<br><br>\n\n   As such, the current network management framework for TCP/IP- based<br>\n   internets consists of: Structure and Identification of Management<br>\n   Information for TCP/IP-based internets, RFC 1155 [12], which<br>\n   describes how managed objects contained in the MIB are defined;<br>\n   Management Information Base for Network Management of TCP/IP-based<br>\n   internets: MIB-II, this memo, which describes the managed objects<br>\n   contained in the MIB (and supercedes RFC 1156 [13]); and, the Simple<br>\n   Network Management Protocol, RFC 1098 [5], which defines the protocol<br>\n   used to manage these objects.<br>\n      </td>\n    </tr>\n  </table>  \n</form>\n</body>".toCharArray();
    }
    catch (Throwable th) {
      System.err.println(th);
    }
}
}
