# coding:utf8
'''
ECharts管理器
用法：
import drawcharts
drawcharts.Draw(xxxxxxdata.GetData())
'''
from pyecharts import Line
from pyecharts import Pie

class EChartsManager(object):
	def __init__(self, data):
		self.InitData(data)
		self.DrawTimeLine()
		self.DrawServerPie()

	def InitData(self, data): # 初始化导表数据
		# 导表数据
		self.m_Data = data

		# 时间数据
		self.m_TimeDict = {}

		# 服务器数据
		self.m_ServerDict = {}

		for info in data:
			self.HandleTimeInfo(info)
			self.HandleServerInfo(info)

	def HandleTimeInfo(self, info):  # 处理时间信息
		import time
		timeStruct = time.localtime(info["iTime"])
		iHour = timeStruct.tm_hour
		if iHour not in self.m_TimeDict:
			self.m_TimeDict[iHour] = 0
		self.m_TimeDict[iHour] += 1

	def HandleServerInfo(self, info):  # 处理服务器消息
		iServer = info["iServer"]
		sServer = info["sServer"]
		if iServer == 0 and (sServer in ("未知服务器", "")):
			sKey = "未知服务器"
		else:
			sKey = sServer
		if sKey not in self.m_ServerDict:
			self.m_ServerDict[sKey] = 0
		self.m_ServerDict[sKey] += 1

	def DrawTimeLine(self):  # 绘制时间折线图
		kList = self.m_TimeDict.keys()
		kList.sort()
		vList = [self.m_TimeDict[iTime] for iTime in kList]
		line = Line("时间-报错数量折线")
		line.add("报错", kList, vList, mark_point=["average", "max", "min"])
		# line.add("平滑线测试", lineAttr, timeList, is_smooth=True, mark_point=["average", "max", "min"])
		line.render(path="line.html")

	def DrawServerPie(self):  # 绘制服务器饼图
		klist = self.m_ServerDict.keys()
		vList = [self.m_ServerDict[sServer] for sServer in klist]
		pie = Pie("服务器报错汇总", title_pos='center', title_top=230, width=900, height=700)
		pie.add("服务器报错饼图", klist, vList, center=[25, 70], is_random=True, radius=[30, 50])
		pie.add("服务器报错玫瑰图", klist, vList, center=[75, 70], is_random=True, radius=[30, 50], rosetype="area")
		pie.render(path="pie.html")

def Draw(dataList):
	oMgr = EChartsManager(dataList)

def Test():
	import testdata # 将导表文件拷贝到同一个目录下
	errorList = testdata.GetData()
	Draw(errorList)

Test()
