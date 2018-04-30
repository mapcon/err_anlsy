# coding:utf8
"""
生成分析报告
"""


def StartAnlys(sTime):
	import countdate
	sDayList = countdate.GetDayList(sTime)
	dDayData = {} # YYMMDD: dDayData
	import data
	for sDay in sDayList:
		dData = data.GetDayData(sDay)
		if dData is not None:
			dDayData[sDay] = dData
	print u"分析时段%s，共计%d天。已找到%d天数据" % (sTime, len(sDayList), len(dDayData))


if __name__ == "__main__":
	sTime = ""
	while True:
		import re

		sInput = raw_input("请输入分析日期，如“180429”或“180427-180429”，Q退出：".decode("utf8").encode("gbk"))
		if sInput in ("Q", "q"):
			exit(0)
		if re.match("[0-9]{6}$", sInput) or re.match("[0-9]{6}-[0-9]{6}$", sInput):
			sTime = sInput
			break
	StartAnlys(sTime)
