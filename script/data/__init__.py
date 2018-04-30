# coding:utf8
"""
数据导出包
"""


def GetDayData(sDay):  # YYMMDD
	try:
		oDataModule = __import__("data._%s" % sDay)
		oModule = getattr(oDataModule, "_%s" % sDay)
		return oModule.GetData()
	except:
		return None
