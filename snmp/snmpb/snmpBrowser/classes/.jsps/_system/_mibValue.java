  /*@lineinfo:filename=/system/mibValue.jsp*/
  /*@lineinfo:generated-code*/
package _system;

import oracle.jsp.runtime.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import com.av.*;
import com.dwipal.*;
import javax.swing.JTree;
import java.util.HashMap;
import javax.swing.tree.*;
import org.snmp4j.*;
import org.snmp4j.event.*;
import org.snmp4j.transport.*;
import org.snmp4j.smi.*;
import org.snmp4j.mp.*;


public class _mibValue extends com.orionserver.http.OrionHttpJspPage {

  public final String _globalsClassName = null;

  // ** Begin Declarations


  // ** End Declarations

  public void _jspService(HttpServletRequest request, HttpServletResponse response) throws java.io.IOException, ServletException {

    response.setContentType( "text/xml;charset=windows-1252");
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
    _mibValue page = this;
    ServletConfig config = pageContext.getServletConfig();

    try {
      // global beans
      // end global beans


      out.write(__oracle_jsp_text[0]);
      out.write(__oracle_jsp_text[1]);
      /*@lineinfo:user-code*//*@lineinfo:4^1*/      
          if(session.getAttribute("user").equals("user")){
            out.println("<err>Only admin can get/set value</err>");
          }else{
            DwSnmpMibTreeGUI tree1 = (DwSnmpMibTreeGUI)application.getAttribute("snmpMibTree");
            DwSnmpMibBrowserFunctions snmp = tree1.getSnmpObject();
            String ip = session.getAttribute("ip") == null?"127.0.0.1":session.getAttribute("ip").toString();
            int port = session.getAttribute("port") == null?161:Integer.parseInt(session.getAttribute("port").toString());
            String oid = request.getParameter("oid");
            
            if(request.getParameter("cSet")!=null){
              session.setAttribute("cSet", request.getParameter("cSet"));
            }
            if(request.getParameter("cGet")!=null){
              session.setAttribute("cGet", request.getParameter("cGet"));
            }
            
            if(session.getAttribute("cSet")==null){
              session.setAttribute("cSet", "public");
            }
            if(session.getAttribute("cGet")==null){
              session.setAttribute("cGet", "public");
            }
            
            snmp.setIP(ip);
            snmp.setPort(port);
        
            SnmpLib snmpLib = new SnmpLib();
            snmpLib.setHost(ip);
            snmpLib.setPort(port);
            snmpLib.setCommunity(session.getAttribute("cGet").toString(), session.getAttribute("cSet").toString());
        
            if (oid.endsWith("0")) {
              oid = oid.substring(0, oid.lastIndexOf("."));
            } else if (oid.endsWith("*")) {
              oid = oid.substring(0, oid.lastIndexOf("*") - 1);
            } else if (oid.endsWith(")")) {
              oid = oid.substring(0, oid.indexOf("(") - 1);
            } else {
            }
            boolean processGet = true;
            if(request.getParameter("set") != null){
              JTree myTree = tree1.getTree();    
              myTree.setSelectionRow(Integer.parseInt(request.getParameter("row")));
              DefaultMutableTreeNode node = (DefaultMutableTreeNode) myTree.getLastSelectedPathComponent();
              DwSnmpMibRecord nodeTree = tree1.getSelectedTreeNode();
              
              String setValue = request.getParameter("value");
              if(setValue!=null && nodeTree.checkValidValue(setValue)) {
                try{
                  snmpLib.snmpSetValue(request.getParameter("oid"), nodeTree.getSyntaxID(), setValue);
                }catch(Exception e){
                  out.println("<err>Error in set Value</err>");
                  processGet = false;
                }
              }else{
                out.println("<err>Value is not valid</err>");
                processGet = false;
              }
            }
            if(processGet){
              MySnmpResponseHandler hnd = new MySnmpResponseHandler();
              snmpLib.setSnmpResponseHandler(hnd);    
              snmpLib.snmpWalk(oid);
              long start = System.currentTimeMillis();
              do{
                long end = System.currentTimeMillis();  
                if((end-start)>5000){
                  out.println("<err>Timeout</err>");
                  start = -1;
                  hnd.done = true;
                }
              }while(!hnd.done);
              if(start != -1){
                out.println("<val><![CDATA["+hnd.value+"]]></val>");
              }
            }
          }
      
      /*@lineinfo:generated-code*/
      out.write(__oracle_jsp_text[2]);


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
  private static final char __oracle_jsp_text[][]=new char[3][];
  static {
    try {
    __oracle_jsp_text[0] = 
    "\n".toCharArray();
    __oracle_jsp_text[1] = 
    "\n<root>\n".toCharArray();
    __oracle_jsp_text[2] = 
    "\n</root>".toCharArray();
    }
    catch (Throwable th) {
      System.err.println(th);
    }
}
}
