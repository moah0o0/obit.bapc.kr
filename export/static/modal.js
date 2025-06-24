
const modal = document.querySelector('.modal');
	function modal_open(opt, hash) {
	  	function reset(){
			var lists = document.getElementsByClassName("month_logo")
			for(let i = 0; i < lists.length; i++){
				lists[i].style.opacity = '1';	
			}
			var lists = document.getElementsByClassName("goo_logo")
			for(let i = 0; i < lists.length; i++){
				lists[i].style.opacity = '1';	
			}
			var lists = document.getElementsByClassName("flower_icon")
			for(let i = 0; i < lists.length; i++){
				lists[i].style.opacity = '1';	
			}
		}
	    modal.style.display = 'block';
	    if (opt == "a") {
	    	reset()
	    	document.getElementById("modal_a").style.display = 'block'
	    	document.getElementById("modal_b").style.display = 'none'
	    	document.getElementById("modal_c").style.display = 'none'
	    	document.getElementById("modal_d").style.display = 'none'
	    }
	    if (opt == "b"){
	    	reset()
	    	document.getElementById("modal_b").style.display = 'block'
	    	document.getElementById("modal_a").style.display = 'none'
	    	document.getElementById("modal_c").style.display = 'none'
	    	document.getElementById("modal_d").style.display = 'none'
	    }
	    if (opt == "c"){
	    	reset()
	    	document.getElementById("modal_c").style.display = 'block'
	    	document.getElementById("modal_b").style.display = 'none'
	    	document.getElementById("modal_a").style.display = 'none'
	    	document.getElementById("modal_d").style.display = 'none'
	    }
	    if (opt == "d"){
	    	document.getElementById("modal_d").style.display = 'block'
	    	document.getElementById("modal_b").style.display = 'none'
	    	document.getElementById("modal_a").style.display = 'none'
	    	document.getElementById("modal_c").style.display = 'none'
		    for(let i = 0; i < db.length; i++) {
		        if(db[i][15] == hash){
		        	var target = db[i]

		        	for (let i2 = 0; i2 < target.length; i2++){
		        		if(target[i2] == "null"){
		        			target[i2] = "<span style='color:rgba(0, 255, 255, 0.9);'> 지자체의 정보 비공개</span>"
		        		}
		        	}

		    		text = `
		    			<strong>이름</strong>&nbsp;`+target[0]+`<br>
	    				<strong>생년월일</strong>&nbsp;`+target[1]+`<br>
	    				<strong>거주지</strong>&nbsp;`+target[2]+`<br>
	    				<strong>사망일시</strong>&nbsp;`+target[3]+`<br>
	    				<strong>사망장소</strong>&nbsp;`+target[4]+`<br>
	    				<strong>장례일정</strong>&nbsp;`+target[5]+`<br>
	    				<strong>장례장소</strong>&nbsp;`+target[6]+`<br>
	    				<strong>발인일시</strong>&nbsp;`+target[7]+`<br>
	    				<strong>화장일시</strong>&nbsp;`+target[8]+`<br>
	    			`
	    			document.getElementById("modal_d_description").innerHTML = text
	    		}
	    	}
	    }
	}
	function modal_close() {
	    modal.style.display = 'none';
	}
