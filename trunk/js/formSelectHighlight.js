function formSelectHighlight() {
	if(!document.getElementsByTagName) return;

	var inputs = document.getElementsByTagName('select');
	for(var lcv = 0; lcv < inputs.length; ++lcv) {
		var input = inputs[lcv];
		setHighlight(input);
	}
}

load(formSelectHighlight);

