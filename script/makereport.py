# coding:utf8
"""
生成分析报告
"""


def DoErrorAnlys(dDayData):
	'''
	报错分析，返回生成文档
	:param dDayData: {sYYMMDD: dDataList}
	:return: sMDContent md文档
	'''
	import erroranlys
	import markdown
	return markdown.markdown(erroranlys.GetReport(dDayData).decode("utf-8", errors='ignore')).encode("utf-8")


def DoGraphAnlys(dDayData):
	'''
	图表分析，返回生成文档
	:param dDayData: {sYYMMDD: dDataList}
	:return: sMDContent md文档
	'''
	import drawcharts
	return drawcharts.Draw(dDayData)


def StartAnlys(sTime):
	import countdate
	import genresult
	import os

	sDayList = countdate.GetDayList(sTime)
	dDayData = {}  # YYMMDD: dDayData
	import data
	for sDay in sDayList:
		dData = data.GetDayData(sDay)
		if dData is not None:
			dDayData[sDay] = dData
	print u"【开始分析】\n分析时段%s，共计%d天。已找到%d天数据" % (sTime, len(sDayList), len(dDayData))

	sErrMD = DoErrorAnlys(dDayData)
	sGraphMD = DoGraphAnlys(dDayData)
	sResultFilePath = os.path.join(os.getcwd(), "result_%s.html" % sTime)
	genresult.Gen(sResultFilePath, sErrMD, sGraphMD)


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
