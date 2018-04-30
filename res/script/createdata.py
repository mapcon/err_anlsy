# coding:utf8
"""
xls导表逻辑
  xls -> data.py
"""

OUT_TEMPLATE = """# coding:utf8
def GetData():
    return DATA
DATA = %s\n"""
RE_XLSMATCH = "^[_0-9]+.xls$"


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
	oPatt = re.compile(RE_XLSMATCH)  # 匹配xls的模式
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
	import xlsparse
	data = xlsparse.GetExcelData(sXlsFilePath, iResultType=xlsparse.RESULT_TYPE_LIST)
	WriteData(data, sDataPyFilePath)


def DoTrans():
	# 获取任务队列
	dTaskList = GetTransTaskList()

	# 生成py
	for dTask in dTaskList:
		sXlsFilePath = dTask["sXlsFilePath"]
		sDataPyFilePath = dTask["sDataPyFilePath"]
		CreateData(sXlsFilePath, sDataPyFilePath)
	print "Trans Done!"


if __name__ == "__main__":
	DoTrans()
