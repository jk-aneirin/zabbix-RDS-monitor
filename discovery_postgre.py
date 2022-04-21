#coding=UTF-8
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest

import json,re,os,sys

DBInstanceIdList = []
DBInstanceIdDict = {}
ZabbixDataDict = {}

ID = "ID"
Secret = "Secret"

def GetRdsList(regionid):
    RdsRequest = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    RdsRequest.set_accept_format('json')
    clt = client.AcsClient(ID, Secret, regionid)
    #RdsInfo = clt.do_action(RdsRequest)
    RdsInfo = clt.do_action_with_exception(RdsRequest)
    for RdsInfoJson in (json.loads(RdsInfo))['Items']['DBInstance']:
        DBInstanceIdDict = {}
        try:
            DBInstanceIdDict["{#DBINSTANCEID}"] = RdsInfoJson['DBInstanceId']
            if re.match('^pgm', RdsInfoJson['DBInstanceId']):
                DBInstanceIdDict["{#DBINSTANCEDESCRIPTION}"] = RdsInfoJson['DBInstanceDescription']
                DBInstanceIdList.append(DBInstanceIdDict)
        except Exception, e:
            print Exception, ":", e
            print "Please check the RDS alias !Alias must not be the same as DBInstanceId！！！"

RegionIds = ['cn-beijing', 'cn-shenzhen']
for regionid in RegionIds:
    GetRdsList(regionid)
ZabbixDataDict['data'] = DBInstanceIdList
print json.dumps(ZabbixDataDict)
