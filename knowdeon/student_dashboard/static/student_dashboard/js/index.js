
$(document).ready(function(){
    $('#show_hide').on('click', function(){
        var passwordFeild = $('#id_password');
        var passwordFieldType = passwordFeild.attr('type');
        if(passwordFieldType == 'password')
        {
            passwordFeild.attr('type', 'text');
            $(this).text('Hide');
        }
        else
        {
            passwordFeild.attr('type', 'password');
            $(this).text('Show');
        }
    })
})

// ajaxSetup to set CSRF token header
$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
});

$(document).ready(function(){
    $('#next-section').on('click',function(){

        var currentSection = $('#next-section').data('current_section');
        var currentChapter = $('#next-section').data('current_chapter');
        $.ajax({
            type        : 'POST',
            url         : '/student_dashboard/next-section/', // the url where we want to POST
            data        :  { 'current_section' :currentSection,
                            'current_chapter' : current_chapter,
            }, // our data object
            dataType    : 'html', // what type of data do we expect back from the server
            encode      : true,
            success     : function(result){
                console.log('result.status')
            },
            error       : function(error){
                console.log("error "+ error)
            },

        })
    })
})