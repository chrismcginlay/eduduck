var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
    $("input#search").click(function(event){
//        event.preventDefault();
//        search_overlay();
    });

    $( "input#id_q" ).click(function(){
        if($( this ).val() == "Search with Elasticsearch")
            $( this ).val("");
    });
});

function search_overlay() {
    //This rude beginnings of a jQuery overlay intended for search.
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
        height:'50%',
        width:'50%',
    });
    return
}
