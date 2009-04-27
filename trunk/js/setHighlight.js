function setHighlight(field) {
	field.onfocus = function() {
		this.className = 'onFocus';
		this.parentNode.getElementsByTagName('span')[0].className = '';
		this.parentNode.getElementsByTagName('span')[0].style.display = 'inline';
	}

	field.onblur = function() {
		var xmlHttp;
		try {
			// Firefox, Opera 8.0+, Safari
			xmlHttp = new XMLHttpRequest();
		}
		catch(e) {
			// Internet Explorer
			try {
				xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
			}
			catch(e) {
				try {
					xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
				}
				catch(e) {
					alert("Your browser does not support AJAX!");
					return false;
				}
			}
		}
		xmlHttp.onreadystatechange = function() {
			if(xmlHttp.readyState == 4) {
				var result = xmlHttp.responseXML.getElementsByTagName('field')[0].getAttribute('valid');
				if(result == 'True')
					field.className = 'valid';
				else if(result == 'False')
					field.className = 'invalid';
			}
		}
		this.className = 'onBlur';
		xmlHttp.open('GET','isValid?key=' + this.getAttribute('name') + '&value=' + this.value, true);
		xmlHttp.send(null);
		this.parentNode.getElementsByTagName('span')[0].style.display = 'none';
	}

	field.className = 'onBlur';
}

