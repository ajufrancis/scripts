# some nmake macros for Win32 apps development
!include <win32.mak>

# make the executable
all:	dbtool.exe

# compile
dbtool.obj:	dbtool.c
	$(cc) $(cflags) /c dbtool.c
	
# link
dbtool.exe:	dbtool.obj
	$(link) -out:dbtool.exe	\
		dbtool.obj	\
		..\xenlib\database.lib
#		advapi32.lib	\
#		shell32.lib
				
