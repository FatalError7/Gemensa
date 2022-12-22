$(document).ready(function () {

    $('form').on('submit', function (event) {
        $.ajax({
            url: "/profilo",
            type: 'POST',
            data: {
                username: $("#username").val(),
                cognome: $("#cognome").val(),
                nome: $("#nome").val(),
                cf: $("#cf").val(),
                password: $("#password").val(),
                passwordc: $("#passwordc").val(),
            },

        }).done(function (data) {
            if (data.success) { window.location.href = "/dashboard" }
            if (data.error == '1') {
                $('#error-passw').show();                
            }
            
        });

        event.preventDefault()


    });
});