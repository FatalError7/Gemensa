$(document).ready(function () {
$('form').on('submit', function (event) {

    if ($("#colazione").is(":checked")) {colazione='true'}else{colazione='false'};
    if ($("#pranzo").is(":checked")) { pranzo = 'true' } else { pranzo = 'false' };
    if ($("#cena").is(":checked")) { cena = 'true' } else { cena = 'false' };
    if (colazione == 'false' & pranzo == 'false' & cena == 'false'){
        $('#error-pasti').show();
    }else{

    mod= $("#modalita").val();
    
    
    $.ajax({
        url: "/modifica",
        type: 'POST',
        data: {   
            id : (sessionStorage.getItem('id_prenotazione')),      
            colazione: colazione,
            pranzo: pranzo,
            cena: cena,
            modalita: mod,            
        }
    }).done(function (data) {
        if (data.success) { pop_session() }
        /* if (data.error == '1') {
            $('#error-pasti').show();
        } */

    });
    };
    
    event.preventDefault()

    
});

});


function pop_session() {
    sessionStorage.removeItem('id_prenotazione');
    window.location.href = ("/dashboard");
}