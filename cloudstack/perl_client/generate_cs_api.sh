while read cmd
do
  if [ not -e cmds/${cmd}.pl ]
  then
    ls -l cmds/${cmd}.pl
  fi
done < ./cs_api_list_cmds.3.0.4.txt
