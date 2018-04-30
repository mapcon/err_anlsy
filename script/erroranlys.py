# coding:utf8
"""
todo
"""

MAX_SHOW = -1

def TransErrInfo(sErr):
	'''
	报错格式化，将str型数据字典化
	:param sErr:
	:return: dErr{
		sErrTime
		sErrType
		sErrStack
	}
	'''
	dErr = {}
	sErrList = sErr.split("\n")
	if len(sErrList) == 1:
		dErr["sErrTime"] = ""
		dErr["sErrType"] = sErrList.pop(0)
		dErr["sErrStack"] = dErr["sErrType"]
	else:
		sTime = sErrList.pop(0)
		dErr["sErrTime"] = sTime.strip()
		dErr["sErrType"] = sErrList.pop().strip()
		sErrStack = ""
		for sErr in sErrList:
			sErrStack += "%s\n" % sErr.strip()
		dErr["sErrStack"] = sErrStack + dErr["sErrType"]
	return dErr

def GetReport(dDayData):
	# 将多天数据汇总
	dTotalList = []
	for dDataList in dDayData.itervalues():
		for dData in dDataList:
			sErr = dData["sErr"]
			dErr = TransErrInfo(sErr)
			dTotalList.append(dErr)

	# 分类统计
	dTypeResult = {}
	dStackResult = {}
	for dData in dTotalList:
		sErrType = dData["sErrType"]
		if sErrType not in dTypeResult:
			dTypeResult[sErrType] = 0
		dTypeResult[sErrType] += 1
		sErrStack = dData["sErrStack"]
		if sErrStack not in dStackResult:
			dStackResult[sErrStack] = 0
		dStackResult[sErrStack] += 1

	sResult = "# 统计报告 #\n"
	sResult += "周期内报错共`%d`个\n" % len(dTotalList)
	# 相同类型报告：分布&罗列
	sResult += "## 同类型报错分布 ##\n"
	tCountList = []
	for sType, iCount in dTypeResult.iteritems():
		tCountList.append((iCount, sType))
	tCountList.sort(reverse=True)
	for iCount, sType in tCountList:
		sResult += "  - <%d> %s\n" % (iCount, sType)
	sResult += "\n" * 5

	# 相同堆栈报告：hash罗列
	sResult += "## 相同报错分布 ##\n"
	tCountList = []
	for sErr, iCount in dStackResult.iteritems():
		tCountList.append((iCount, sErr))
	tCountList.sort(reverse=True)
	for iCount, sErr in tCountList:
		sResult += "  - <%d> %s\n" % (iCount, hash(sErr))
		sResult += "```\n%s\n```\n" % sErr
	sResult += "\n" * 5

	return sResult





