from jinja2 import Template
import DB
import os

_PATH = """
	
	index.html : 메인 연도 페이지(2025년)	
	index_0000.html : 각 연도별 페이지(메인 연도 페이지도 포함됨)
	comments.html : 댓글+통계 페이지(disqus 기반)
	
"""

import feedparser
from html import unescape
from bs4 import BeautifulSoup

def get_disqus_comments():
    rss_url = "https://obit-bapc-kr.disqus.com/comments.rss"
    feed = feedparser.parse(rss_url)

    results = []

    for entry in feed.entries:
        author = entry.get("author", "알 수 없음")
        
        # description은 HTML이므로, 텍스트로 변환
        raw_html = entry.get("description", "")
        soup = BeautifulSoup(unescape(raw_html), "html.parser")
        comment = soup.get_text().strip()

        results.append((author, comment))

    return results


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
			"VAR_COMMENTS":get_disqus_comments()
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
			if file.startswith("comment"):
				os.remove("./export/" + file)

		html = self.EXPORT_RENDER()
		self.SAVE_HTML("./export/comment.html", html)

	def GET_TEMPLATE(self):
		file = open("./templates/comment.html", "r", encoding='utf-8')
		template_html = file.read()
		file.close()
		return Template(template_html)

	def EXPORT_RENDER(self):	
		TEMPLATE = self.TEMPLATE
		render_html = TEMPLATE.render()
		return render_html

	def SAVE_HTML(self, EXPORT_DIRECTORY, HTML):
		file = open(EXPORT_DIRECTORY, 'w', encoding="utf-8")
		file.write(HTML)
		file.close()
		return True

INDEX_PAGES()
COMMENT_PAGE()