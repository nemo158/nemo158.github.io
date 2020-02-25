# -*- coding: utf-8 -*-
import os
import sys
import time

#reload(sys)
#sys.setdefaultencoding('utf8')

path = "D:\网站备份\source2\_posts"
for root, dir, files in os.walk(path):
    for file in files:
        full_path = os.path.join(root, file)
        mtime = os.stat(full_path).st_mtime
        file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        print("{0} 修改时间是: {1}".format(full_path,file_modify_time))
        data=''
        haveUpdated_flag=0
        freshTime=0
        same_flag=0
        with open(full_path,encoding='utf-8') as f:
            headCnt=0 #用来检验头部位置
            for line in f.readlines():
                if('---\n'==line):
                    if(0==headCnt):
                        headCnt+=1
                    elif(1==headCnt and 0==haveUpdated_flag):
                        headCnt+=1
                        data+='updated: '+file_modify_time+'  \n'
                if(0==line.find('updated:')):
                    haveUpdated_flag=1
                    file_modify_time_inner=line #将其保存在for外部
                    line='updated: '+file_modify_time+'  \n'
                if(0==line.find('<!-- freshTime=')):
                    freshTime=line
                data+=line
        
        #file_modify_time='updated: '+file_modify_time
        file_modify_time='<!-- freshTime='+file_modify_time+'-->'
        if(file_modify_time==freshTime):#原文中有updated属性，此处比较是否再次有修改
            print(file+file_modify_time+file_modify_time_inner)
            continue
        with open(full_path,'r+',encoding='utf-8') as f:
            data+='\n<!-- freshTime='+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))+'-->'
            f.writelines(data)
