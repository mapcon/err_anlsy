# coding:utf8
"""
清理文件夹内容，包括：
  res/*.xls
  res/*.html
  script/data/_*.py
  script/data/_*.pyc
"""

def DoClear():
	import os
	sRoot = os.getcwd()

	# 清理xls&html
	sResPath = os.path.join(sRoot, "res")
	for sFile in os.listdir(sResPath):
		if os.path.splitext(sFile)[1] in (".xls", ".html"):
			os.remove(os.path.join(sResPath, sFile))

	# 清理datapy
	sDataPath = os.path.join(sRoot, "script/data")
	for sFile in os.listdir(sDataPath):
		sFileName, sExt = os.path.splitext(sFile)
		if sFileName.startswith("_1") and sExt in (".py", ".pyc"):
			os.remove(os.path.join(sDataPath, sFile))

if __name__ == "__main__":
	DoClear()
