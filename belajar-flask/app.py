from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from backend.db import db 

from backend.auth import auth
from backend.mahasiswa import mahasiswa
app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = '4p44p4'

app.register_blueprint(auth)
app.register_blueprint(mahasiswa)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dosen', methods = ['POST', 'GET'])
def dosen(): 
    if 'user' not in session:
        flash('Anda Harus login', 'danger')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        #simpan dictonary
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'nidn' : request.form['nidn'],
            'matakuliah' : request.form['dosen'],
            'is_active' : True
        }
        #simpan database
        db.collection('dosen').document().set(data)
        flash('Berhasil Menambahkan Dosen','success')
        return redirect(url_for('dosen'))
    
    #panggil database
    dos = db.collection('dosen').stream()
    dos_mk = []
    for dosen in dos:
        dosn = dosen.to_dict()
        dosn['id'] = dosen.id
        dos_mk.append(dosn)

    jurs = db.collection('jurusan').stream()
    data = []
    for jur in jurs:
        usr = jur.to_dict()
        usr['id'] = jur.id
        data.append(usr)
    return render_template('dosen.html', dosmat = dos_mk, jurusan = data)

@app.route('/mahasiswa', methods =['POST','GET'])
def mahasiswa():
    if 'user' not in session:
        flash('Anda Harus login', 'danger')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        #simpan dictonary
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'nim' : request.form['nim'],
            'jurusan' : request.form['jurusan'],
            'is_active' : True
        }
        #simpan database
        db.collection('mahasiswa').document().set(data)
        flash('Berhasil Menambahkan Mahasiswa','success')
        return redirect(url_for('mahasiswa'))
    
    #panggil database
    docs = db.collection('mahasiswa').stream()
    mhs = []
    for doc in docs:
        user = doc.to_dict()
        user['id'] = doc.id
        mhs.append(user)

    jurs = db.collection('jurusan').stream()
    data = []
    for jur in jurs:
        usr = jur.to_dict()
        usr['id'] = jur.id
        data.append(usr)

    return render_template('mahasiswa.html', students = mhs, jurusan=data)


@app.route('/mahasiswa/lihat/<uid>')
def lihat_mahasiswa(uid):
    mahasiswa = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('lihat_mahasiswa.html', data = mahasiswa)

@app.route('/mahasiswa/delete', methods= ['POST'])
def delete_mahasiswa():
    uid = request.form['uid']
    db.collection('mahasiswa').document(uid).delete()
    flash('Berhasil Hapus Mahasiswa', 'danger')
    return redirect(url_for('mahasiswa'))

@app.route('/mahasiswa/edit/<uid>', methods=['GET','POST'])
def edit_mhs(uid):
    if request.method == 'POST':
         #simpan dictonary
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'nim' : request.form['nim'],
            'jurusan' : request.form['jurusan']
        }
        #simpan database
        db.collection('mahasiswa').document(uid).set(data, merge=True)
        flash('Berhasil Edit Mahasiswa','success')
        return redirect(url_for('mahasiswa'))
    mahasiswa = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('edit_mhs.html', data = mahasiswa)


#code menjalankan flask
if __name__ == '__main__':
    app.run(debug=True)
