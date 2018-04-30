# coding:utf8
"""
todo
"""

OUT_TEMPLATE = """# coding:utf8
def GetData():
    return DATA
DATA = %s\n"""

TIMEFORMAT = "(%f-19-70*365)*86400-8*3600"

def GetTransTaskList():
	'''
	获取getcwd目录下的数据xls，安排导表任务
	:return: dTaskList: [
		{
			sXlsFilePath,
			sDataPyFilePath,
		}
	]
	'''
	import re
	import os
	dTaskList = []
	oPatt = re.compile("^[_0-9]+.xls$") # 匹配xls的模式
	sFileList = os.listdir(os.getcwd())
	for sFile in sFileList:
		if oPatt.match(sFile):
			dTask = {}
			dTask["sXlsFilePath"] = os.path.abspath(sFile)
			sName, _ = os.path.splitext(sFile)
			sPyData = "data/%sdata.py" % sName
			dTask["sDataPyFilePath"] = os.path.abspath(sPyData)
			dTaskList.append(dTask)
	return dTaskList


RESULT_TYPE_DICT = 1
RESULT_TYPE_LIST = 2
MAX_COL = 15 # 超过最大列数的会被忽略。最大行数是取连续非空行最大值

def FormatData(tPos, data, sSpecifiedType=None): # 规整化
	try:
		if sSpecifiedType == "str" or type(data) == unicode:
			if data is None:
				return ""
			return data.encode("utf8")
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
		if sSpecifiedType == "int":
			if data is None:
				return 0
			return int(data)
		return data
	except:
		print "wrong content in %s" % str(tPos)
		raise

def AnlysColKey(sKey): # 分析行头
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
		dSheetData = dSheetDataList[0][1] # 第一个sheet

	# key-value配对及规整
	dColKey = {} # iCol: (sKey, sType)
	for iCol in xrange(0, MAX_COL):
		tPos = iKeyRow, iCol
		if tPos in dSheetData:
			data = dSheetData.pop(tPos) # pop colkey
			sKey = FormatData(tPos, data)
			dColKey[iCol] = AnlysColKey(sKey)
	dRowData = {} # iRow: {sColKey: data}
	for tPos, data in dSheetData.iteritems():
		iRow, iColKey = tPos
		if iColKey not in dColKey:
			continue
		sColKey, sType = dColKey[iColKey]
		if iRow not in dRowData:
			dRowData[iRow] = {}
		data = FormatData(tPos, data, sType)
		dRowData[iRow][sColKey] = data

	iRowList = dRowData.keys()
	iRowList.sort()
	dDataList = []
	for iRow in iRowList:
		dData = dRowData[iRow]
		for sColKey, sType in dColKey.itervalues():
			if sColKey not in dData:
				data = FormatData(None, None, sType)
				dData[sColKey] = data
		dDataList.append(dData)
	return dDataList

def WriteData(data, sDataPyFilePath):
	'''
	将python数据写入data.py
	:param data: Python数据对象 
	:param sDataPyFilePath: 导出py文件绝对路径
	:return: NULL
	'''
	import prettyprint
	sData = prettyprint.pp_str(data)
	f = open(sDataPyFilePath, "w")
	f.write(OUT_TEMPLATE % sData)
	f.close()

def CreateData(sXlsFilePath, sDataPyFilePath):
	'''
	xls数据导表
	:param sXlsFilePath: xls文件绝对路径
	:param sDataPyFilePath: data.py绝对路径
	:return: NULL
	'''
	data = GetExcelData(sXlsFilePath, iResultType=RESULT_TYPE_LIST)
	WriteData(data, sDataPyFilePath)


def DoTrans():
	# 获取任务队列
	dTaskList = GetTransTaskList()

	# 生成py
	for dTask in dTaskList:
		sXlsFilePath = dTask["sXlsFilePath"]
		sDataPyFilePath = dTask["sDataPyFilePath"]
		CreateData(sXlsFilePath, sDataPyFilePath)
		break
	print "Trans Done!"

if __name__ == "__main__":
	DoTrans()
