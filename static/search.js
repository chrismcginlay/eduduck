$(document).ready(function(){
    $("input#search").click(function(event){
        event.preventDefault();
        var div_adv = "<div id='adv_search'>";
        div_adv += "<h2>Advanced Search</h2>";
        div_adv += "<a href='http://www.elasticsearch.org'>ElasticSearch</a>";
        div_adv += "</div>";
        $("div#content").prepend(div_adv);
        $("div#adv_search").css({
            "position":"absolute",
            "background-color":"red"
        }).animate({
            left:'12%',
            opacity:'0.7',
            height:'75%',
            width:'75%',
        });
    });
});