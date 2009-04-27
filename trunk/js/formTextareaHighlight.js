function formTextareaHighlight() {
	if(!document.getElementsByTagName) return;

	var textareas = document.getElementsByTagName("textarea");
	for(var lcv = 0; lcv < textareas.length; ++lcv)
		setHighlight(textareas[lcv]);
}

load(formTextareaHighlight);

