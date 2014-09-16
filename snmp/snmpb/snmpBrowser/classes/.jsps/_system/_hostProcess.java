  /*@lineinfo:filename=/system/hostProcess.jsp*/
  /*@lineinfo:generated-code*/
package _system;

import oracle.jsp.runtime.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.util.HashMap;


public class _hostProcess extends com.orionserver.http.OrionHttpJspPage {

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
    _hostProcess page = this;
    ServletConfig config = pageContext.getServletConfig();

    try {
      // global beans
      // end global beans


      out.write(__oracle_jsp_text[0]);
      /*@lineinfo:user-code*//*@lineinfo:2^1*/      
        String ip = request.getParameter("ip");
        HashMap hm = (HashMap)application.getAttribute("hashWS");
        HashMap hmStat = (HashMap)application.getAttribute("hashWSstat");
        if(request.getParameter("event").equals("delete")){
          hm.remove(ip);
          hmStat.remove(ip);
        }else if(request.getParameter("event").equals("add")){
          hm.put(ip, ip);
          hmStat.put(ip, hmStat.get(ip)==null?"dact":hmStat.get(ip));
        }
        application.setAttribute("hashWS", hm);
      
      /*@lineinfo:generated-code*/


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
    "\n".toCharArray();
    }
    catch (Throwable th) {
      System.err.println(th);
    }
}
}
