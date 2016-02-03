// Shadable class. To use specify 'shadable' class on an element.
// The next sibling element will shade or toggle.

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

function shadeAllUp() {
    // slide up all shadeable elements
    $( ".shade" ).each( function( idx, element ) {
        $( this ).parent().next().slideUp( 1 );
        $( this ).html( '&darr;');
    });
    return true;
}

$(document).ready(function(){    
    $( ".shadable" ).prepend('<span class="shade" title="Show/Hide">&darr;</span>');

    // slide up all shadeable elements
    shadeAllUp();

    $( ".shade" ).click(function(){
        // bbs variable is border-bottom-style
        var bbs = $( this ).parent().css('border-bottom-style');
        if (bbs=='solid') {
            $( this ).parent().css('border-bottom-style', 'None');
        } else {
            $( this) .parent().css('border-bottom-style', 'solid');
        }
        $( this ).parent().next().slideToggle( "slow" );
        //http://www.unicode.org/charts/PDF/U2190.pdf
        //  \u2193 == &darr; \u2191 == &uarr; \u2192 == &rarr;
        //  \u23ec == &#9196; \23e9 == &#9193; 
        
        //Toggle from down arrow to right arrow etc.
        if ($( this ).html()=='\u2192'){
            $( this ).html('&darr;');
        } else {
            $( this ).html('&rarr;');
        }
    });
});

