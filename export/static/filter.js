var selected = ""

function SET_FILTER(text){	
	var remove_list = ["age0", "age10", "age20", "age30", "age40", "age50", "age60", "age70", "age80", "age90", "북구", "동구", "동래구", "강서구", "금정구", "기장군", "해운대구", "부산진구", "중구", "남구", "사하구", "사상구", "서구", "수영구", "영도구", "연제구", "1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
	
	for(let i = 0; i < remove_list.length; i++){
		var lists = document.getElementsByClassName(remove_list[i])
		for(let i = 0; i < lists.length; i++){
			lists[i].style.opacity = '0.3';	
		}
	}

	if (selected != text){
		var lists = document.getElementsByClassName(text)
		selected = text
		for(let i = 0; i < lists.length; i++){
			lists[i].style.opacity = '1';	
		}
	} else {
		var lists = document.getElementsByClassName(text)
		selected = ""
		for(let i = 0; i < lists.length; i++){
			lists[i].style.opacity = '0.1';	
		}	
	}	

	modal_close()

}