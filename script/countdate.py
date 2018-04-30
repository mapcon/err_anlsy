# coding:utf8
"""
日期计算相关
"""
import datetime


# >>接口
def GetDayList(sTime):
	'''
	获取指定时段内的每一天
	:param sTime: “YYMMDD”或“YYMMDD-YYMMDD”
	:return: 给出时段范围内每一天的YYMMDD列表
	'''
	tResult = sTime.split("-")
	sStartDay = tResult[0]
	if len(tResult) > 1:
		sEndDay = tResult[1]
	else:
		sEndDay = sStartDay
	return GenDayList(sStartDay, sEndDay)


# <<接口

def GenDates(b_date, days):
	import datetime
	day = datetime.timedelta(days=1)
	for i in range(days):
		yield b_date + day * i


def GetDateObj(sDay):  # YYMMDD -> datetimeobj
	return datetime.datetime.strptime(sDay, "%y%m%d")


def GenDayList(sStartDay, sEndDay):
	oStartDate = GetDateObj(sStartDay)
	oEndDate = GetDateObj(sEndDay)
	sDayList = []
	for oDate in GenDates(oStartDate, (oEndDate - oStartDate).days + 1):
		sDay = oDate.strftime("%y%m%d")
		sDayList.append(sDay)
	return sDayList
