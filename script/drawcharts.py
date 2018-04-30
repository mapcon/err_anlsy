# coding:utf8
'''
ECharts管理器
'''
from pyecharts import Line
from pyecharts import Pie

LINE_FILE   = "line.html"
PIE_FILE    = "pie.html"
OUTPUT_FILE = "output.html"

FILE_LIST = [
	LINE_FILE,
	PIE_FILE,
]

BODYSTART   = "<body>"
BODYEND     = "</body>\n"
NEWLINE     = "<br>"

class EChartsManager(object):

	def __init__(self, data):
		self.InitData(data)

	def DoDraw(self):
		self.DrawTimeLine()
		self.DrawServerPie()
		return self.GetMergeHtmls()

	def InitData(self, data): # 初始化导表数据
		# 导表数据
		self.m_Data = data

		# 时间数据
		self.m_TimeDict = {}

		# 服务器数据
		self.m_ServerDict = {}

		for sKey in data:
			oneDayData = data[sKey]
			for info in oneDayData:
				self.HandleTimeInfo(info)
				self.HandleServerInfo(info)

	def HandleTimeInfo(self, info):  # 处理时间信息
		import time
		sTime = time.strftime("%Y/%m/%d %H时", time.localtime(info["iTime"]))
		if sTime not in self.m_TimeDict:
			self.m_TimeDict[sTime] = 0
		self.m_TimeDict[sTime] += 1

	def HandleServerInfo(self, info):  # 处理服务器消息
		iServer = info["iServer"]
		sServer = info["sServer"]
		if iServer == 0 or (sServer in ("未知服务器", "")):
			sKey = "未知服务器"
		else:
			sKey = sServer
		if sKey not in self.m_ServerDict:
			self.m_ServerDict[sKey] = 0
		self.m_ServerDict[sKey] += 1

	def DrawTimeLine(self):  # 绘制时间折线图
		kList = self.m_TimeDict.keys()
		kList.sort()
		vList = [self.m_TimeDict[sTime] for sTime in kList]
		line = Line("时间-报错数量折线")
		line.add("报错", kList, vList, is_datazoom_show=True, datazoom_type='both', mark_point=["average", "max", "min"])
		# line.add("平滑线测试", lineAttr, timeList, is_smooth=True, mark_point=["average", "max", "min"])
		line.render(path=LINE_FILE)

	def DrawServerPie(self):  # 绘制服务器饼图
		klist = self.m_ServerDict.keys()
		vList = [self.m_ServerDict[sServer] for sServer in klist]
		pie = Pie("服务器报错汇总", title_pos='center', title_top=160, width=900, height=700)
		pie.add("服务器报错饼图", klist, vList, center=[25, 50], is_random=True, radius=[20, 50])
		pie.add("服务器报错玫瑰图", klist, vList, center=[75, 50], is_random=True, radius=[10, 50], rosetype="area")
		pie.render(path=PIE_FILE)

	def GetMergeHtmls(self): # 合并多张图表
		import os
		headString = ""
		midStringList = []
		tailString = ""
		for filename in FILE_LIST:
			if os.path.exists(filename):
				f = open(filename, "r")
				fileString = f.read()
				f.close()
				headString, bodyString, tailString = self.GetOneHtml(fileString)
				if bodyString:
					midStringList.append(bodyString)
				os.remove(filename)
		sResult = "%s%s" % (headString, NEWLINE)
		for sBody in midStringList:
			sResult += sBody
		sResult += tailString
		# 测试图表合成输出
		# f = open(OUTPUT_FILE, "w+")
		# f.write(sResult)
		# f.close()
		return sResult

	def GetOneHtml(self, sHtml): # 处理单张图表
		iStart = sHtml.find(BODYSTART)
		iEnd = sHtml.find(BODYEND)
		iLen = len(BODYEND)
		headString = sHtml[:iStart]
		bodyString = "\n%s%s%s%s" % (sHtml[iStart:iEnd], BODYEND, NEWLINE, NEWLINE)
		tailString = sHtml[iEnd+iLen:]
		return headString, bodyString, tailString

def Draw(dataDict):
	oMgr = EChartsManager(dataDict)
	return oMgr.DoDraw()

# def Test():
# 	import _180410, _180411, _180412 # 将导表文件拷贝到同一个目录下
# 	errorDict = {
# 		180410: _180410.GetData(),
# 		180411: _180411.GetData(),
# 		180412: _180412.GetData(),
# 	}
# 	Draw(errorDict)
# Test()