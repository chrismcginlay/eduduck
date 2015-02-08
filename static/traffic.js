//static/traffic.js
//https://docs.djangoproject.com/en/1.6/ref/contrib/csrf/#ajax
var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function assert(cond, message) {
    if (!cond) throw new Error(message);
}

function cycle_and_progress(img) {
	var lid = img;
	var lid_pk = (lid.attr('id')).slice(2);
	var path = "/interaction/learningintentiondetail/"+lid_pk+"/cycle/";

	$.getJSON(path, lid, function(data) {
		var loc = lid.css("background-position");
		var x_loc = loc.split(" ")[0];
		assert(x_loc, "x position of background not properly parsed");
		if (x_loc == "0px") x_loc= "-17px";
		else if (x_loc == "-17px") x_loc = "-34px";
		else if (x_loc == "-34px") x_loc ="0px";
		else assert(false, "Problem with x_loc =" + x_loc);
		lid.css("background-position",x_loc + " 0px");

		//Update the progress bars, looking up parent LI via ULID
		var bar_type = lid.attr('id').slice(0,2);
		var bar_id = "prog" + bar_type;	//SC or LO?
		path = "/interaction/learningintentiondetail/"+lid_pk+"/progress/";
		$.getJSON(path, bar_id, function(data) {
			var prog_bar = document.getElementById(bar_id);
			if (bar_type == 'SC') {			
				completed = data.progress.SC[0];
				maxtodo = data.progress.SC[1];
			} else if (bar_type == 'LO') {			
				completed = data.progress.LO[0];
				maxtodo = data.progress.LO[1];
			}
			prog_bar.value = completed;
			prog_bar.max = maxtodo;
			var fallback = document.getElementById(bar_id+"_fb");
			var status = document.getElementById(bar_id + "_status");

			//Fallback if no <progress> support
			$(fallback).append("Browser lacks support for progress bar");
			$(fallback).css("display", "block");

			$(status).empty().append(completed + "/" + maxtodo + " completed. ");

			if (completed == maxtodo) {
				$(status).append("Well done!");
			}
		}); //getJSON inner
	}); //getJSON outer	
	return
}


$(document).ready(function() {
    $("input.traffic").remove();
    $("img").dblclick(function() {
	    cycle_and_progress($(this))
    });
}); //ready
