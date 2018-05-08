# coding:utf8
"""
xls解析逻辑
"""

TIMEFORMAT = "(%f-19-70*365)*86400-8*3600"
RESULT_TYPE_DICT = 1
RESULT_TYPE_LIST = 2
MAX_COL = 15  # 超过最大列数的会被忽略。最大行数是取连续非空行最大值
RE_HEX = "\\\\x([0-9a-f]{2})"


def FormatData(tPos, data, sSpecifiedType=None):  # 规整化
	try:
		if sSpecifiedType in ("str", "sDefault"):
			if data is None: # 缺省处理
				if sSpecifiedType == "sDefault":
					return "NULL"
				return ""

			if sSpecifiedType == "sDefault":
				if type(data) == float:
					if data == 0:
						data = "NULL"
					else:
						data = str(int(data))
				if data in ("", "0"):
					data = "NULL"

			data = data.replace("\"", "'") # 引号转换
			data_raw = data

			# 编码处理，解决gbk编码下"\\x"->"\x"的问题，然后统一转为utf8处理
			import re
			try:
				data = data.encode("gbk")
				sCharList = re.findall(RE_HEX, data)
				for sChar in sCharList:
					data = data.replace("\\x%s" % sChar, sChar.decode("hex"))
				data = data.decode("gbk").encode("utf8")
			except:
				data = data_raw.encode("utf8")
				print u"Warning: 编码混乱", data

			return data

		if sSpecifiedType == "time":
			if data is None:
				return 0
			return int(eval(TIMEFORMAT % data))

		if sSpecifiedType == "float" or type(data) == float:
			if data is None:
				return 0
			iData = int(data)
			if iData == data:
				return iData
			return data

		if sSpecifiedType in ("int", "iDefault"):
			if data is None:
				return 0

			if sSpecifiedType == "iDefault" and data == "None":
				data = "0"

			return int(data)
		return data
	except:
		print "wrong content in %s" % str(tPos), repr(data)
		raise


def AnlysColKey(sKey):  # 分析行头
	tResult = sKey.split("|")
	sColKey = tResult[0]
	if len(tResult) > 1:
		sType = tResult[1]
	else:
		sType = "str"
	return sColKey, sType


def GetExcelData(sXlsFilePath, sSheetName=None, iKeyRow=0, iResultType=RESULT_TYPE_DICT, iKeyCol=0):
	'''
	获取xls数据对象
	:param sXlsFilePath: xls文件路径
	:param sSheetName: Sheet分页名
	:param iKeyRow: 做key的行数
	:param iResultType: 返回值类型
	:param iKeyCol: 做key的列数（字典型才需要）
	:return: xls数据对象（字典或列表）
	'''
	if iResultType == RESULT_TYPE_DICT:
		raise "暂不支持"

	# from xls获取数据
	import pyExcelerator
	dSheetDataList = pyExcelerator.parse_xls(sXlsFilePath, "cp936")
	if sSheetName is not None:
		raise "暂不支持sheet"
	else:
		dSheetData = dSheetDataList[0][1]  # 第一个sheet

	# key-value配对及规整
	dColKey = {}  # iCol: (sKey, sType)
	for iCol in xrange(0, MAX_COL):
		tPos = iKeyRow, iCol
		if tPos in dSheetData:
			data = dSheetData.pop(tPos)  # pop colkey
			sKey = FormatData(tPos, data, "str") # 行头分析
			dColKey[iCol] = AnlysColKey(sKey)
	dRowData = {}  # iRow: {sColKey: data}
	for tPos, data in dSheetData.iteritems():
		iRow, iColKey = tPos
		if iColKey not in dColKey:
			continue
		sColKey, sType = dColKey[iColKey]
		if iRow not in dRowData:
			dRowData[iRow] = {}
		data = FormatData(tPos, data, sType) # 数据获取
		dRowData[iRow][sColKey] = data

	iRowList = dRowData.keys()
	iRowList.sort()
	dDataList = []
	for iRow in iRowList:
		dData = dRowData[iRow]
		for sColKey, sType in dColKey.itervalues():
			if sColKey not in dData:
				data = FormatData(None, None, sType) # 缺省填充
				dData[sColKey] = data
		dDataList.append(dData)
	return dDataList
