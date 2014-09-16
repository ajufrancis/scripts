package com.av;
import com.dwipal.ISnmpResponseHandler;
import com.dwipal.SnmpOidValuePair;

public class MySnmpResponseHandler implements ISnmpResponseHandler{
  public String value = null;
  public boolean done = false;

  public void responseReceived(SnmpOidValuePair resp_values) {
    value = resp_values.value_str;
    done = true;
  }
  
  public void requestStats(int totalRequests, int totalResponses,
                           long timeInMillis) {
  }
}