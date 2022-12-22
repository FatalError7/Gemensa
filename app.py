from flask import Flask, render_template, request, redirect, session, url_for, jsonify, json, make_response, send_from_directory
from pymongo import MongoClient
import bcrypt
import uuid
from datetime import datetime,timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["Gemensa"]
user = db["User"]
prenotazioni = db['Prenotazioni']
app = Flask(__name__)
app.secret_key = 'gemensakey'
UPLOAD_FOLDER = '/static/assets/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    if request.method == 'POST':
        login_user = user.find_one({"username": request.form['username']})
        if login_user:
            passw = request.form['password']
            if bcrypt.checkpw(passw.encode('utf-8'), login_user['password']):
                session["_id"] =login_user["_id"] 
                session["username"] = request.form['username']
                session["nome"] = login_user['nome']
                if 'cognome' in login_user : session["cognome"] = login_user['cognome']
                if 'cf' in login_user : session["cf"] = login_user['cf']
                session['isMensa'] = login_user['isMensa']
                if 'isAdmin' in login_user : session['isAdmin'] = login_user['isAdmin']
                return jsonify({'success': 'true'})
            return jsonify({'error': '2'}) #render_template('index.html', error=2)
        return jsonify({'error': '1'}) #render_template('index.html', error=1)
    return render_template('index.html')


