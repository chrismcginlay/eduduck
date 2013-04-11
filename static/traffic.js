function assert(cond, message){
    if (!cond) throw new Error(message);
}

$(document).ready(function(){
    $("input").remove();
    $("img").click(function(){
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

	//Now update the progress bar, looking up parent LI via ULID
	var bar_id = "prog" + ($(this).attr('id')).slice(0,2);	//SC or LO?
	path = "/interaction/learningintentiondetail/"+lid_pk+"/progress/";
	updates = $.getJSON(path, bar_id, function(data){
		//return [data.progress.SC[0], data.progress.SC[1]];
		//});
		var pbar = document.getElementById(bar_id);
		completedSC = data.progress.SC[0];
		maxtodoSC = data.progress.SC[1];
		pbar.value = completedSC;
		pbar.max = maxtodoSC;
		var fallback = document.getElementById(bar_id+"_fb");
		var status = document.getElementById(bar_id + "_status");

		//Fallback if no <progress> support
		$(fallback).empty().append("Browser lacks support for progress bar");
		$(status).empty().append(completedSC + "/" + maxtodoSC + " completed. ");

		if (completedSC == maxtodoSC) {
			$(status).append("Well done!");
		}
	});
    });
});
