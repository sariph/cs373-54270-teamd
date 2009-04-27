function load(func) {
	var old = window.onload;
	if(typeof window.onload != 'function')
		window.onload = func;
	else
		window.onload = function() {
			if(old)
				old();
			func();
		}
}

