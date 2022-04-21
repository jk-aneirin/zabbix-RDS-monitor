#coding=utf-8
#Auther：xwjr.com
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeResourceUsageRequest,DescribeDBInstancePerformanceRequest
import json,sys,datetime,os

ID = "ID"
Secret = "Secret"
RegionId = 'cn-shenzhen'
clt = client.AcsClient(ID, Secret, RegionId)


Type = sys.argv[1]
DBInstanceId = sys.argv[2]
Key = sys.argv[3]

# 阿里云返回的数据为UTC时间，因此要转换为东八区时间。其他时区同理。
UTC_End = datetime.datetime.today() - datetime.timedelta(hours=8)
UTC_Start = UTC_End - datetime.timedelta(minutes=5)

StartTime = datetime.datetime.strftime(UTC_Start, '%Y-%m-%dT%H:%MZ')
EndTime = datetime.datetime.strftime(UTC_End, '%Y-%m-%dT%H:%MZ')

def GetResourceUsage(DBInstanceId,Key):
    ResourceUsage = DescribeResourceUsageRequest.DescribeResourceUsageRequest()
    ResourceUsage.set_accept_format('json')
    ResourceUsage.set_DBInstanceId(DBInstanceId)
    ResourceUsageInfo = clt.do_action_with_exception(ResourceUsage)
    #print ResourceUsageInfo
    Info = (json.loads(ResourceUsageInfo))[Key]
    print Info

def GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime):
    Performance = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
    Performance.set_accept_format('json')
    Performance.set_DBInstanceId(DBInstanceId)
    Performance.set_Key(MasterKey)
    Performance.set_StartTime(StartTime)
    Performance.set_EndTime(EndTime)
    PerformanceInfo = clt.do_action_with_exception(Performance)
   # print PerformanceInfo
    Info = (json.loads(PerformanceInfo))
    Value = Info['PerformanceKeys']['PerformanceKey'][0]['Values']['PerformanceValue'][-1]['Value']
    print str(Value).split('&')[IndexNum]

if (Type == "Disk"):
    GetResourceUsage(DBInstanceId, Key)

elif (Type == "Performance"):
    #平均当前活跃连接数
    if (Key == "postgre_active_session"):
        IndexNum = 0
        MasterKey = "PolarDBConnections"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #当前连接总数
    elif (Key == "postgre_total_session"):
        IndexNum = 2
        MasterKey = "PolarDBConnections"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #平均等待连接数
    elif (Key == "postgre_waiting_connection"):
        IndexNum = 3
        MasterKey = "PolarDBConnections"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #每秒死锁数目
    elif (Key == "postgre_deadlocks_delta"):
        IndexNum = 1
        MasterKey = "PolarDBQPSTPS"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #每秒事务数目
    elif (Key == "postgre_tps"):
        IndexNum = 3
        MasterKey = "PolarDBQPSTPS"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #CPU使用率
    elif (Key == "postgre_cpu"):
        IndexNum = 0
        MasterKey = "PolarDBCPU"
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime)

    #内存使用率
    elif (Key == "postgre_memory"):
        MasterKey = "PolarDBMemory"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

    #执行时长超过5秒的SQL语句数目
    elif (Key == "postgre_five_seconds_executing_sqls"):
        MasterKey = "PolarDBLongSQL"
        IndexNum = 0
        GetPerformance(DBInstanceId, MasterKey, IndexNum, StartTime, EndTime)

