/***************************************************************************
 *	Copyright (C) 2008 Citrix Systems                                      *
 *	bob.hudson@citrix.com                                                  *
 *                                                                         *
 *	This program is free software; you can redistribute it and/or modify   *
 *	it under the terms of the GNU General Public License as published by   *
 *	the Free Software Foundation; either version 2 of the License, or      *
 *	(at your option) any later version.                                    *
 *                                                                         *
 *	This program is distributed in the hope that it will be useful,        *
 *	but WITHOUT ANY WARRANTY; without even the implied warranty of         *
 *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
 *	GNU General Public License for more details.                           *
 *                                                                         *
 *	You should have received a copy of the GNU General Public License      *
 *	along with this program; if not, write to the                          *
 *	Free Software Foundation, Inc.,                                        *
 *	59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.              *
 *                                                                         *
 *	This utility parses a XenServer (4.x - 5.x) database file and lists    *
 *	class objects or components, thier data, and 'connecting' objects.     *
 *                                                                         *
 ***************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

#ifdef _WIN32
#include <io.h>
#include <windows.h>
#include <winbase.h>
#include <libxml\tree.h>
#include <libxml\parser.h>
#else
#include <stdbool.h>
#include <libxml/tree.h>
#include <libxml/parser.h>
#endif	// _WIN32

#ifdef _WIN32
#include "..\xenlib\database.h"
#else
#include "../xenlib/database.h"
#endif

#ifndef TRUE
#define TRUE	1
#endif
#ifndef FALSE
#define FALSE	0
#endif

#define PROGRAM_HEADER	"\ndbtool - XenServer database tool\n"	\
						"v0.1 (beta) 11/2008 [bob.hudson@citrix.com]\n\n"

// Global data
TABLE	*server;
char	*db_file = NULL;

#ifdef _WIN32
	#define BOOL		BOOLEAN
	#define	STRICMP		stricmp
	#define STRNICMP	strnicmp
#else
	#define BOOL		bool
	#define	STRICMP		strcasecmp
	#define STRNICMP	strncasecmp
#endif	// _WIN32
BOOL	dumpall = FALSE;
BOOL	templates = FALSE;
BOOL	isos = FALSE;
BOOL	verbose = FALSE;

char	*object = NULL;
char	*uuid = NULL;

int		parse_command_line(int argc, char **argv);
void	print_syntax(void);
void	print_available_objects(void);
int		verify_parameters(void);
void	dump_all(void);
void	list_uuid(void);
void	list_object(void);
int		format_print_entry(ENTRY *entry);
void	print_entry(int index, int num, ENTRY *entry);

int		get_max_label(ENTRY *entry);
void	print_aligned(int pad, char *label, int maximum, char *value, BOOL cr);

void	print_Bond(int num, ENTRY *entry);
void	print_PBD(int num, ENTRY *entry);
void	print_PIF(int num, ENTRY *entry);
void	print_PIF_metrics(int num, ENTRY *entry);
void	print_SM(int num, ENTRY *entry);
void	print_SR(int num, ENTRY *entry);
void	print_VBD(int num, ENTRY *entry);
void	print_VBD_metrics(int num, ENTRY *entry);
void	print_VDI(int num, ENTRY *entry);
void	print_VIF(int num, ENTRY *entry);
void	print_VIF_metrics(int num, ENTRY *entry);
void	print_VLAN(int num, ENTRY *entry);
void	print_VM(int num, ENTRY *entry);
void	print_VM_guest_metrics(int num, ENTRY *entry);
void	print_VM_metrics(int num, ENTRY *entry);
void	print_VTPM(int num, ENTRY *entry);
void	print_console(int num, ENTRY *entry);
void	print_crashdump(int num, ENTRY *entry);
void	print_event(int num, ENTRY *entry);
void	print_host(int num, ENTRY *entry);
void	print_host_cpu(int num, ENTRY *entry);
void    print_host_crashdump(int num, ENTRY *entry);
void    print_host_metrics(int num, ENTRY *entry);
void    print_host_patch(int num, ENTRY *entry);
void    print_network(int num, ENTRY *entry);
void    print_pool(int num, ENTRY *entry);
void    print_pool_patch(int num, ENTRY *entry);
void    print_schema_version(int num, ENTRY *entry);
void    print_session(int num, ENTRY *entry);
void    print_task(int num, ENTRY *entry);
void    print_user(int num, ENTRY *entry);
void    print_message(int num, ENTRY *entry);
void    print_data_source(int num, ENTRY *entry);
void    print_blob(int num, ENTRY *entry);

int
main(int argc, char **argv)
{
	// Parse command line
	if(parse_command_line(argc, argv) == -1){
		exit(1);
	}
	// Verify parameters
	if(verify_parameters() == -1){
		exit(1);
	}
	// Get database type and display
	printf("database type: ");
	switch(get_database_type(db_file)){
		case SQL_DB_TYPE:{
				printf("SQL - XS 4.x\n\n");
				break;
		}
		case XML_DB_TYPE:{
				printf("XML - XS 5.x\n\n");
				break;
		}
		case ERR_DB_TYPE:
		default:{
			printf("unknown or invalid file - aborting\n\n");
			exit(1);
		}
	}
	// Check for object or uuid - if neither exit
	if(dumpall == FALSE && !object && !uuid){
		return -1;
	}
	// Parse database and get TABLE server
	server = parse_database(db_file);
	if(!server){
		switch(get_parse_error()){
			case DB_SQL_DLL_ERR:{
				printf("error loading/using sqlite3.dll\n");
				break;
			}
			case DB_XML_DLL_ERR:{
				printf("error loading/using libxml2.dll, zlib1.dll, and/or iconv.dll\n");
				break;
			}
			default:{
				printf("error parsing database\n");
				break;
			}
		}
		exit(-1);
	}
	// Check for dump all
	if(dumpall == TRUE){
		dump_all();
	}else if(uuid){
		list_uuid();
	}else{
		list_object();
	}
	// Free up table
	free_table();
	exit(0);
}

int
parse_command_line(int argc, char **argv)
{
	int		i;

	if(argc < 2){
		print_syntax();
		return -1;
	}

	for(i=1; i<argc; i++){

		if(!STRICMP("-a", argv[i])){
			dumpall = TRUE;
			verbose = TRUE;
			templates = TRUE;
			isos = TRUE;
			continue;
		}else if(!STRICMP("-l", argv[i])){
			print_available_objects();
			exit(0);
		}else if(!STRICMP("-ver", argv[i])){
			printf("%s", PROGRAM_HEADER);
			exit(0);
		}else if(!STRICMP("-v", argv[i])){
			verbose = TRUE;
			continue;
		}else if(!STRICMP("-t", argv[i])){
			templates = TRUE;
			continue;
		}else if(!STRICMP("-i", argv[i])){
			isos = TRUE;
			continue;
		}else if(!STRNICMP("-o", argv[i], 2)){
			if(strlen(argv[i]) > 2){
				object = argv[i] + 2;
			}else{
				if((i + 1) < argc){
					object = argv[i + 1];
					i++;
				}else{
					print_syntax();
					return -1;
				}
			}
		}else if(!STRNICMP("-u", argv[i], 2)){
			if(strlen(argv[i]) > 2){
				uuid = argv[i] + 2;
			}else{
				if((i + 1) < argc){
					uuid = argv[i + 1];
					i++;
				}else{
					print_syntax();
					return -1;
				}
			}
		}else if(!(STRICMP("-h", argv[i])) || !(STRICMP("-help", argv[i])) ||
				 !(STRICMP("/h", argv[i])) || !(STRICMP("/help", argv[i])) ||
				 !(STRICMP("/?", argv[i])) || !(STRICMP("?", argv[i])) ||
				 !(STRICMP("h", argv[i])) || !(STRICMP("help", argv[i]))){
			print_syntax();
			return -1;
			continue;
		}else if(!db_file){
			db_file = argv[i];
			continue;
		}else{
			printf("invalid option: %s\n", argv[i]);
			return -1;
		}
	}

	return 0;
}

void
print_syntax(void)
{
	printf(	"syntax: dbtool [options] database_file\n"
			"   options: -a          dump all\n"
			"            -i          list ISOs and CDs\n"
			"            -l          list available objects\n"
			"            -o object   list by object\n"
			"            -t          list VM templates\n"
			"            -u uuid     list by uuid\n"
			"            -v          verbose\n"
			"            -ver        version\n");
}

void
print_available_objects(void)
{
	printf(	"available objects (not case-sensitive):\n\n"
			"  object                 description\n"
			"  --------------------------------------------------------\n"
			"  Bond                   network interface bond\n"
			"  PBD                    physical block device\n"
			"  PIF_metrics            physical network interface metrics\n"
			"  PIF                    physical network interface\n"
			"  SM                     storage manager plugin\n"
			"  SR                     storage repository\n"
			"  VBD                    virtual block device\n"
			"  VBD_metrics            virtual block device metrics\n"
			"  VDI                    virtual disk interface\n"
			"  VIF                    virtual network interface\n"
			"  VIF_metrics            virtual network interface metrics\n"
			"  VLAN                   virtual local area network\n"
			"  VM                     virtual machine\n"
			"  VM_guest_metrics       virtual machine guest metrics\n"
			"  VM_metrics             virtual machine metrics\n"
			"  VTPM                   virtual trusted platform module\n"
			"  console                virtual machine console\n"
			"  crashdump              virtaul machine crashdump\n"
			"  event                  asynchronous event\n"
			"  host                   physical host\n"
			"  host_cpu               physical CPU\n"
			"  host_crashdump         host crashdump\n"
			"  host_metrics           host metrics\n"
			"  host_patch             host patch\n"
			"  network                virtual network\n"
			"  pool                   pool of hosts\n"
			"  pool_patch             pool patch\n"
			"  schema_version         ???\n"
			"  session                session\n"
			"  task                   asynchronous task\n"
			"  user                   user\n"
			"  message                message\n"
			"  data_source            data source\n"
			"  blob                   blob\n");
}

int
verify_parameters(void)
{
	// Database file
	if(db_file == NULL){
		return -1;
	}
	if(dumpall == TRUE){
		return 0;
	}
	return 0;
}

void
dump_all(void)
{
	int	i;

	for(i=0; i<TABLE_COUNT; i++){
		object = server[i].name;
		list_object();
	}
}

void
list_uuid(void)
{
	TABLE			*tab;
	ENTRY			*entry;
	char			*luuid;
	int				i, x;

	for(i=0; i<TABLE_COUNT; i++){
		// Get table entry pointer
		tab = &server[i];
		// For each entry
		for(x=0; x<tab->entry_count; x++){
			// Get entry
			entry = tab->entry + x;
			// Try to get a uuid
			if((luuid = get_record_value(entry, "uuid"))){
				// Check for specified uuid
				if(!strcmp(luuid, uuid)){
					print_entry(i, 0, entry);
					return;
				}
			}
		}
	}
	printf("uuid: %s not found\n", uuid);
}

void
list_object(void)
{
	int		i, x;
	TABLE	*tab;
	ENTRY	*entry;

	for(i=0; i<TABLE_COUNT; i++){
		if(!STRICMP(server[i].name, object)){
			// Get table entry pointer
			tab = &server[i];
			printf("%s count: %d\n", tab->name, tab->entry_count);
			// For each entry
			for(x=0; x<tab->entry_count; x++){
				// Get entry
				entry = tab->entry + x;
				// Print entry
				print_entry(i, x, entry);
			}
		}
	}
}

//
// Prints any name__label first followed by the uuid
// Skips any ref or _ref labels
// Returns maximum from get_max_label function
// 
int
format_print_entry(ENTRY *entry) 
{
	int		i, maximum = 0, current;
	char	*str;

	// Check for entry and record count
	if((!entry) || (!entry->record_count)){
		return maximum;
	}

	// Get maximum label string
	maximum = get_max_label(entry);

	// List any name__label first
	str = get_record_value(entry, "name__label");
	if(str){
		printf("  name__label:");
		for(current = 11; current < maximum; current++){
			printf(" ");
		}
		printf("%s\n", str);
	}
	// List uuid second to name__label
	printf("  uuid:");
	for(current = 4; current < maximum; current++){
		printf(" ");
	}
	printf("%s\n", get_record_value(entry, "uuid"));

	if(verbose == FALSE){
		return maximum;
	}

	// List all records
	for(i=0; i<entry->record_count; i++){
		// Skip name__label
		if(!strcmp(entry->record[i].label, "name__label")){
			continue;
		}
		// Skip uuid
		if(!strcmp(entry->record[i].label, "uuid")){
			continue;
		}
		// Skip ref or _ref
		if(strstr(entry->record[i].label, "ref")){
			continue;
		}
		// Skip OpaqueRef
		if(strstr(entry->record[i].value, "OpaqueRef")){
			continue;
		}
		current = strlen(entry->record[i].label);
		printf("  %s:", entry->record[i].label);
		for(; current < maximum; current++){
			printf(" ");
		}
		printf("%s\n", entry->record[i].value);
	}
	return maximum;
}

void
print_entry(int index, int num, ENTRY *entry)
{
	switch(index){
		case Bond:		        print_Bond(num, entry);				return;
		case PBD:		        print_PBD(num, entry);				return;
		case PIF:		        print_PIF(num, entry);				return;
		case PIF_metrics:		print_PIF_metrics(num, entry);		return;
		case SM:		        print_SM(num, entry);				return;
		case SR:		        print_SR(num, entry);		        return;
		case VBD:		        print_VBD(num, entry);		        return;
		case VBD_metrics:       print_VBD_metrics(num, entry);		return;
		case VDI:		        print_VDI(num, entry);		        return;
		case VIF:		        print_VIF(num, entry);		        return;
		case VIF_metrics:       print_VIF_metrics(num, entry);		return;
		case VLAN:				print_VLAN(num, entry);				return;
		case VM:				print_VM(num, entry);				return;
		case VM_guest_metrics:	print_VM_guest_metrics(num, entry);	return;
		case VM_metrics:		print_VM_metrics(num, entry);		return;
		case VTPM:				print_VTPM(num, entry);				return;
		case console:			print_console(num, entry);			return;
		case crashdump:			print_crashdump(num, entry);		return;
		case event:				print_event(num, entry);			return;
		case host:				print_host(num, entry);				return;
		case host_cpu:			print_host_cpu(num, entry);			return;
		case host_crashdump:	print_host_crashdump(num, entry);   return;
		case host_metrics:      print_host_metrics(num, entry);     return;
		case host_patch:        print_host_patch(num, entry);       return;
		case network:           print_network(num, entry);			return;
		case pool:              print_pool(num, entry);         	return;
		case pool_patch:        print_pool_patch(num, entry);       return;
		case schema_version:    print_schema_version(num, entry);   return;
		case session:           print_session(num, entry);			return;
		case task:              print_task(num, entry);				return;
		case user:              print_user(num, entry);				return;
		case message:           print_message(num, entry);			return;
		case data_source:       print_data_source(num, entry);		return;
		case blob:              print_blob(num, entry);				return;
	}
}

void
print_Bond(int num, ENTRY *entry)
{
	BOND_RELATION	*rel;
	int				i, maximum;

	printf("Bond");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List master PIF
	print_aligned(2, "master PIF:", maximum, get_record_value(rel->PIF_master, "device_name"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->PIF_master, "uuid"), TRUE);

	// List slave PIFs
	for(i=0; i<rel->pif_slave_count; i++){
		print_aligned(2, "slave PIF:", maximum, get_record_value(rel->PIF_slave[i], "device_name"), TRUE);
		print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->PIF_slave[i], "uuid"), TRUE);
	}
}

void
print_PBD(int num, ENTRY *entry)
{
	PBD_RELATION	*rel;
	int				maximum;

	printf("PBD");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List host and SR
	print_aligned(2, "host:", maximum, get_record_value(rel->host, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host, "uuid"), TRUE);
	print_aligned(2, "SR:", maximum, get_record_value(rel->SR, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->SR, "uuid"), TRUE);
}

void
print_PIF(int num, ENTRY *entry)
{
	PIF_RELATION	*rel;
	BOND_RELATION	*bond = NULL;
	VLAN_RELATION	*vlan = NULL;
	ENTRY			*bond_pif = NULL;
	ENTRY			*tagged_pif = NULL;
	ENTRY			*untagged_pif = NULL;
	int				maximum;

	printf("PIF");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List host
	print_aligned(2, "host:", maximum, get_record_value(rel->host, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host, "uuid"), TRUE);

	// List network
	print_aligned(2, "network:", maximum, get_record_value(rel->network, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host, "uuid"), TRUE);

	// Get bond
	if(rel->bond_slave_of){
		bond = rel->bond_slave_of->relation;
	}
	if(bond){
		bond_pif = bond->PIF_master;
	}
	// Get vlan
	if(rel->VLAN_master_of){
		vlan = rel->VLAN_master_of->relation;
	}
	if(vlan){
		tagged_pif = vlan->PIF_tagged;
		untagged_pif = vlan->PIF_untagged;
	}
	// List bond slave of
	print_aligned(2, "bond slave of:", maximum, get_record_value(bond_pif, "device_name"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(bond_pif, "uuid"), TRUE);

	// List VLAN master of
	if(vlan){
		printf("  VLAN master of\n");
		print_aligned(4, "tagged:", maximum - 2, get_record_value(tagged_pif, "device_name"), TRUE);
		print_aligned(6, "uuid:", maximum - 4, get_record_value(tagged_pif, "uuid"), TRUE);
		print_aligned(4, "untagged:", maximum - 2, get_record_value(untagged_pif, "device_name"), TRUE);
		print_aligned(6, "uuid:", maximum - 4, get_record_value(untagged_pif, "uuid"), TRUE);
	}
}

void
print_PIF_metrics(int num, ENTRY *entry)
{
	ENTRY	*pif;
	char	*_ref;
	int		i, x, maximum;

	printf("PIF_metrics");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	maximum = format_print_entry(entry);

	// List PIF
	_ref = get_record_value(entry, "_ref");
	for(i=0; i<server[PIF].entry_count; i++){
		pif = server[PIF].entry + i;
		for(x=0; x<pif->record_count; x++){
			if(!strcmp(_ref, get_record_value(pif, "metrics"))){
				print_aligned(2, "PIF:", maximum, get_record_value(pif, "device_name"), TRUE);
			}
		}
	}
}

void
print_SM(int num, ENTRY *entry)
{
	printf("SM");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_SR(int num, ENTRY *entry)
{
	ENTRY	*vdi;
	ENTRY	*pbd;
	char	*_ref;
	int		i, x, maximum;

	printf("SR");
	if(object){
		// Check for isos
		if(isos == FALSE){
			if(!strcmp("iso", get_record_value(entry, "content_type"))){
				printf(" %d (ISO)\n", num);
				return;
			}
		}
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	maximum = format_print_entry(entry);

	// Get SR _ref
	_ref = get_record_value(entry, "_ref");

	// List PBDs
	for(i=0; i<server[PBD].entry_count; i++){
		pbd = server[PBD].entry + i;
		for(x=0; x<pbd->record_count; x++){
			if(!strcmp(_ref, get_record_value(pbd, "SR"))){
				print_aligned(2, "PBD uuid:", maximum, get_record_value(pbd, "uuid"), TRUE);
				break;
			}
		}
	}

	// List VDIs
	for(i=0; i<server[VDI].entry_count; i++){
		vdi = server[VDI].entry + i;
		for(x=0; x<vdi->record_count; x++){
			if(!strcmp(_ref, get_record_value(vdi, "SR"))){
				print_aligned(2, "VDI:", maximum, get_record_value(vdi, "name__label"), TRUE);
				print_aligned(4, "uuid:", maximum - 2, get_record_value(vdi, "uuid"), TRUE);
				break;
			}
		}
	}
}

void
print_VBD(int num, ENTRY *entry)
{
	VBD_RELATION	*rel;
	int				maximum;

	printf("VBD");
	if(object){
		// Check for isos
		if(isos == FALSE){
			if(!strcmp("CD", get_record_value(entry, "type"))){
				printf(" %d (ISO)\n", num);
				return;
			}
		}
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List VM
	if(rel->VM){
		print_aligned(2, "VM:", maximum, get_record_value(rel->VM, "name__label"), TRUE);
		print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VM, "uuid"), TRUE);
	}

	// List VDI
	if(rel->VDI){
		print_aligned(2, "VDI:", maximum, get_record_value(rel->VDI, "name__label"), TRUE);
		print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VDI, "uuid"), TRUE);
	}

}

void
print_VBD_metrics(int num, ENTRY *entry)
{
	ENTRY	*vbd;
	char	*_ref;
	int		i, x, maximum;

	printf("VBD_metrics");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	maximum = format_print_entry(entry);

	// List VBDs
	_ref = get_record_value(entry, "_ref");
	for(i=0; i<server[VBD].entry_count; i++){
		vbd = server[VBD].entry + i;
		for(x=0; x<vbd->record_count; x++){
			if(!strcmp(_ref, get_record_value(vbd, "metrics"))){
				print_aligned(2, "VBD:", maximum, get_record_value(vbd, "device"), TRUE);
			}
		}
	}
}

void
print_VDI(int num, ENTRY *entry)
{
	VDI_RELATION	*rel;
	ENTRY			*vbd;
	char			*_ref;
	int				i, x, maximum;

	printf("VDI");
	if(object){
		// Check for isos
		if(isos == FALSE){
			rel = entry->relation;
			if(!strcmp("iso", get_record_value(rel->SR, "type"))){
				printf(" %d (ISO)\n", num);
				return;
			}
		}
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List SR
	print_aligned(2, "SR:", maximum, get_record_value(rel->SR, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->SR, "uuid"), TRUE);

	// List VDI_parent
	if(rel->VDI_parent){
		print_aligned(2, "VDI parent:", maximum, get_record_value(rel->VDI_parent, "name__label"), TRUE);
		print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VDI_parent, "uuid"), TRUE);
	}

	// List VDI_snapshot_of
	if(rel->VDI_snapshot_of){
		print_aligned(2, "VDI snapshot of:", maximum, get_record_value(rel->VDI_snapshot_of, "name__label"), TRUE);
		print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VDI_snapshot_of, "uuid"), TRUE);
	}
	_ref = get_record_value(entry, "_ref");

	// List VBDs
	for(i=0; i<server[VBD].entry_count; i++){
		vbd = server[VBD].entry + i;
		for(x=0; x<vbd->record_count; x++){
			if(!strcmp(_ref, get_record_value(vbd, "VDI"))){
				print_aligned(2, "VBD:", maximum, get_record_value(vbd, "userdevice"), TRUE);
				print_aligned(4, "uuid:", maximum - 2, get_record_value(vbd, "uuid"), TRUE);
				break;
			}
		}
	}
}

void
print_VIF(int num, ENTRY *entry)
{
	VIF_RELATION	*rel;
	ENTRY			*pif;
	char			*_ref;
	int				i, x, maximum;

	printf("VIF");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List VM
	print_aligned(2, "VM:", maximum, get_record_value(rel->VM, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VM, "uuid"), TRUE);

	// List network
	print_aligned(2, "network:", maximum, get_record_value(rel->network, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->network, "uuid"), TRUE);

	//
	// Extra info
	//

	// List bridge
	print_aligned(2, "bridge:", maximum, get_record_value(rel->network, "bridge"), TRUE);
	_ref = get_record_value(rel->network, "_ref");

	// List PIFs
	for(i=0; i<server[PIF].entry_count; i++){
		pif = server[PIF].entry + i;
		for(x=0; x<pif->record_count; x++){
			if(!strcmp(_ref, get_record_value(pif, "network"))){
				print_aligned(2, "PIF device:", maximum, get_record_value(pif, "device_name"), TRUE);
				print_aligned(4, "uuid:", maximum - 2, get_record_value(pif, "uuid"), TRUE);
				break;
			}
		}
	}
}

void
print_VIF_metrics(int num, ENTRY *entry)
{
	printf("VIF_metrics");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_VLAN(int num, ENTRY *entry)
{
	VLAN_RELATION	*rel;
	int				maximum;

	printf("VLAN");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	if(rel->PIF_tagged || rel->PIF_untagged){
		printf("  PIF device\n");
		print_aligned(4, "tagged:", maximum - 2, get_record_value(rel->PIF_tagged, "device_name"), TRUE);
		print_aligned(6, "uuid:", maximum - 4, get_record_value(rel->PIF_tagged, "uuid"), TRUE);
		print_aligned(4, "untagged:", maximum -2 , get_record_value(rel->PIF_untagged, "device_name"), TRUE);
		print_aligned(6, "uuid:", maximum - 4, get_record_value(rel->PIF_untagged, "uuid"), TRUE);
	}
}

void
print_VM(int num, ENTRY *entry)
{
	VM_RELATION		*rel;
	ENTRY			*vbd;
	ENTRY			*vif;
	ENTRY			*CONSOLE;
	char			*_ref;
	int				i, x, maximum;

	printf("VM");
	if(object){
		// Check for templates
		if(templates == FALSE){
			if(!strcmp("true", get_record_value(entry, "is_a_template"))){
				printf(" %d (template)\n", num);
				return;
			}
		}
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List hosts
	print_aligned(2, "host resident:", maximum, get_record_value(rel->host_resident_on, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host_resident_on, "uuid"), TRUE);
	print_aligned(2, "host affinity:", maximum, get_record_value(rel->host_affinity, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host_affinity, "uuid"), TRUE);
	print_aligned(2, "host scheduled:", maximum, get_record_value(rel->host_scheduled_to_be_resident_on, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host_scheduled_to_be_resident_on, "uuid"), TRUE);

	// List VMs
	print_aligned(2, "VM snapshot of:", maximum, get_record_value(rel->VM_snapshot_of, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VM_snapshot_of, "uuid"), TRUE);
	print_aligned(2, "VM metrics uuid:", maximum, get_record_value(rel->VM_metrics, "uuid"), TRUE);
	print_aligned(2, "VM guest metrics uuid:", maximum, get_record_value(rel->VM_guest_metrics, "uuid"), TRUE);

	// List VDI suspend
	print_aligned(2, "VDI suspend:", maximum, get_record_value(rel->VDI_suspend, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VDI_suspend, "uuid"), TRUE);

	_ref = get_record_value(entry, "_ref");

	// List VBDs
	for(i=0; i<server[VBD].entry_count; i++){
		vbd = server[VBD].entry + i;
		for(x=0; x<vbd->record_count; x++){
			if(!strcmp(_ref, get_record_value(vbd, "VM"))){
				print_aligned(2, "VBD device", maximum, get_record_value(vbd, "device"), TRUE);
				print_aligned(4, "uuid:", maximum - 2, get_record_value(vbd, "uuid"), TRUE);
				break;
			}
		}
	}

	// List VIFs
	for(i=0; i<server[VIF].entry_count; i++){
		vif = server[VIF].entry + i;
		for(x=0; x<vif->record_count; x++){
			if(!strcmp(_ref, get_record_value(vif, "VM"))){
				print_aligned(2, "VIF device:", maximum, get_record_value(vif, "device"), TRUE);
				print_aligned(4, "uuid:", maximum - 2, get_record_value(vif, "uuid"), TRUE);
				break;
			}
		}
	}

	// List consoles
	for(i=0; i<server[console].entry_count; i++){
		CONSOLE = server[console].entry + i;
		for(x=0; x<CONSOLE->record_count; x++){
			if(!strcmp(_ref, get_record_value(CONSOLE, "VM"))){
				print_aligned(2, "console uuid:", maximum, get_record_value(CONSOLE, "uuid"), TRUE);
				break;
			}
		}
	}
}

void
print_VM_guest_metrics(int num, ENTRY *entry)
{
	printf("VM_guest_metrics");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_VM_metrics(int num, ENTRY *entry)
{
	ENTRY	*vm;
	char	*_ref;
	int		i, x, maximum;

	printf("VM_metrics");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	maximum = format_print_entry(entry);

	// List VM
	_ref = get_record_value(entry, "_ref");
	for(i=0; i<server[VM].entry_count; i++){
		vm = server[VM].entry + i;
		for(x=0; x<vm->record_count; x++){
			if(!strcmp(_ref, get_record_value(vm, "metrics"))){
				// Check for templates
				if(templates == FALSE){
					if(!strcmp("true", get_record_value(vm, "is_a_template"))){
						continue;
					}
					print_aligned(2, "VM:", maximum, get_record_value(vm, "name__label"), TRUE);
					print_aligned(4, "uuid:", maximum - 2, get_record_value(vm, "uuid"), TRUE);
					break;
				}
			}
		}
	}
}

void
print_VTPM(int num, ENTRY *entry)
{
	VTPM_RELATION	*rel;
	int				maximum;

	printf("VTPM");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List VMs
	print_aligned(2, "VM:", maximum, get_record_value(rel->VM, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VM, "uuid"), TRUE);
	print_aligned(2, "VM backend:", maximum, get_record_value(rel->VM_backend, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VM_backend, "uuid"), TRUE);
}

void
print_console(int num, ENTRY *entry)
{
	console_RELATION	*rel;
	int					maximum;

	printf("console");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List VM
	print_aligned(2, "VM:", maximum, get_record_value(rel->VM, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VM, "uuid"), TRUE);
}

void
print_crashdump(int num, ENTRY *entry)
{
	crashdump_RELATION	*rel;
	int					maximum;

	printf("crashdump");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List VM
	print_aligned(2, "VM:", maximum, get_record_value(rel->VM, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VM, "uuid"), TRUE);

	// List VDI
	print_aligned(2, "VDI:", maximum, get_record_value(rel->VDI, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->VDI, "uuid"), TRUE);
}

void
print_event(int num, ENTRY *entry)
{
	printf("event");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_host(int num, ENTRY *entry)
{
	host_RELATION	*rel;
	ENTRY			*pbd;
	ENTRY			*pif;
	char			*_ref;
	int		 		i, x, maximum;

	printf("host");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	_ref = get_record_value(entry, "_ref");

	// List SRs
	print_aligned(2, "SR suspend image:", maximum, get_record_value(rel->SR_suspend_image, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->SR_suspend_image, "uuid"), TRUE);
	print_aligned(2, "SR crash dump:", maximum, get_record_value(rel->SR_crash_dump, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->SR_crash_dump, "uuid"), TRUE);

	// List metrics
	print_aligned(2, "metrics:", maximum, get_record_value(rel->host_metrics, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host_metrics, "uuid"), TRUE);

	// List PBDs
	for(i=0; i<server[PBD].entry_count; i++){
		pbd = server[PBD].entry + i;
		for(x=0; x<pbd->record_count; x++){
			if(!strcmp(_ref, get_record_value(pbd, "host"))){
				print_aligned(2, "PBD uuid:", maximum, get_record_value(pbd, "uuid"), TRUE);
				break;
			}
		}
	}

	// List PIFs
	for(i=0; i<server[PIF].entry_count; i++){
		pif = server[PIF].entry + i;
		for(x=0; x<pif->record_count; x++){
			if(!strcmp(_ref, get_record_value(pif, "host"))){
				print_aligned(2, "PIF:", maximum, get_record_value(pif, "device_name"), TRUE);
				print_aligned(4, "uuid:", maximum - 2, get_record_value(pif, "uuid"), TRUE);
				break;
			}
		}
	}
}

void
print_host_cpu(int num, ENTRY *entry)
{
	host_cpu_RELATION	*rel;
	int		 		   	maximum;

	printf("host_cpu");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List host
	print_aligned(2, "host:", maximum, get_record_value(rel->host, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host, "uuid"), TRUE);
}

void
print_host_crashdump(int num, ENTRY *entry)
{
	host_crashdump_RELATION		*rel;
	int		 		   			maximum;

	printf("host_crashdump");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List host
	print_aligned(2, "host:", maximum, get_record_value(rel->host, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host, "uuid"), TRUE);
}

void
print_host_metrics(int num, ENTRY *entry)
{
	printf("host_metrics");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_host_patch(int num, ENTRY *entry)
{
	host_patch_RELATION		*rel;
	int		   	   			maximum;

	printf("host_patch");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List host
	print_aligned(2, "host:", maximum, get_record_value(rel->host, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host, "uuid"), TRUE);

	// List pool patch
	print_aligned(2, "pool patch:", maximum, get_record_value(rel->pool_patch, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->pool_patch, "uuid"), TRUE);
}

void
print_network(int num, ENTRY *entry)
{
	ENTRY	*pif;
	ENTRY	*vif;
	char	*_ref;
	int		i, x, maximum;

	printf("network");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	maximum = format_print_entry(entry);

	_ref = get_record_value(entry, "_ref");

	// List PIFs
	for(i=0; i<server[PIF].entry_count; i++){
		pif = server[PIF].entry + i;
		for(x=0; x<pif->record_count; x++){
			if(!strcmp(_ref, get_record_value(pif, "network"))){
				print_aligned(2, "PIF:", maximum, get_record_value(pif, "device_name"), TRUE);
				print_aligned(4, "uuid:", maximum - 2, get_record_value(pif, "uuid"), TRUE);
				break;
			}
		}
	}

	// List VIFs
	for(i=0; i<server[VIF].entry_count; i++){
		vif = server[VIF].entry + i;
		for(x=0; x<vif->record_count; x++){
			if(!strcmp(_ref, get_record_value(vif, "network"))){
				print_aligned(2, "VIF:", maximum, get_record_value(vif, "device"), TRUE);
				print_aligned(4, "uuid:", maximum - 2, get_record_value(vif, "uuid"), TRUE);
				break;
			}
		}
	}
}

void
print_pool(int num, ENTRY *entry)
{
	pool_RELATION		*rel;
	int	   	   			maximum;

	printf("pool");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List host master
	print_aligned(2, "host master:", maximum, get_record_value(rel->host_master, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host_master, "uuid"), TRUE);

	// List SRs
	print_aligned(2, "SR default:", maximum, get_record_value(rel->SR_default, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->SR_default, "uuid"), TRUE);
	print_aligned(2, "SR suspend image:", maximum, get_record_value(rel->SR_suspend_image, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->SR_suspend_image, "uuid"), TRUE);
	print_aligned(2, "SR crash dump:", maximum, get_record_value(rel->SR_crash_dump, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->SR_crash_dump, "uuid"), TRUE);
}

void
print_pool_patch(int num, ENTRY *entry)
{
	printf("pool_patch");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_schema_version(int num, ENTRY *entry)
{
	printf("schema_version");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_session(int num, ENTRY *entry)
{
	session_RELATION		*rel;
	int	   	   				maximum;

	printf("session");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List host
	print_aligned(2, "host:", maximum, get_record_value(rel->host, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host, "uuid"), TRUE);

	// List user
	print_aligned(2, "user:", maximum, get_record_value(rel->user, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->user, "uuid"), TRUE);
}

void
print_task(int num, ENTRY *entry)
{
	task_RELATION		*rel;
	int	   				maximum;

	printf("task");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}

	rel = entry->relation;
	maximum = format_print_entry(entry);

	// List session
	print_aligned(2, "session:", maximum, get_record_value(rel->session, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->session, "uuid"), TRUE);

	// List hosts
	print_aligned(2, "host resident on:", maximum, get_record_value(rel->host_resident_on, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host_resident_on, "uuid"), TRUE);
	print_aligned(2, "host forwarded:", maximum, get_record_value(rel->host_forwarded, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host_forwarded, "uuid"), TRUE);
	print_aligned(2, "host forwarded to:", maximum, get_record_value(rel->host_forwarded_to, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->host_forwarded_to, "uuid"), TRUE);

	// List subtask of
	print_aligned(2, "subtask of:", maximum, get_record_value(rel->task_subtask_of, "name__label"), TRUE);
	print_aligned(4, "uuid:", maximum - 2, get_record_value(rel->task_subtask_of, "uuid"), TRUE);

}

void
print_user(int num, ENTRY *entry)
{
	printf("user");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_message(int num, ENTRY *entry)
{
	printf("message");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_data_source(int num, ENTRY *entry)
{
	printf("data_source");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

void
print_blob(int num, ENTRY *entry)
{
	printf("blob");
	if(object){
		printf(" %d\n", num);
	}else{
		printf("\n");
	}
	format_print_entry(entry);
}

int
get_max_label(ENTRY *entry)
{
	int	i, len, maximum;

	maximum = 0;
	for(i=0; i<entry->record_count; i++){
		len = strlen(entry->record[i].label);
		maximum = (len > maximum) ? len : maximum;
	}
	return maximum + 1;
}

void
print_aligned(int pad, char *label, int maximum, char *value, BOOL cr)
{
	int		i, len;

	if(!label || !value){
		return;
	}

	len = strlen(label);

	for(i=0; i<pad; i++){
		printf(" ");
	}

	printf("%s", label);

	for(; len<=maximum; len++){
		printf(" ");
	}

	if(cr == TRUE){
		printf("%s\n", value);
	}else{
		printf("%s", value);
	}
}



