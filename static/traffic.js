//static/traffic.js
//https://docs.djangoproject.com/en/1.6/ref/contrib/csrf/#ajax
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

function assert(cond, message) {
    if (!cond) {
        if (!message) message = "no message defined";
        message = "Assert Failed: " + message
        console.log(message);
        throw new Error(message);
    }
}

function get_status(img) {
    assert (img, "no image supplied from DOM");
    var status = (img.attr('class')).slice(3);
    return status; 
}

function cycle_status_indb(lid_id) {
    assert(lid_id, "no lid_id supplied");
    assert(typeof lid_id !== "string", "string argument: expect integer");
    assert(lid_id%1 == 0, "float argument: expect integer");
    var url = '/interaction/learningintentiondetail/'+lid_id+'/cycle/';
    return $.ajax({
        type:'POST',
        url: url, 
        data: {'csrf_token':csrftoken},
        dataType: 'json',
    });
}

function get_lid(img) {
    assert(img, "no image supplied from DOM");
    lid_pk = (img.attr('id')).slice(5);
    assert(lid_pk, "no lid_pk extracted from img");
    return lid_pk;
}

function cycle(img) {
    assert(img, "no image supplied from DOM");
    var lid_pk = get_lid(img);
    var current_status = get_status(img);
    assert(current_status, "no current status obtained");
    var next_status; 
    switch(current_status) {
        case 'red':
            next_status = 'amber';
            img.removeClass('tl-red');
            img.addClass('tl-amber');
            break;
        case 'amber':
            next_status = 'green';
            img.removeClass('tl-amber');
            img.addClass('tl-green');
            break;
        case 'green':
            next_status = 'red';
            img.removeClass('tl-green');
            img.addClass('tl-red');
            break;
    }
    return next_status;
}

function refresh_progress(data) {
    assert(data, "data argument not supplied");
    progressLO_data = data['LO'];
    progressSC_data = data['SC'];
    progressLO_element = $('progress#progLO');
    progressSC_element = $('progress#progSC');
    progressLO_element[0].value = progressLO_data[0];
    progressLO_element[0].max = progressLO_data[1];
    progressSC_element[0].value = progressSC_data[0];
    progressSC_element[0].max = progressSC_data[1];

    var fallback = document.getElementById("progLO_fb");
    var status = document.getElementById("progLO_status");
    $(fallback).append("Browser lacks support for progress bar");
    $(fallback).css("display", "block");
    var LO_prog = progressLO_data[0];
    var LO_max = progressLO_data[1];
    $(status).empty().append(LO_prog + "/" + LO_max + " completed. ");
    if (LO_prog == LO_max) {
        $(status).append("Well done!");
    }
    fallback = document.getElementById("progSC_fb");
    var status = document.getElementById("progSC_status");
    var SC_prog = progressSC_data[0];
    var SC_max = progressSC_data[1];
    $(fallback).append("Browser lacks support for progress bar");
    $(fallback).css("display", "block");
    $(status).empty().append(SC_prog + "/" + SC_max + " completed. ");
    if (SC_prog == SC_max) {
        $(status).append("Well done!");
    }
}

$(document).ready(function() {
    $("input.traffic").remove();
    $("img[id^='id_SC'], img[id^='id_LO']").dblclick(function() {
        //http://stackoverflow.com/questions/14220321/how-to-return-the-response-from-an-asynchronous-call
        var lid_pk = parseInt(get_lid($(this)));
        cycle_status_indb(lid_pk).done(function(json) {
            if (json.authenticated==false) {
                alert('You are not logged in');
                return false;
            }
            if (json.enrolled==false) {
                alert('You are not enrolled');
                return false;
            }
            cycle($(this));
            refresh_progress(json.progress);
            return true;
        }).fail(function() {
            alert('Something went wrong whilst trying to update this traffic light');
            return false;
        });
    });
}); //ready
