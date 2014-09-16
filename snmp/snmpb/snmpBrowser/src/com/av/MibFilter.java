package com.av;

import java.io.IOException;
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class MibFilter implements Filter{
  public MibFilter() {
  }
  
  public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException{
    HttpServletRequest req = (HttpServletRequest)request;
    if(req.getSession().getAttribute("user")==null){
      ((HttpServletResponse)response).sendRedirect("./../index.jsp");
    }else{
      chain.doFilter(request, response);    
    }
  }
   
  public void destroy(){    
  }
  
  public void init(FilterConfig fc) throws ServletException{    
  }
}