@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if "username" in session:
        if session['isMensa'] == 'true':
           return render_template('dashboard_mensa.html') 
        if session['isAdmin'] == 'true':
           return render_template('dashboard_admin.html')
        return render_template('dashboard.html')        
    return render_template('index.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(url_for("dashboard"))
    if request.method == 'POST':
        username = request.form['username']
        signin_user = user.find_one({"username": username})
        if signin_user:
            return "Utente già esiste"
        else:
            if request.form['password'] != request.form['passwordc']:
                return "Le password non coincidono"
            else:
                hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                user.insert_one({
                    "_id": uuid.uuid4().hex,
                    "username": request.form['username'],
                    "password": hashed,                    
                    "cognome": request.form['cognome'],
                    "nome": request.form['nome'],
                    "cf": request.form['cf'],                    
                    "isMensa": "false",       
                })
                return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    session.pop('nome', None)
    session.pop('cognome', None)
    session.pop('_id', None)
    return redirect(url_for('index'))


@app.route('/prenota/', methods=['POST', 'GET'])
def prenota():
    if request.method == 'POST':
        if 'colazione' in request.form : colazione = request.form['colazione'] 
        else: colazione = 'false'
        if 'pranzo' in request.form : pranzo= request.form['pranzo']
        else: pranzo = 'false'
        if 'cena' in request.form : cena = request.form['cena']
        else: cena= 'false'
        if colazione=='false' and pranzo=='false' and cena=='false':
          return render_template('prenota.html', error=1)
        
        #Check della data
        datafrom = request.form['datafrom']
        datato = request.form['datato']
        datacheck='true'

        if datafrom>datato: 
            datacheck ='false'        
        oggi = datetime.now().strftime("%Y-%m-%d")
        ora = datetime.now().strftime("%H")

        if datafrom<=oggi: 
            datacheck='false'
        domani = (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d")
        if ora>"14" and datafrom<domani :
            datacheck='false'
        if datacheck == 'false':
            return render_template('prenota.html',error=2)        
        
                   
        
        #Controllo se le date inserite esistono nel Db
        a = datetime.strptime(datafrom, '%Y-%m-%d')
        b = datetime.strptime(datato, '%Y-%m-%d')
        c = b-a
                
        result = prenotazioni.find({
            "id_user": session['_id'],
            "data": {"$gte": a,"$lte": b}
         })        
        result_count = 0
        for x in result:
            result_count=1

        if result_count!=0:
            return render_template('prenota.html', error=3)
        
        #Inserimento Prenotazioni in Db
        modalita = request.form['modalita']
        for x in range(0, c.days+1):
            data = a+timedelta(days=x)
            prenotazioni.insert_one({
                "_id": uuid.uuid4().hex,
                "id_user": session['_id'],
                "data": data,
                "modalita": modalita,
                "prenotato_colazione": colazione,
                "prenotato_pranzo": pranzo,
                "prenotato_cena": cena,
                "usufruito_colazione": "false",
                "usufruito_pranzo": "false",
                "usufruito_cena": "false",
                })
        return redirect(url_for('dashboard'))
    return render_template('prenota.html')


@app.route('/elimina/', methods=['POST', 'GET'])
def elimina():
    if request.method == 'POST':
      id =  request.get_data()
      data = id[3:]
      enc_data = data.decode("utf-8")      
      prenotazioni.delete_one({'_id': enc_data })      
      return jsonify({'success': 'true'})
    


@app.route('/table/', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        result = prenotazioni.find({
            "id_user": session['_id'],
            "data": {"$gte": datetime.now()}
        })

        results = list(result)
        if results:
            return jsonify(results)
        else: return jsonify({'error':'true'})



@app.route('/modifica/', methods=['GET', 'POST'])
def modifica():
    if request.method == 'POST':  

        id_ = request.form['id']
        colazione = request.form['colazione']
        pranzo = request.form['pranzo']
        cena=request.form['cena']
        modalita = request.form['modalita']

        query= {'_id': id_}
        newval= {
            "prenotato_colazione": colazione,
            "prenotato_pranzo": pranzo,
            "prenotato_cena": cena,
            'modalita': modalita
        }
        prenotazioni.update_one(query,{'$set': newval})
        return jsonify({'success': 'true'})
    return render_template('modifica.html')
       
        
@app.route('/profilo/', methods=['GET', 'POST'])
def profilo():
    if request.method == 'POST':
        if request.form['password'] != request.form['passwordc']:
            return jsonify({'error': '1'}) #Le password nn coincidono
        else:
            hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            query = {'_id': session['_id']}
            newval = {
                "username": request.form['username'],
                "cognome": request.form['cognome'],
                "nome": request.form['nome'],
                'cf': request.form['cf'],
                'password': hashed
            }
            user.update_one(query, {'$set': newval})
            
            session["username"] = request.form['username']
            session["nome"] = request.form['nome']
            session["cognome"] = request.form['cognome']
            session["cf"] = request.form['cf']
            

            return jsonify({'success': 'true'})
    return render_template('profilo.html')


@app.route('/accettazione/', methods=['GET', 'POST'])
def accettazione():
    ora = datetime.now().strftime('%H')
    if ora >= '06' and ora <= '09':
        tempo = 'Colazione'
    else:
        if ora >= "11" and ora <= "14":
            tempo = 'Pranzo'
        else:
            if ora >= "18" and ora <= "21":
               tempo = 'Cena'
            else:
                tempo= 'chiusa'

    if request.method== 'POST':
        username = request.form['username']
        user_find = user.find_one({"username": username})
        if user_find:
            data=datetime.now().strftime('%Y-%m-%d')
            oggi=datetime.strptime(data, '%Y-%m-%d')
            query = {'id_user': user_find['_id'],'data':oggi}
            prenotazione_find= prenotazioni.find_one(query)
            if tempo == 'Colazione':
                if prenotazione_find['prenotato_colazione']=='true':
                    if prenotazione_find['usufruito_colazione'] == 'false':
                        newval = {
                        "usufruito_colazione": 'true',
                        }
                        prenotazioni.update_one(query, {'$set': newval})
                        return jsonify({'success': (user_find['nome']) + ' ' + (user_find['cognome'])})
                    return jsonify({'error': 'Utente ha già usufruito'})
                return jsonify({'error': 'Utente non prenotato'})
            if tempo == 'Pranzo':
                if prenotazione_find['prenotato_pranzo'] == 'true':
                    if prenotazione_find['usufruito_pranzo'] == 'false':
                        newval = {
                            "usufruito_pranzo": 'true',
                        }
                        prenotazioni.update_one(query, {'$set': newval})
                        return jsonify({'success': (user_find['nome']) + ' ' + (user_find['cognome'])})
                    return jsonify({'error': 'Utente ha già usufruito'})
                return jsonify({'error': 'Utente non prenotato'})
            if tempo == 'Cena':
                if prenotazione_find['prenotato_cena'] == 'true':
                    if prenotazione_find['usufruito_cena'] == 'false':
                        newval = {
                            "usufruito_cena": 'true',
                        }
                        prenotazioni.update_one(query, {'$set': newval})
                        return jsonify({'success': (user_find['nome']) + ' ' + (user_find['cognome'])})
                    return jsonify({'error': 'Utente ha già usufruito'})
                return jsonify({'error': 'Utente non prenotato'})
        return jsonify({'error': 'Username errato'}) 
     
    if tempo=='chiusa':
        return render_template('mensa_chiusa.html')
    return render_template('accettazione.html',tempo=tempo)


@app.route('/liste/', methods=['GET', 'POST'])
def liste():
    if request.method == 'POST':
        #Inserire i dati in session
        session['table_pasto']= request.form['pasto']
        session['table_giorno']= request.form['giorno']
        return jsonify({'success': 'true'})
    return render_template('liste.html')


@app.route('/lista/', methods=['GET', 'POST'])
def lista():
    if request.method == 'POST':
        #Creazione table lista
        data= session['table_giorno']
        pasto_p = 'prenotato_'
        pasto_u = 'usufruito_'
        d = datetime.strptime(data, '%Y-%m-%d')
        if session['table_pasto'] == 'Colazione':
             pasto_p=pasto_p+'colazione' 
             pasto_u = pasto_u+'colazione'
        if session['table_pasto'] == 'Pranzo':
             pasto_p=pasto_p+'pranzo'
             pasto_u = pasto_u+'pranzo'
        if session['table_pasto'] == 'Cena':
             pasto_p = pasto_p+'cena' 
             pasto_u = pasto_u+'cena'
       
        p_find = prenotazioni.aggregate([
            {
                '$match':
                {
                    'data': d,
                    pasto_p : 'true'
                }
            },
            {'$lookup':
             {
                 'from': "User",
                 'localField': 'id_user',
                 'foreignField': '_id',
                 'as': "info"
             }
             }
        ])
        
        result= dict()
        i=1
        for x in p_find:
            if x[pasto_u]=='true':
                pasto='Si'
            else: 
                pasto='No'
            result[i] = {'cognome': x['info'][0]['cognome'], 'nome': x['info'][0]['nome'], 'modalita': x['modalita'],'affluito': pasto}
            i=i+1        
        print(result)
        if len(result)!=0:
            return jsonify(result)
        return jsonify({'error': 'true'})
         
    return render_template('lista.html', pasto=session['table_pasto'], giorno=session['table_giorno'])


@app.route('/prenotati/', methods=['GET', 'POST'])
def prenotati():
    if request.method == 'POST':
        # Creazione table lista
        data = session['table_giorno']
        pasto_p = 'prenotato_'
        pasto_u = 'usufruito_'
        d = datetime.strptime(data, '%Y-%m-%d')
        if session['table_pasto'] == 'Colazione':
            pasto_p = pasto_p+'colazione'
            pasto_u = pasto_u+'colazione'
        if session['table_pasto'] == 'Pranzo':
            pasto_p = pasto_p+'pranzo'
            pasto_u = pasto_u+'colazione'
        if session['table_pasto'] == 'Cena':
            pasto_p = pasto_p+'cena'
            pasto_u = pasto_u+'colazione'

        p_count = prenotazioni.find({pasto_p:'true','data': d}).count()
        return jsonify({'prenotati': p_count})


@app.route('/statistiche/', methods=['GET', 'POST'])
def statistiche():
    if request.method=='POST':
        d= datetime.now().strftime('%Y-%m-%d')
        dd = datetime.strptime(d, '%Y-%m-%d')

        print(dd)
        p_count = prenotazioni.find({'data': dd})
        p= list(p_count)
        print(p)
        p_col = 0
        u_col = 0
        m_col = 0
        p_pranzo=0
        u_pranzo=0
        m_pranzo=0
        p_cena = 0
        u_cena = 0
        m_cena = 0
        perc_col = 0
        perc_pra = 0
        perc_ce = 0
        for x in p:
            if x['prenotato_colazione'] == 'true':
                p_col=p_col+1
                if x['usufruito_colazione']== 'true':
                    u_col= u_col+1
                else:
                    m_col = m_col+1
            if x['prenotato_pranzo'] == 'true':
                print('entrato')
                p_pranzo = p_pranzo+1
                if x['usufruito_pranzo'] == 'true':
                    u_pranzo = u_pranzo+1
                else:
                    m_pranzo = m_pranzo+1
            if x['prenotato_cena'] == 'true':
                p_cena = p_cena+1
                if x['usufruito_cena'] == 'true':
                    u_cena = u_cena+1
                else:
                    m_cena = m_cena+1
        if p_col != 0 : perc_col= (100/p_col)*u_col
        if p_pranzo != 0: perc_pra = (100/p_pranzo)*u_pranzo
        if p_cena != 0 : perc_ce = (100/p_cena)*u_cena
        result= {
            'prenotati_colazione': p_col,
            'prenotati_pranzo': p_pranzo,
            'prenotati_cena': p_cena,
            'usufruiti_colazione' : u_col,
            'usufruiti_pranzo': u_pranzo,
            'usufruiti_cena': u_cena,
            'mancanti_colazione': m_col,
            'mancanti_pranzo': m_pranzo,
            'mancanti_cena': m_cena,            
            'perc_col': perc_col,
            'perc_pra': perc_pra,
            'perc_ce': perc_ce,
        }
        print(result)
        return jsonify(result)


    return render_template('statistiche.html')


@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if request.method=='POST':
        login_user = user.find_one({"username": request.form['username']})
        if login_user:
            session["find_id"] = login_user["_id"]
            session["find_cf"] = login_user['cf']
            session["find_nome"] = login_user['nome']
            session["find_cognome"] = login_user['cognome']
            
            return jsonify({'success': 'true'})       
        return jsonify({'error': 'true'})


@app.route('/update/', methods=['GET', 'POST'])
def update():
    if request.method=='POST':
        hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        query = {'_id': session['find_id']}        
        if 'nome' in request.form:
            newval = {
                "nome": request.form['nome'],
            }
            user.update_one(query, {'$set': newval})
        if 'cognome' in request.form:
            newval = {
                "cognome": request.form['cognome'],
            }
            user.update_one(query, {'$set': newval})
        if 'cf' in request.form:
            newval = {
                "cf": request.form['cf'],
            }
            user.update_one(query, {'$set': newval})
        if request.form['password'] != '':
            newval = {
                "password": hashed,
            }
            user.update_one(query, {'$set': newval})


        return jsonify({'success': 'true'})




@app.route('/sw.js')
def sw():
    response = make_response(send_from_directory('', 'sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response


@app.route('/main.js')
def main():
    response = make_response(send_from_directory('', 'main.js'))
    response.headers['Content-Type'] = 'application/javascript'
    return response



@app.route('/manifest.json')
def manifest():
    return send_from_directory('', 'manifest.json')


if __name__ == '__main__':
    app.secret_key = 'gemensakey'
    app.run(debug=True)
