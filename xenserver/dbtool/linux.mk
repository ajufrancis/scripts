# dbtool Makefile

dbtool : dbtool.c
	gcc -O2 -o dbtool dbtool.c -l sqlite3 -l xml2 ../xenlib/database.a
	
.PHONY: clean

clean::
	/bin/rm -f dbtool
