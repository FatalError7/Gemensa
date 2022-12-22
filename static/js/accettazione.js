$(document).ready(function () {
    $('form').on('submit', function (event) {
            $.ajax({
                url: "/accettazione",
                type: 'POST',
                data: {
                    username: $("#username").val(),
                }
            }).done(function (data) {
                if (data.success) { 
                    $("#success").empty();
                    var text1 = document.createTextNode("Buon Appetito");
                    var br = document.createElement("br");
                    var text2 = document.createTextNode(data.success);

                    document.getElementById('success').appendChild(text1);
                    document.getElementById('success').appendChild(br);
                    document.getElementById('success').appendChild(text2);
                    $('#success').show();
                    $('#error').hide();


                 }
                if (data.error) {    
                    $("#error").empty();               
                    var text= document.createTextNode(data.error);
                    document.getElementById('error').appendChild(text);                    
                    $('#error').show();
                    $('#success').hide();
                }

            });
        

        event.preventDefault()


    });

});