// Shadable class. To use specify 'shadable' class on an element.
// The next sibling element will shade or toggle.
$(document).ready(function(){    
    $( ".shadable" ).prepend('<span class="shade" title="Show/Hide">&darr;</span>');
    $( ".shade" ).click(function(){
        // bbs variable is border-bottom-style
        bbs = $( this ).parent().css('border-bottom-style');
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

