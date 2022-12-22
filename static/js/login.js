$(document).ready(function () {

    $('form').on('submit',function(event) {
        $.ajax({
            url: "/",
            type: 'POST',
            data: {
                username: $("#username").val(),
                password: $("#password").val()
            },

        }).done(function(data){
            if (data.success){window.location.href="/dashboard"}
            if (data.error == '1') {
                $('#error-user').show(); 
                $('#error-passw').hide();          
            }
            if (data.error == '2') {
                $('#error-passw').show();
                $('#error-user').hide();
            }
        });
        
        event.preventDefault()


    });

});