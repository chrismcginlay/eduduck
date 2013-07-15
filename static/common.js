$(document).ready(function(){    
    $( '<span class="shade" title="Show/Hide">&uarr;</span>' ).insertBefore( ".abstract" );
    $( '<span class="shade" title="Show/Hide">&uarr;</span>' ).insertBefore( ".FYI" );

    $( ".shade" ).click(function(){
        $( this ).next().slideToggle( "slow" );
        //http://www.unicode.org/charts/PDF/U2190.pdf  \u2193 == &darr;
        //Toggle from down arrow to up arrow etc.
        if ($( this ).html()=='\u2193'){
            $( this ).html('&uarr;');
        } else {
            $( this ).html('&darr;');
        }
    });
});

