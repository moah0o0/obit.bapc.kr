
INPUT_FORMAT = """DB.LOAD_BUGO(TARGET_YEAR="2025")"""

RETURN_VALUE = """  []list 형태로 반환되며,
					- 각 값은 str(문자열) 형태로 구성되어 있음

					0:고인명
					1:생년월일
					2:주소
					3:사망일시
					4:사망장소
					5:장례일시
					6:장례장소
					7:발인일시
					8:화장일시
					9:기타사항
					10:key값(지자체명)
					11:key값(표출순서 기준값: 장례일시(없으면 발인일시-화장일시-사망일시 순으로 대체 적용))
					12:key값(장례연도)
					13:key값(장례월)
					14:key값(연령대)
					15:key값(식별값)"""

import gspread
import uuid
import os

def LOAD_BUGO(TARGET_YEAR):

	RESULT = []
	

	# 1. KEY값 구하는 함수 : get_key_datas(부고데이터)

	def get_key_datas(bugo): 
		
		# 1) KEY값 중 표출순서 기준값으로 삼을 값을 불러오기
		
		display_key_options = [bugo[5], bugo[7], bugo[8], bugo[3]]  # 우선순위순으로 가져오기(장례일시-발인일시-화장일시-사망일시)
		display_key = "null"

		for opt in display_key_options:
			if opt != "null":
				display_key = opt.split("~")[0]
				break

		# 2) KEY값 중 장례연도 불러오기
		year_key = display_key.split("-")[0]
		
		# 3) KEY값 중 장례월 불러오기
		month_key = display_key.split("-")[1]
		month_key = int(month_key)
		month_key = str(month_key)

		# 4) KEY값 중 연령대 불러오기

		if bugo[1] == "null":
			age_key = "null"
		else:
			birth_year = bugo[1].split("-")[0]
			age_key = int(year_key) - int(birth_year)
		
			if age_key < 10:
				age_key = 0
			elif age_key >= 10 and age_key < 20:
				age_key = 10
			elif age_key >= 20 and age_key < 30:
				age_key = 20
			elif age_key >= 30 and age_key < 40:
				age_key = 30
			elif age_key >= 40 and age_key < 50:
				age_key = 40
			elif age_key >= 50 and age_key < 60:
				age_key = 50
			elif age_key >= 60 and age_key < 70:
				age_key = 60
			elif age_key >= 70 and age_key < 80:
				age_key = 70
			elif age_key >= 80 and age_key < 90:
				age_key = 80
			elif age_key >= 90:
				age_key = 90
			age_key = str(age_key)

		# 5) 식별코드 UUID값 넣기
		id_key = str(uuid.uuid1())

		# 6) KEY값 반환하기(표출순서 기준값, 장례연도, 장례월, 연령대, 식별값)
		return [display_key, year_key, month_key, age_key, id_key]

	# 2. 구글 스프레드시트에서 데이터를 가져와 KEY값까지 입히기

	print(os.environ.get('PRIVATE_KEY'))
	print(os.environ.get('PRIVATE_KEY_ID')
	credentials = {
		"type": "service_account",
		"project_id": "bapc-croll",
		"private_key_id": os.environ.get('PRIVATE_KEY_ID'),
		"private_key": os.environ.get('PRIVATE_KEY'),
		"client_email": "databaseaccesor@bapc-croll.iam.gserviceaccount.com",
		"client_id": "110468661734487274979",
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://oauth2.googleapis.com/token",
		"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
		"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/databaseaccesor%40bapc-croll.iam.gserviceaccount.com",
		"universe_domain": "googleapis.com"
	}

	gspread_account = gspread.service_account_from_dict(credentials)
	db_document = gspread_account.open_by_url("https://docs.google.com/spreadsheets/d/1kseND7MHBpoOhr6xm5svHvjDMZxCRGKsa7Lc-bNxSLo/edit?usp=sharing")
	db_worksheet = db_document.worksheet("now")

	counts = 0
	
	for row in db_worksheet.get_all_values():		
		counts += 1
		if counts < 6: # 6행부터 수집하도록 한다.
			continue
		add_bugo = row[6:16] + [row[1]] 
		add_bugo = add_bugo + get_key_datas(add_bugo)
		RESULT.append(add_bugo)

	# 3. TARGET_YEAR(대상연도)에 해당하는 값만 필터링

	RESULT = [res for res in RESULT if res[12] == TARGET_YEAR]

	# 4. KEY값 중 표출순서의 기준값에 따라 오름차순으로 정렬

	RESULT.sort(key=lambda x:x[11])

	return RESULT

if __name__ == "__main__":
	for i in LOAD_BUGO(TARGET_YEAR="2025"):
		print(i[10:16])
