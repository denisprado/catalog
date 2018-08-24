import os
import tempfile
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Foto, Arte, Festa, Arquivo, Objeto, FormatoArquivo, ItensFesta
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./assets/uploads/fotos"
ALLOWED_EXTENSIONS = set(["jpg", "gif", "png", "jpge"])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


engine = create_engine('sqlite:///festas_de_papel.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/fotos/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
@app.route('/fotos')
def listFoto():
    fotos = session.query(Foto).all()
    return render_template('fotos.html', fotos=fotos)


@app.route('/fotos/new', methods=['POST', 'GET'])
def newFoto():

    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Sem arquivo")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("Arquivo nao selecionado")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newFoto = Foto(foto_caminho=filename)
            session.add(newFoto)
            session.commit()
            return redirect(url_for('listFoto'))
    return render_template('newFoto.html')


@app.route('/foto/<int:id>/edit',
           methods=['GET', 'POST'])
def editFoto(id):
    editedFoto = session.query(Foto).filter_by(id=id).one()
    if request.method == 'POST':
        file = request.files['file']
        print(request.files)
        if file:
            filename = secure_filename(file.filename)
            editedFoto.foto_caminho = filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session.add(editedFoto)
            session.commit()
            return redirect(url_for('listFoto'))
    else:

        return render_template(
            'editFoto.html', id=id, foto=editedFoto)


@app.route('/festas')
def listFesta():
    fotos = session.query(Foto).all()
    festas = session.query(Festa).all()
    return render_template('festas.html', festas=festas, fotos=fotos)


@app.route('/festas/new', methods=['GET', 'POST'])
def newFesta():
    fotos = session.query(Foto).all()
    if request.method == 'POST':  # response from template form
        newFesta = Festa(festa_nome=request.form['name'], festa_descr=request.form[
            'description'], festa_valor=request.form['price'], festa_foto=request.form['foto'])
        session.add(newFesta)
        session.commit()
        return redirect(url_for('listFesta'))
    else:
        return render_template('newfesta.html', fotos=fotos)


@app.route('/festa/<int:id>/edit',
           methods=['GET', 'POST'])
def editFesta(id):
    fotos = session.query(Foto).all()
    editedFesta = session.query(Festa).filter_by(id=id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedFesta.festa_nome = request.form['name']
        if request.form['description']:
            editedFesta.festa_descr = request.form['description']
        if request.form['price']:
            editedFesta.festa_valor = request.form['price']
        if request.form['foto']:
            editedFesta.festa_valor = request.form['foto']
        session.add(editedFesta)
        session.commit()
        return redirect(url_for('listFesta'))
    else:

        return render_template(
            'editFesta.html', festa_id=id, festa=editedFesta, fotos=fotos)


@app.route('/festa/<int:id>/delete',
           methods=['GET', 'POST'])
def deleteFesta(id):
    festaToDelete = session.query(Festa).filter_by(id=id).one()
    if request.method == 'POST':
        session.delete(festaToDelete)
        session.commit()
        return redirect(url_for('listFesta'))
    else:
        return render_template('deleteFesta.html', festa=festaToDelete)


if __name__ == '__main__':
    app.secret_key = "my_incredible_token_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
