$(document).ready(function () {    
    $.ajax({
        url: "/statistiche",
        type: 'POST',
        data: {
        }
    }).done(function (data) {
        if (data) {
            var cont_col1 = document.createTextNode(data.usufruiti_colazione + '/' + data.prenotati_colazione);
            var cont_col_perc = document.createTextNode(data.perc_col + '%');
            var cont_pre_col = document.createTextNode(data.prenotati_colazione);
            var cont_usu_col = document.createTextNode(data.usufruiti_colazione);
            var cont_man_col = document.createTextNode(data.mancanti_colazione);
            document.getElementById('Colazione').appendChild(cont_col1);
            $('#perc-colazione').attr('style', 'width: ' + (data.perc_col) + '%');
            document.getElementById('perc-colazione').appendChild(cont_col_perc);
            document.getElementById('prenotati_colazione').appendChild(cont_pre_col);
            document.getElementById('usufruiti_colazione').appendChild(cont_usu_col);
            document.getElementById('mancanti_colazione').appendChild(cont_man_col);

            var cont_pra1 = document.createTextNode(data.usufruiti_pranzo + '/' + data.prenotati_pranzo);
            var cont_pra_perc = document.createTextNode(data.perc_pra + '%');
            var cont_pre_pra = document.createTextNode(data.prenotati_pranzo);
            var cont_usu_pra = document.createTextNode(data.usufruiti_pranzo);
            var cont_man_pra = document.createTextNode(data.mancanti_pranzo);
            document.getElementById('Pranzo').appendChild(cont_pra1);
            $('#perc-pra').attr('style', 'width: ' + (data.perc_pra) + '%');
            document.getElementById('perc-pra').appendChild(cont_pra_perc);
            document.getElementById('prenotati_pranzo').appendChild(cont_pre_pra);
            document.getElementById('usufruiti_pranzo').appendChild(cont_usu_pra);
            document.getElementById('mancanti_pranzo').appendChild(cont_man_pra);

            var cont_ce1 = document.createTextNode(data.usufruiti_cena + '/' + data.prenotati_cena);
            var cont_ce_perc = document.createTextNode(data.perc_ce + '%');
            var cont_pre_ce = document.createTextNode(data.prenotati_cena);
            var cont_usu_ce = document.createTextNode(data.usufruiti_cena);
            var cont_man_ce = document.createTextNode(data.mancanti_cena);
            document.getElementById('Cena').appendChild(cont_ce1);
            $('#perc-ce').attr('style', 'width: ' + (data.perc_ce) + '%');
            document.getElementById('perc-ce').appendChild(cont_ce_perc);
            document.getElementById('prenotati_cena').appendChild(cont_pre_ce);
            document.getElementById('usufruiti_cena').appendChild(cont_usu_ce);
            document.getElementById('mancanti_cena').appendChild(cont_man_ce);



            $('#perc-pranzo').attr('style','width: ' + (data.perc_pra) + '%');
        }
    });
    
});