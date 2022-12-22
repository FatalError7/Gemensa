$(document).ready(function () {
    $('#user_form').on('submit', function (event) {
        $.ajax({
            url: "/admin",
            type: 'POST',
            data: {
                username: $("#username").val(),
            }
        }).done(function (data) {
            if (data.success) {
                $("#error").hide();
                $('#find').show();
            }
            if (data.error) {
                $('#error').show();
                
            }

        });


        $('#find_form').on('submit', function (event) {
            $.ajax({
                url: "/update",
                type: 'POST',
                data: {
                    cognome: $("#cognome").val(),
                    nome: $("#nome").val(),
                    cf: $("#cf").val(),
                    password: $("#password").val(),
                },

            }).done(function (data) {
                if (data.success) { 
                    $('#success').show(); }
                 
            });

            event.preventDefault()


        });


        event.preventDefault()


    });

});