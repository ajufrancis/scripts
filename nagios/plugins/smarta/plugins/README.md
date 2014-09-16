= Install lua

wget http://www.lua.org/ftp/lua-5.1.4.tar.gz
tar xvf lua-5.1.4.tar.gz
cd lua-5.1.4
make linux && make install

= Plugins

1. check_disk 检查磁盘是否满了
2. check_memory 检查内存占用
3. check_swap 检查内存占用
4. check_process 检查进程正常吗
5. check_log 检查日志大小
