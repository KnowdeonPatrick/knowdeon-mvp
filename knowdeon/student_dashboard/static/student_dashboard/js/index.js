
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
