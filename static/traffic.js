function assert(cond, message){
    if (!cond) throw new Error(message);
}

$(document).ready(function(){
    $("img").click(function(){
        var loc = $(this).css("background-position");
        var x_loc = loc.split(" ")[0];
        assert(x_loc, "x position of background not properly parsed");
        if (x_loc == "0px") x_loc= "-17px";
        else if (x_loc == "-17px") x_loc = "-34px";
        else if (x_loc == "-34px") x_loc ="0px";
        else assert(false, "Problem with x_loc =" + x_loc);
        $(this).css("background-position",x_loc + " 0px");
    });
});