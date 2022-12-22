$(document).ready(function () {
    $('button').click(function () {
        pasto = $(this).attr('value');
        giorno= $("#date").val();
        $.ajax({
            url: "/liste",
            type: 'POST',
            data: {
                pasto: pasto,
                giorno: giorno,
            }
        }).done(function (data) {
            if (data.success) {
               window.location.href="/lista";
            }        
        });
        event.preventDefault()


    });

});