  /*@lineinfo:filename=/system/hostStatus.jsp*/
  /*@lineinfo:generated-code*/
package _system;

import oracle.jsp.runtime.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import com.av.*;
import com.dwipal.*;
import org.snmp4j.*;
import org.snmp4j.event.*;
import org.snmp4j.transport.*;
import org.snmp4j.smi.*;
import org.snmp4j.mp.*;
import java.net.InetAddress;
import java.util.HashMap;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.InputStreamReader;


public class _hostStatus extends com.orionserver.http.OrionHttpJspPage {

  public final String _globalsClassName = null;

  // ** Begin Declarations


  // ** End Declarations

  public void _jspService(HttpServletRequest request, HttpServletResponse response) throws java.io.IOException, ServletException {

    response.setContentType( "text/xml;charset=ISO-8859-1");
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
    int __jsp_tag_starteval;
    ServletContext application = pageContext.getServletContext();
    JspWriter out = pageContext.getOut();
    _hostStatus page = this;
    ServletConfig config = pageContext.getServletConfig();

    com.evermind.server.http.JspCommonExtraWriter __ojsp_s_out = (com.evermind.server.http.JspCommonExtraWriter) out;
    try {
      // global beans
      // end global beans


      __ojsp_s_out.write(__oracle_jsp_text[0]);
      __ojsp_s_out.write(__oracle_jsp_text[1]);
      /*@lineinfo:user-code*//*@lineinfo:4^1*/      
        final int maxTime = 20000;
        if(session.getAttribute("cSet")==null){
          session.setAttribute("cSet", "public");
        }
        if(session.getAttribute("cGet")==null){
          session.setAttribute("cGet", "public");
        }
        if(application.getAttribute("hashWS")==null){
          HashMap hash = new HashMap();
          HashMap hmStat = new HashMap();
          
          hash.put(request.getServerName(), request.getServerName());
          hmStat.put(request.getServerName(), "act");
          
          application.setAttribute("hashWS", hash);
          application.setAttribute("hashWSstat", hmStat);
          
          application.setAttribute("lastCheck", System.currentTimeMillis()+"");
        }
        HashMap hm = (HashMap)application.getAttribute("hashWS");
        final HashMap hmStat = (HashMap)application.getAttribute("hashWSstat");
        ArrayList al = new ArrayList(hm.values());
        final HttpServletRequest req = request;
        final ServletContext app = application;
        req.setAttribute("ctrStat", "");
        final long start = Long.parseLong(app.getAttribute("lastCheck").toString());
        final long now = System.currentTimeMillis();
        final long diff = Math.abs(now - start);
        for(int i=0; i<al.size(); i++){
          final String ip = al.get(i).toString();
          final JspWriter innerOut = out;
      
          if(diff > maxTime){
            app.setAttribute("lastCheck", now+"");
          }
          try{
            final int port = session.getAttribute("port") == null?161:Integer.parseInt(session.getAttribute("port").toString());
            Thread t=new Thread(new Runnable() {
              public void run() {
                try{
                  if(diff > maxTime){
                    Process processPing = Runtime.getRuntime().exec("ping "+ ip + " -n 1 -l 1 -w 1000");
                    BufferedReader br= new BufferedReader( new InputStreamReader(processPing.getInputStream()));
                    String lnPing = null;
                    while ((lnPing = br.readLine()) != null){
                      if(lnPing.indexOf("Reply from") == 0){
                        lnPing = "act";
                        SnmpLib snmpLib = new SnmpLib();
                        snmpLib.setHost(ip);
                        snmpLib.setPort(port);
                        snmpLib.setCommunity("public", "public");
      
                        String oid = ".1.3.6.1.2.1.1.1";              
                        MySnmpResponseHandler hnd = new MySnmpResponseHandler();
                        snmpLib.setSnmpResponseHandler(hnd);    
                        snmpLib.snmpWalk(oid);
                        long start = System.currentTimeMillis();
                        do{
                          long end = System.currentTimeMillis();  
                          if((end-start)>1000){
                            start = -1;
                            hnd.done = true;
                          }
                        }while(!hnd.done);
                        if(start == -1){
                          lnPing = "nav";
                        }else{
                          lnPing = "act";
                        }
                        break;
                      }
                    }
                    if(lnPing == null){
                      lnPing = "dact";
                    }
                    hmStat.put(ip, lnPing);
                  }
                  innerOut.println("<host stat=\""+hmStat.get(ip)+"\"><![CDATA["+ip+"]]></host>");
                  req.setAttribute("ctrStat", req.getAttribute("ctrStat")+"1");
                }catch(Exception e){
                }
              }
            });
            t.start();
            }catch(Exception e){}
        }
        do{
        }while(request.getAttribute("ctrStat").toString().length()!=al.size());
        application.setAttribute("hashWSstat", hmStat);
      
      /*@lineinfo:generated-code*/
      __ojsp_s_out.write(__oracle_jsp_text[2]);


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
  private static final byte __oracle_jsp_text[][]=new byte[3][];
  static {
    try {
    __oracle_jsp_text[0] = 
    "\r\n".getBytes("ISO8859_1");
    __oracle_jsp_text[1] = 
    "\r\n<root>\r\n".getBytes("ISO8859_1");
    __oracle_jsp_text[2] = 
    "\r\n</root>".getBytes("ISO8859_1");
    }
    catch (Throwable th) {
      System.err.println(th);
    }
}
}
