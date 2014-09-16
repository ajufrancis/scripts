package com.av;
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.PrintWriter;
import java.io.IOException;

public class ServletLogin extends HttpServlet  {
  private static final String CONTENT_TYPE = "text/html; charset=windows-1252";
  private final String user = "user";
  private final String password = "userMib";
  private final String adm = "adminMib";
  private final String passAdm = "`admin123";

  public void init(ServletConfig config) throws ServletException {
    super.init(config);
  }

  public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    doPost(request, response);
  }

  public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    String logout = request.getParameter("logout");
    if(logout!=null){
        request.getSession().removeAttribute("user");
        response.sendRedirect("index.jsp");      
    }else{
      String usr = request.getParameter("user");
      String pass = request.getParameter("pass");
      if(usr.equals(user) && pass.equals(password)){
        request.getSession().setAttribute("user", usr);
      }else if(usr.equals(adm) && pass.equals(passAdm)){
        request.getSession().setAttribute("user", usr);
      }else{
        String err = "Invalid password!";
        if(!usr.equals(user)&&!usr.equals(adm)){
          err = "Invalid user!";
        }
        response.sendRedirect("index.jsp?err="+err);
      }
      
      if(request.getSession().getAttribute("user")!=null){
        response.sendRedirect("system/hosts.jsp");
      }
    }
  }
}