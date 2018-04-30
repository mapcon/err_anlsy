# coding:utf8
"""
生成分析报告
"""


def StartAnlys(sTime):
	print u"分析时段", sTime


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
