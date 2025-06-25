from jinja2 import Template
import DB
import os

_PATH = """
	
	index.html : 메인 연도 페이지(2025년)	
	index_0000.html : 각 연도별 페이지(메인 연도 페이지도 포함됨)
	together.html : 댓글 페이지(disqus 기반)
	
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

class COMMENT_PAGE:

	def __init__(self):
		self.TEMPLATE = self.GET_TEMPLATE()
		for file in os.listdir("./export"):
			if file.startswith("together"):
				os.remove("./export/" + file)

		html = self.EXPORT_RENDER()
		self.SAVE_HTML("./export/together.html", html)

	def GET_TEMPLATE(self):
		file = open("./templates/together.html", "r", encoding='utf-8')
		template_html = file.read()
		file.close()
		return Template(template_html)

	def EXPORT_RENDER(self):	
		TEMPLATE = self.TEMPLATE
		DATA = {
			"VAR_ANALYZED_DATA":self.GET_ANALYZE()
		}
		render_html = TEMPLATE.render(DATA)
		return render_html

	def SAVE_HTML(self, EXPORT_DIRECTORY, HTML):
		file = open(EXPORT_DIRECTORY, 'w', encoding="utf-8")
		file.write(HTML)
		file.close()
		return True


	def GET_ANALYZE(self):
		
		all_bugos = []

		for target_year in SETTING.BUGO_AVAILABLE_YEARS:
			all_bugos = all_bugos + DB.LOAD_BUGO(TARGET_YEAR=target_year)


		def age_analyze():
			
			labels = ["10대", "20대", "30대", "40대", "50대", "60대", "70대", "80대"]
			# 10대 이하 및 90대 이상 미포함 / 반영 필요

			values = []

			for label in labels:
				values.append(len([i for i in all_bugos if i[14] == label.replace("대","")]))

			under_teen = len([i for i in all_bugos if i[14] == "0"])
			over_nineteen = len([i for i in all_bugos if i[14] == "90"])
			null_age = len([i for i in all_bugos if i[14] == "null"])

			labels = ["10세 미만"] + labels + ["90세 이상"] + ["미상"]
			values = [under_teen] + values + [over_nineteen] + [null_age]


			return (labels, values)


		def region_analyze():
			
			labels = ["해운대구", "서구", "남구", "북구", "동구", "기장군", "금정구", "중구", "연제구", "사상구", "영도구", "부산진구", "동래구", "사하구", "수영구", "강서구"]
			# 10대 이하 및 90대 이상 미포함 / 반영 필요

			values = []

			for label in labels:
				values.append(len([i for i in all_bugos if i[10] == label]))

			return (labels, values)

		def yearmonth_analyze():

			labels = []
			values = []

			def get_year_month_value(year, month):
				if len(month) == 1:
					month = "0" + month
				return "{}-{}".format(year, month)

			labels = [get_year_month_value(i[12], i[13]) for i in all_bugos]
			labels = set(labels)
			labels = list(labels)
			labels.sort()
			
			for label in labels:
				counts = [i for i in all_bugos if label == get_year_month_value(i[12], i[13])]
				counts = len(counts)
				values.append(counts)

			return (labels, values)



		age_data = age_analyze()
		region_data = region_analyze()
		yearmonth_data = yearmonth_analyze()
		
		RESULT = {
			"연령대":{
				"label":age_data[0],
				"value":age_data[1]
			},
			"지자체":{
				"label":region_data[0],
				"value":region_data[1]
			},
			"연월":{
				"label":yearmonth_data[0],
				"value":yearmonth_data[1]
			},
			"총인원":len(all_bugos)
		}

		return RESULT


INDEX_PAGES()
COMMENT_PAGE()