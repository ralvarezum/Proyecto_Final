from flask import request, render_template, redirect, url_for, make_response
from flask import current_app as app
from .modelos import db, Persona, Tarjeta, Venta

@app.route('/tarjeta/')
def tarjeta():
    tarjetas = Tarjeta.get_all()
    return render_template("tarjeta/index.html",
                           tarjetas=tarjetas,
                           titulo='Tarjetas')

@app.route("/tarjeta/crear", methods=["GET"])
def tarj_crear():
    personas = Persona.get_all()
    return render_template("tarjeta/crear.html",
                           personas=personas,
                           titulo='Crear nueva')

@app.route("/tarjeta/crear", methods=["POST"])
def tarj_agregar():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        numero = request.form.get('numero')
        cods = request.form.get('cods')
        mes = request.form.get('mes')
        año = request.form.get('año')
        montomax = request.form.get('montomax')
        personas = request.form.getlist('personas')
    if tipo and numero and cods and mes and 0 < int(mes) < 13 and año and int(año) > 2019 and montomax:
        tarj = Tarjeta(tipo=tipo, numero=numero, cods=cods, mes=mes, año=año, montomax=montomax)
        db.session.add(tarj)
        db.session.commit()
        for persona_id in personas:
            persona = Persona.find_by_id(persona_id)
            persona.tarjetas.append(tarj)
            persona.update()
    else:
        return render_template('/tarjeta/errormes.html')
    return redirect(url_for('tarjeta'))

@app.route('/tarjeta/delete')
def tarj_delete():
    tarjeta_id = int(request.args['id'])
    tarjeta = Tarjeta.find_by_id(tarjeta_id)
    db.session.delete(tarjeta)
    db.session.commit()
    return redirect('/tarjeta')

@app.route('/tarjeta/update', methods=['GET', 'POST'])
def tarj_update():
    tarjeta_id = int(request.args['id'])
    tarjeta = Tarjeta.find_by_id(tarjeta_id)
    if request.method == 'POST':
        tarjeta.tipo = request.form.get('tipo')
        tarjeta.numero = request.form.get('numero')
        tarjeta.cods = request.form.get('cods')
        tarjeta.mes = request.form.get('mes')
        tarjeta.año = request.form.get('año')
        tarjeta.montomax = request.form.get('montomax')
        if 0 < int(tarjeta.mes) < 13  and int(tarjeta.año) > 2019:
            db.session.commit()
        else:
            return render_template('/tarjeta/errormes.html')
        return redirect('/tarjeta')
    else:
        return render_template('/tarjeta/update.html', tarjeta=tarjeta)

@app.route("/tarjeta/detalle", methods=['GET'])
def tarj_detalles():
    tarjeta_id = int(request.args['id'])
    tarjeta = Tarjeta.find_by_id(tarjeta_id)
    return render_template("tarjeta/detalle.html", tarjeta=tarjeta)
