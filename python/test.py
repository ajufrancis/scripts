ld = ldap.initialize('ldap://localhost:1389')
user = "bjensen"
password = "hifalutin"
password = "hifalutin"
basedn = "ou=people,dc=example,dc=com"
filter = "(|(uid=" + user + "\*)(mail=" + user + "\*))"
results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)
for dn,entry in results:
  dn = str(dn)

ld.simple_bind_s(dn,password)
ld.whoami_s()
ld = ldap.initialize('ldap://localhost:1389')
name = "jensen"
ld.simple_bind_s()
basedn = "ou=people,dc=example,dc=com"
filter = "(|(cn=\*" + name + "\*)(sn=\*" + name + "\*))"
results = ld.search_s(basedn,ldap.SCOPE_SUBTREE,filter)

ldif_writer = ldif.LDIFWriter(sys.stdout)
for dn,entry in results:
  ldif_writer.unparse(dn,entry)
#http://ochiba77.blogspot.com/2011/10/how-to-set-up-web2py-ldap-with-windows.html
