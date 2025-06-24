
var BUGOS_HTML = ""

for (let i = 0; i < db.length; i++) {
    NEW_BUGO = `<div class="flower_icon age`+db[i][14]+` `+db[i][13]+`월  `+db[i][10] +`" onclick="modal_open('d', '`+db[i][15]+`')">
					<p class='ribbon_name'>`+db[i][0]+`</p>
				</div>`
	BUGOS_HTML = BUGOS_HTML + NEW_BUGO

}

document.getElementById("flower_line").innerHTML = BUGOS_HTML