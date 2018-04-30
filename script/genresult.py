# coding:utf8
"""
生成统计报告
"""

HTML_TAIL = "</html>"

def Gen(sResultFilePath, sErrMD, sGraphMD):
	iFind = sGraphMD.find(HTML_TAIL)
	if iFind:
		sHtml = ""
		print u"生成报告！", sResultFilePath
		sHtml = "%s\n%s\n%s</html>" % (sGraphMD[:iFind], sErrMD, HTML_TAIL)
		f = open(sResultFilePath, "w+")
		f.write(sHtml)
		f.close()
