Hi sourceforge users,
Here's some instruction to install wMibBrowser on your app server.
First, deploy the ear file to your app server. Then put the mibs file to anywhere on ur server 
(By Default, you have to put the files on D:\mibs).
Here's 2 files that you should changes, if you want to change a user and password for wMibBrowser users,
or change mibs files path
1. DwSnmpMibTreeGUI.java
   on line 109, change this path to anywhere on your server (if the projectdir is still "D:/" 
   then you have to put the files on "D:\mibs")
      projectdir = "D:/";

2. ServletLogin.java
   make a change to this line, then recompile the file and put the file on your app server.
   private final String user = "user";
   private final String password = "userMib";
   private final String adm = "adminMib";
   private final String passAdm = "`admin123";
