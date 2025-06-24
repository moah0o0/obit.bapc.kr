from jinja2 import Template
import DB
import os

_PATH = """
	
	index.html : 메인 연도 페이지(2025년)	
	index_0000.html : 각 연도별 페이지(메인 연도 페이지도 포함됨)
	comments.html : 댓글 페이지(disqus 기반)
	
"""

class SETTING:

	# 페이지를 생성할 연도 목록
	BUGO_AVAILABLE_YEARS = ["2023", "2024", "2025"]

	# 메인 연도 페이지
	BUGO_MAIN_YEAR = "2025"

class INDEX_PAGES:
	 
	def __init__(self):
		self.AVAILABLE_YEARS = SETTING.BUGO_AVAILABLE_YEARS
		self.TEMPLATE = self.GET_TEMPLATE()
		
		for file in os.listdir("./export"):
			if file.startswith("index"):
				os.remove("./export/" + file)

		for available in self.AVAILABLE_YEARS:
			html = self.EXPORT_RENDER(TARGET_YEAR=available)
			if available == SETTING.BUGO_MAIN_YEAR:
				self.SAVE_HTML("./export/index.html", html)
				self.SAVE_HTML("./export/index_2025.html", html)	
			else:
				self.SAVE_HTML("./export/index_{}.html".format(available), html)

	def GET_TEMPLATE(self):
		file = open("./templates/index.html", "r", encoding='utf-8')
		template_html = file.read()
		file.close()
		return Template(template_html)


	def EXPORT_RENDER(self, TARGET_YEAR):	
		TEMPLATE = self.TEMPLATE
		DATA = {
			"VAR_BUGO_DATA":DB.LOAD_BUGO(TARGET_YEAR=TARGET_YEAR),
			"VAR_TARGET_YEAR":TARGET_YEAR,
			"VAR_AVAILABLE_YEARS":self.AVAILABLE_YEARS,
		}

		render_html = TEMPLATE.render(DATA)
		return render_html

	def SAVE_HTML(self, EXPORT_DIRECTORY, HTML):
		file = open(EXPORT_DIRECTORY, 'w', encoding="utf-8")
		file.write(HTML)
		file.close()
		return True



INDEX_PAGES()
