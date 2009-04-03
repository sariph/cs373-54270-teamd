function formInputHighlight() {
	if(!document.getElementsByTagName) return;

	var inputs = document.getElementsByTagName('input');
	for(var lcv = 0; lcv < inputs.length; ++lcv) {
		var input = inputs[lcv];
		var inputType = input.getAttribute('type');
		if(inputType == 'text' || inputType == 'password' || inputType == 'radio')
			setHighlight(input);
	}
}

load(formInputHighlight);

