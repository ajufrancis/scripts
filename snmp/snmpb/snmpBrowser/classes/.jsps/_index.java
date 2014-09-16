  /*@lineinfo:filename=/index.jsp*/
  /*@lineinfo:generated-code*/

import oracle.jsp.runtime.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;


public class _index extends com.orionserver.http.OrionHttpJspPage {

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
    _index page = this;
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
    "\n<html>\n  <head>\n    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=windows-1252\">\n    <title>MIB Browser - Login Page</title>\n  </head>\n  <script>\n    function checkPath(){\n      var path = window.parent.location+\"\";\n      if(path.indexOf(\"index.jsp\")==-1){\n        window.parent.location = \"index.jsp\";\n      }\n    }\n  </script>\n  <body onload=\"checkPath()\" bgcolor=\"#CDCDCD\">\n    <table width=\"100%\" height=\"100%\">\n      <tr>\n      <td valign=\"center\" align=\"center\">\n        <table width=\"600\" height=\"200\" style=\"border:1px solid\" bgcolor=\"#EFEFEF\">\n          <tr>\n            <td valign=\"bottom\" align=\"center\">\n              <font size=\"18\" face=\"Courier\">Login Page</font>\n              <hr width=\"80%\" style=\"border:1px solid\"/>\n            </td>\n          </tr>\n          <tr>\n          <td align=\"center\" valign=\"top\">\n          <form method=\"post\" action=\"process\">\n            <table cellpadding=0 cellspacing=7 style=\"font-family:courier;font-weight:bold\">\n              <tr>\n                <td width=\"100\">User</td>\n                <td width=\"5\">:</td>\n                <td><input type=\"text\" name=\"user\"/></td>\n              </tr>\n              <tr>\n                <td>Password</td>\n                <td>:</td>\n                <td><input type=\"password\" name=\"pass\"/></td>\n              </tr>\n              <tr>\n                <td colspan=\"2\"></td>\n                <td style=\"padding-top:2px\"><input type=\"submit\" value=\"Login\" style=\"width:100;font-size:16;font-weight:bold\"/></td>\n              </tr>\n            </table>\n          </form>\n          </td>\n          </tr>\n        </table>\n      </td>\n      </tr>\n    </table>    \n  </body>\n</html>\n".toCharArray();
    }
    catch (Throwable th) {
      System.err.println(th);
    }
}
}
