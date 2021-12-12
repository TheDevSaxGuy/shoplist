from flask import request,make_response, redirect,render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required, current_user
from app.forms import ProductForm, DeleteProductForm, TotalCapitalForm, UpdateProductDoneForm
from app.firestore_service import get_users, get_products, get_total, put_product, delete_product, put_capital, get_capital, update_product

import unittest

from app import create_app

app = create_app()

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response

@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username= current_user.id
    product_form = ProductForm()
    delete_form = DeleteProductForm()
    update_form = UpdateProductDoneForm()
    capital_form = TotalCapitalForm()
    capital = get_capital(user_id = username).to_dict()['capital']

    context={
        'user_ip' : user_ip, 
        'products' : get_products(user_id = username),
        'username': username,
        'total' : get_total(user_id = username),
        'product_form': product_form,
        'delete_form': delete_form,
        'capital_form': capital_form,
        'capital': capital,
        'update_form': update_form,
    }
    print(get_capital(user_id = username).to_dict()['capital'])
    if product_form.validate_on_submit():
        description = product_form.description.data
        price = product_form.price.data
        put_product(user_id = username, description = description, price = price)
        flash('Product agregado con éxito')
        return redirect(url_for('hello'))
    
    if capital_form.validate_on_submit():
        capital = capital_form.capital.data
        put_capital(user_id = username, capital = capital)
        flash('Presupuesto actualizado')
        return redirect(url_for('hello'))

    return render_template('hello.html',**context)

@app.route('/products/delete/<product_id>', methods=['POST'])
def delete(product_id):
    user_id = current_user.id
    delete_product(user_id=user_id, product_id = product_id)
    return redirect(url_for('hello'))

@app.route('/products/update/<product_id>/<int:done>', methods=['POST'])
def update(product_id, done):
    user_id = current_user.id
    update_product(user_id=user_id, product_id=product_id, done=done)
    return redirect(url_for('hello'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error)

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)