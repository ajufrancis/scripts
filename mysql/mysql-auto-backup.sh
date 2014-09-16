#!/bin/bash
#数据库信息  
db_user=backup
db_passwd=pwd4backup  
db_host=localhost
#文件名  
file_name=`date +%Y%m%d`.sql
backup_dir=/data/backup/
#mysql编译后命令所在位置  
#mysql=/usr/local/mysql/bin/mysql  
#mysqldump=/usr/local/mysql/bin/mysqldump
 
#测试备份目录是否可写，如果不可写就报错退出  
test ! -w $backup_dir && echo "Error: $backup_dir is unwrite." && exit 0 
   
#测试备份目录中最新备份文件夹是否存在，如果不在就创建  
test ! -d "$backup_dir/backup.1/" && mkdir "$backup_dir/backup.1" 
   
#制定要备份的数据库  
for db in database_1 database_2 database_3 database_n  
do 
    $mysqldump -u $db_user -h $db_host -p$db_passwd --opt -B $db | gzip -6 > "$backup_dir/backup.1/$db.$file_name.gz"
done 
   
#检测最旧的备份数据库是否存在，如果在就删掉  
test -d "$backup_dir/backup.7/" && rm -rf "$backup_dir/backup.7" 
   
#循环修改备份数据库目录的编号，记录新旧程度  
for i in 6 5 4 3 2 1 0
do 
    if(test -d "$backup_dir"/backup."$int")  
    then  
        next_i=`expr $i + 1`  
        mv "$backup_dir"/backup."$i" "$backup_dir"/backup."$next_i" 
    fi  
done  
exit 0;
 
#过期用户:database4
