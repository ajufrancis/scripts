#!/usr/bin/perl -w
my $database_oldformat_path = "/tmp/1124/1.txt";
my $database_line;
my @database_line_column;
my $database_line_column;
my $database_newformat_path = "/tmp/1124/11.txt";
open "database_oldformat_file","$database_oldformat_path";
#open "dababase_newformat_file","> $database_newformat_path";
# 读取每行
for $database_line (<database_oldformat_file>){
# print $database_line . "\n";
# 将每行按照空格分成4段
(@database_line_column)=split(" ",$database_line);
# 将第一段的ip地址按照小数点分开
(@ip_start) = split("\\.",$database_line_column[0]);
$ip_start_number = $ip_start[0]*256*256*256+$ip_start[1]*256*256+$ip_start[2]*256+$ip_start[3];
# 将第二段的ip地址按照小数点分开
(@ip_stop) = split("\\.",$database_line_column[1]);
$ip_stop_number = $ip_stop[0]*256*256*256+$ip_stop[1]*256*256+$ip_stop[2]*256+$ip_stop[3];
# 将第三段
$ip_areaname = $database_line_column[2];
# 将第四段拿出来作为 网络名称，比如 电信或者网通 或者 cznet
$ip_ispname = $database_line_column[3];
# 将上边四个： 起始IP地址、结束IP地址、地理信息、ISP信息 写到新的文件
open "database_newformat_file",">> $database_newformat_path";
syswrite("database_newformat_file","$ip_start_number $ip_stop_number $ip_areaname $ip_ispname\n");
close("database_newformat_file");
}
