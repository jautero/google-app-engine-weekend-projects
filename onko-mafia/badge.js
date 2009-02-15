// Javascript for onko-mafia badge
//
// Copyright 2009 Juha Autero <jautero@iki.fi>
//

// We load jquery from Google
google.load("jquery", "1.3.1");

// on page load complete, modify elements with id mafiaweek or mafiaday 

google.setOnLoadCallback(function() {
	var weekElement =$("#mafiaweek");
	var dayElement = $("#mafiaday");
	weekElement.css("color", "{{weekcolor}}");
	weekElement.html("{{weekword}}");

	dayElement.css("color","{{daycolor}}");
	dayElement.html("{{dayword}}");
});