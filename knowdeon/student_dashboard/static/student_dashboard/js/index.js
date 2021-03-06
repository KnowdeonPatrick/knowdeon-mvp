
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

        var submitedCourse = $('#next-section').data('submited_course');
        var next = $('#next-section').data('next');
        // var sections = document.getElementById("sections");
        $.ajax({
            type        : 'POST',
            url         : '/student_dashboard/next-section/', // the url where we want to POST
            data        :  { 'submited_course' : submitedCourse,
                            'next' : next,
                            // 'current_chapter' : current_chapter,
            }, // our data object
            dataType    : 'html', // what type of data do we expect back from the server
            encode      : true,
            success     : function(result){
               
            //    if(result.search('id="next-chapter"') !== -1 || result.search('id="completed_course"') !== -1){
            if(result.search('http://') !== -1 && result.search('/student_dashboard/chapter/') !== -1){
                console.log(result);
                    window.location.href = result;
                    // $('#next-section').remove();
                    // $('#next-buttons').append(result)
               } 
               else if(result.search('http://') !== -1 && result.search('/student_dashboard/course/') !== -1) {
                    window.location.href = result;
                }
               else {
                    $('#next-buttons').remove();
                    $('#sections').append(result)
               }

            },
            error       : function(error){
                console.log("error "+ error)
            },

        })
    })
})