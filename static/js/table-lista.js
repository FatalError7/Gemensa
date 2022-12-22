
$(document).ready(function () {

    loadtable();

}
);



function loadtable() {
    $.ajax({
        url: "/lista",
        type: 'POST',
        data: {
        },

    }).done(function (data) {
        if (data.error == 'true') {
            var tr0 = document.createElement("tr");
            var par0 = document.createElement("p");
            $(par0).addClass('text-muted mb-0');
            var cont0 = document.createTextNode('Nessuna prenotazione');
            tr0.appendChild(par0);
            par0.appendChild(cont0);
            document.getElementById('table').appendChild(tr0);

        }
        else {
            prenotati=0;
            affluiti=0;
            for (x in data) {
                
                /* Creazione variabile usufruito*/
                // if (data[x]['usufruito_'] == 'true') { pasto = 'Colazione ' };
                /* Creazione Table */
                var tr = document.createElement("tr");
                var td = document.createElement("td");
                var td2 = document.createElement("td");
                var td3 = document.createElement("td");
                var td4 = document.createElement("td");
                var par = document.createElement("p");
                $(par).addClass('text-muted mb-0');
                var par2 = document.createElement("p");
                $(par2).addClass('text-muted mb-0')
                var par3 = document.createElement("p");
                $(par3).addClass('text-muted mb-0')
                var par4 = document.createElement("p");
                $(par4).addClass('text-muted mb-0')
                var cont_cognome = document.createTextNode(data[x]['cognome']);
                var cont_nome = document.createTextNode(data[x]['nome']);
                var cont_usufruito = document.createTextNode(data[x]['affluito']);
                var cont_modalita = document.createTextNode(data[x]['modalita']);


                par.appendChild(cont_cognome);
                par2.appendChild(cont_nome);
                par3.appendChild(cont_usufruito);
                par4.appendChild(cont_modalita);
                td.appendChild(par);
                td2.appendChild(par2);
                td3.appendChild(par3);
                td4.appendChild(par4)
                tr.appendChild(td)
                tr.appendChild(td2)
                tr.appendChild(td3)
                tr.appendChild(td4)

                document.getElementById('table').appendChild(tr);

                var prenotati = prenotati+1
                if (data[x]['affluito']=='Si'){
                    affluiti=affluiti+1;
                }


            }
            var tr = document.createElement("tr");
            var td = document.createElement("td");
            var par = document.createElement("p");            
            $(par).addClass('text-muted mb-0');
            var cont_prenotati = document.createTextNode('Prenotati: '+ prenotati+' Affluiti: '+ affluiti);
            par.appendChild(cont_prenotati);
            td.appendChild(par);
            tr.appendChild(td)
            document.getElementById('table').appendChild(tr);

        }

    });


}