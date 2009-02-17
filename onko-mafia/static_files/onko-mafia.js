// Javascript for onko-mafia
//
// Copyright 2009 Juha Autero <jautero@iki.fi>
//
//
google.load("jquery", "1");

// on page load complete, fire off a jQuery json-p query
// against Google web search
google.setOnLoadCallback(function() {
  $.getJSON("http://localhost:8080/?format=json",

    // on search completion, process the results
    function (data) {
	var weekElement =$("#mafiaweek");
	var dayElement = $("#mafiaday");
	var yescolor="#00ff00";
	var nocolor="#ff0000";
	var yesword="on";
	var noword="ei";
	
	if (data.week) {
		weekElement.css("color",yescolor);
		weekElement.html(yesword);
	} else {
		weekElement.css("color",nocolor);
		weekElement.html(noword);
	}
	if (data.day) {
		dayElement.css("color",yescolor);
		dayElement.html(yesword);
	} else {
		dayElement.css("color",nocolor);
		dayElement.html(noword);
	}
	
    });
  });
