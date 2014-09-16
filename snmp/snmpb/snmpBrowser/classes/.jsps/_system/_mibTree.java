  /*@lineinfo:filename=/system/mibTree.jsp*/
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


public class _mibTree extends com.orionserver.http.OrionHttpJspPage {

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
    int __jsp_tag_starteval;
    ServletContext application = pageContext.getServletContext();
    JspWriter out = pageContext.getOut();
    _mibTree page = this;
    ServletConfig config = pageContext.getServletConfig();

    com.evermind.server.http.JspCommonExtraWriter __ojsp_s_out = (com.evermind.server.http.JspCommonExtraWriter) out;
    try {
      // global beans
      // end global beans


      __ojsp_s_out.write(__oracle_jsp_text[0]);
      __ojsp_s_out.write(__oracle_jsp_text[1]);
      /*@lineinfo:user-code*//*@lineinfo:31^3*/      
          HashMap al = new HashMap();    
          DwSnmpMibTreeGUI tree1 = null;
          if(application.getAttribute("snmpMibTree") == null){
            tree1 = new DwSnmpMibTreeGUI();
            tree1.createComponents();
            application.setAttribute("snmpMibTree", tree1);
          }else{
            tree1 = (DwSnmpMibTreeGUI)application.getAttribute("snmpMibTree");
          }    
          try{
            Thread.sleep(500);
          }catch(Exception e){
          }
          JTree t = tree1.getTree();
      
          for(int i=0; i<t.getRowCount(); i++){
            t.expandRow(i);
            Object []path = t.getPathForRow(i).getPath();
      
            t.setSelectionRow(i);
            DefaultMutableTreeNode node = (DefaultMutableTreeNode) t.getLastSelectedPathComponent();
      
            boolean declare = false;
            if(al.get(path[path.length-1])==null){
              al.put(path[path.length-1], ""+i);
              declare = true;
            }
            if(i==0){
              out.println("var foldersTree"+i+" = insFld(foldersTree, gFld(\""+path[path.length-1]+"\", \"infoMib.jsp?row="+i+"\"));");
            }else if(node.getChildCount()!=0){
              out.println("var foldersTree"+i+" = insFld(foldersTree"+al.get(path[path.length-2])+", gFld(\""+path[path.length-1]+"\", \"infoMib.jsp?row="+i+"\"));");
            }else if(path.length>1){
              out.println("insDoc(foldersTree"+al.get(path[path.length-2])+", gLnk(\"R\", \""+path[path.length-1]+"\", \"infoMib.jsp?row="+i+"\"));");
            }
          }
        
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
    "\r\n".getBytes("Cp1252");
    __oracle_jsp_text[1] = 
    "\r\n<html>\r\n  <head>\r\n    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=windows-1252\">\r\n    <title>untitled</title>\r\n  </head>\r\n\r\n\r\n  <style>\r\n   BODY {\r\n     background-color: #CDCDCD;}\r\n   TD {\r\n     font-size: 10pt;\r\n     font-family: verdana,helvetica;\r\n     text-decoration: none;\r\n     white-space: nowrap;}\r\n   A {\r\n     text-decoration: none;\r\n     color: black;}\r\n  </style>\r\n\r\n  <script src=\"js/ua.js\"></script>\r\n  <script src=\"js/ftiens4.js\"></script>\r\n  \r\n  <script>\r\n    USETEXTLINKS = 1\r\n    HIGHLIGHT = 1\r\n    ICONPATH = \"img/\";\r\n    var foldersTree = gFld(\"MIB Tree - RFC1213\", \"aboutMib.jsp\");\r\n  ".getBytes("Cp1252");
    __oracle_jsp_text[2] = 
    "\r\n  </script>\r\n  <body>\r\n    <input type=\"button\" value=\"Logout\" onclick=\"window.parent.location='./../process?logout=true'\"/>\r\n    <input type=\"button\" value=\"Change Host\" onclick=\"window.parent.location='hosts.jsp'\"/>\r\n    <div style=\"position:absolute; top:0; left:0;display:none\"><table border=\"0\"><tr><td><font size=\"-2\"><a style=\"font-size:7pt;text-decoration:none;color:silver;\" href=\"http://www.treemenu.net/\" target=\"_blank\">JavaScript Tree</a></font></td></tr></table></div>\r\n    <script>initializeDocument();</script>\r\n  </body>\r\n</html>\r\n".getBytes("Cp1252");
    }
    catch (Throwable th) {
      System.err.println(th);
    }
}
}
