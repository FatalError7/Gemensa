
$(document).ready(function () {
   
loadtable();


      
}
);




function loadtable() {
    $.ajax({
        url: "/table",
        type: 'POST',
        data: {
        },

    }).done(function (data) {
        if (data.error == 'true'){
            var tr0 = document.createElement("tr");
            var par0 = document.createElement("p");
            $(par0).addClass('text-muted mb-0');
            var cont0 = document.createTextNode('Nessuna prenotazione');
            tr0.appendChild(par0);
            par0.appendChild(cont0);
            document.getElementById('table').appendChild(tr0);            
            
        }
        else{
        for (x in data) {
            /* Creazione data in Formato D-M-Y */
            var dt = data[x]['data'];
            var dtformat = new Date(dt);
            var y = dtformat.getFullYear();
            var m = dtformat.getMonth();
            m += 1;
            var d = dtformat.getDate();
            var date = d + '-' + m + '-' + y;

            /* Creazione variabile pasto*/
            pasto = '';
            if (data[x]['prenotato_colazione'] == 'true') { pasto = 'Colazione ' };
            if (data[x]['prenotato_pranzo'] == 'true') { pasto = pasto + 'Pranzo ' };
            if (data[x]['prenotato_cena'] == 'true') { pasto = pasto + 'Cena ' };

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
            var cont_date = document.createTextNode(date);
            var cont_pasto = document.createTextNode(pasto);
            var cont_modalita = document.createTextNode(data[x]['modalita']);

            var row = document.createElement("div");
            $(row).addClass('row');
            var col = document.createElement("div");
            $(col).addClass('col-6');
            var button = document.createElement("a");
            $(button).addClass('btn btn-primary btn-rounded');
            var cont_button = document.createTextNode('Elimina');
            var col2 = document.createElement("div");
            $(col2).addClass('col-6');
            var button2 = document.createElement("a");
            $(button2).addClass('btn btn-primary btn-rounded');
            var cont_button2 = document.createTextNode('Modifica');

            $(button).attr('value', data[x]['_id']);
            $(button2).attr('value', data[x]['_id']);
            $(button).click(function () {
                elimina($(this).attr('value'));
            });
            $(button2).click(function () {
                id = $(this).attr('value');
                sessionStorage.setItem('id_prenotazione',id);           
                /*id_session($(this).attr('value')); */
                window.location.href = "/modifica";
            });


            par.appendChild(cont_date);
            par2.appendChild(cont_pasto);
            par3.appendChild(cont_modalita);
            button.appendChild(cont_button);
            button2.appendChild(cont_button2);
            col.appendChild(button);
            col2.appendChild(button2);
            row.appendChild(col2)
            row.appendChild(col)
            td.appendChild(par);
            td2.appendChild(par2);
            td3.appendChild(par3);
            td4.appendChild(row)
            tr.appendChild(td)
            tr.appendChild(td2)
            tr.appendChild(td3)
            tr.appendChild(td4)

            document.getElementById('table').appendChild(tr);


        }}

    });


}



function elimina(element) {
    $.ajax({
        url: "/elimina",
        type: 'POST',
        data: {'id': element}
    }).done(function(data){
        if (data.success) {
        $("#table").empty();
        loadtable();
        }
    }
    )  
    ;

}




