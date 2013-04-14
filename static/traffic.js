function assert(cond, message){
    if (!cond) throw new Error(message);
}

$(document).ready(function(){
    $("input").remove();
    $("img").click(function(){

/*
array.slice(start, end)
Parameter Values
Parameter	Description
start	Required. An integer that specifies where to start the selection (The first element has an index of 0). Use negative numbers to select from the end of an array
end	Optional. An integer that specifies where to end the selection. If omitted, all elements from the start position and to the end of the array will be selected. Use negative numbers to select from the end of an array
*/

        lid_pk = ($(this).attr('id')).slice(2);
        path = "/interaction/learningintentiondetail/"+lid_pk+"/cycle/";
        $.getJSON(path);
        var loc = $(this).css("background-position");
        var x_loc = loc.split(" ")[0];
        assert(x_loc, "x position of background not properly parsed");
        if (x_loc == "0px") x_loc= "-17px";
        else if (x_loc == "-17px") x_loc = "-34px";
        else if (x_loc == "-34px") x_loc ="0px";
        else assert(false, "Problem with x_loc =" + x_loc);
        $(this).css("background-position",x_loc + " 0px");

	//Now update the progress bars, looking up parent LI via ULID
	var bar_type = $(this).attr('id').slice(0,2);
	var bar_id = "prog" + bar_type;	//SC or LO?
	path = "/interaction/learningintentiondetail/"+lid_pk+"/progress/";
	$.getJSON(path, bar_id, function(data){
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
		$(fallback).empty().append("Browser lacks support for progress bar");
		$(status).empty().append(completed + "/" + maxtodo + " completed. ");

		if (completed == maxtodo) {
			$(status).append("Well done!");
		}
	});
    });
});
