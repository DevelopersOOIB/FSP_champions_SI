from flask import Flask, session, render_template, redirect, request, jsonify, flash, url_for
import database
import uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['SESSION_COOKIE_HTTPONLY'] = False


@app.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        #render_template
        return redirect('/profile')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/')

    if request.method == 'GET':
        return render_template('login.html')
    
    if 'login' not in request.form:
        error = "Должны быть указаны логин и пароль"
        return render_template('login.html', error=error)
    if 'password' not in request.form:
        error = "Должны быть указаны логин и пароль"
        return render_template('login.html', error=error)
    

    login = request.form['login']
    password = request.form['password']

    if not (login and password):
        error = "Должны быть указаны логин и пароль"
        return render_template('login.html', error=error)

    user = database.login(login, password)

    if not user:
        error = "Неверный логин или пароль"
        return render_template('login.html', error=error)


    #return jsonify(user)
    session["user_id"] = user["id"]
    
    return redirect('/')    


@app.route('/logout', methods=['GET'])
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')



@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if 'user_id' in session:
        return redirect('/profile')

    if request.method == 'GET':
        return render_template('create_account.html')

    if 'login' not in request.form:
        error = "Должны быть указаны логин и пароль"
        return render_template('create_account.html', error=error)
    if 'password' not in request.form:
        error = "Должны быть указаны логин и пароль"
        return render_template('create_account.html', error=error)  
    
    login = request.form['login']
    password = request.form['password']

    if not (login and password):
        error = "Должны быть указаны логин и пароль"
        return render_template('create_account.html', error=error)

    if database.check_if_login_taken(login=login):
        error = "Логин занят"
        return render_template('create_account.html', error=error)
    
    user = database.create_account(login=login, password=password)

    if not user:
        return redirect('/')
    
    session["user_id"] = user["id"]
    return redirect('/profile')
     

@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('profile.html', user_id=session['user_id'])


@app.route('/api/profile/<int:user_id>', methods=['GET'])
def api_profile(user_id):
    if 'user_id' not in session:
        return jsonify({"error":"Access denied"})
    
    #if not isinstance(user_id, int):
    #    return jsonify({"error":"Type Error"})
    
    user = database.proflie(user_id)

    return jsonify({"profile":user})
    

@app.route('/shop', methods=['GET'])
def shop():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('shop.html')


@app.route('/api/shop', methods=['GET'])
def api_shop():
    if 'user_id' not in session:
        return jsonify({"error":"Access denied"})

    products = database.shop()

    return jsonify({"products":products})


@app.route('/add_to_buscket', methods=['POST'])
def add_to_bucket():
    if 'user_id' not in session:
        return redirect('/')
    
    if 'product_id' not in request.form:
        error = "Возникли ошибки при добавлении товара в корзину"
        flash(error, "error")
        return redirect(url_for('shop'))
    
    product_id = request.form['product_id']

    if not product_id:
        error = "Возникли ошибки при добавлении товара в корзину"
        flash(error, "error")
        return redirect(url_for('shop'))
    
    try:
        product_id = int(product_id)
    except Exception as e:
        return redirect('/')

    status = database.add_product_to_bucket(session['user_id'], product_id)

    if not status:
        error = "Возникли ошибки при добавлении товара в корзину"
        flash(error, "error")
        return redirect(url_for('shop'))
    
    success = "Товар добавлен в корзину"
    flash(success, "success")
    return redirect(url_for('shop'))


@app.route('/delete_from_buscket', methods=['POST'])
def delete_from_bucket():
    if 'user_id' not in session:
        return redirect('/')
    
    if 'buscket_id' not in request.form:
        error = "Возникли ошибки при удалении товара из корзины"
        flash(error, "error")
        return redirect(url_for('bucket'))
    
    bucket_id = request.form['buscket_id']

    if not bucket_id:
        error = "Возникли ошибки при удалении товара из корзины"
        flash(error, "error")
        return redirect(url_for('bucket'))
    
    status = database.delete_from_bucket(bucket_id ,session['user_id'])

    if not status:
        error = "Ошибка при удалении товара из корзины"
        flash(error, "error")
        return redirect(url_for('bucket'))
    
    success = "Товар удален из корзины"
    flash(success, "success")
    return redirect(url_for('bucket'))


@app.route('/clear_buscket', methods=['GET'])
def clear_bucket():
    if 'user_id' not in session:
        return redirect('/')
    
    status = database.clear_bucket(session['user_id'])

    if not status:
        error = "Ошибка при очистке корзины"
        flash(error, "error")
        return redirect(url_for('bucket'))
    
    success = "Корзина была очищена"
    flash(success, "success")
    return redirect(url_for('bucket'))


@app.route('/buscket', methods=['GET'])
def bucket():
    if 'user_id' not in session:
        return redirect('/')

    account_number = database.get_account_number(session['user_id'])
    
    if not account_number:
        return redirect('/')
    
    return render_template('bucket.html', account_number=account_number)


@app.route('/api/buscket', methods=['GET'])
def api_bucket():
    if 'user_id' not in session:
        return jsonify({"error":"Access denied"})

    bucket = database.bucket(session['user_id'])
    return jsonify({"busckets":bucket})


@app.route('/pay', methods=['POST'])
def pay():
    if 'user_id' not in session:
        return redirect('/')
    
    if 'buscket_id' not in request.form:
        error = "Ошибка при покупке товара"
        flash(error, "error")
        return redirect(url_for('bucket'))
    
    if 'account_number' not in request.form:
        error = "Ошибка при покупке товара"
        flash(error, "error")
        return redirect(url_for('bucket'))
    
    bucket_id = request.form['buscket_id']
    account_number = request.form['account_number']

    if not (bucket_id and account_number):
        error = "Ошибка при покупке товара"
        flash(error, "error")
        return redirect(url_for('bucket'))

    payment_result = database.pay(bucket_id, account_number, session['user_id'])

    if not payment_result:
        error = "Ошибка при покупке товара"
        flash(error, "error")
        return redirect(url_for('bucket'))
    
    if "error" in payment_result:
        error = "Недостаточно средств"
        flash(error, "error")
        return redirect(url_for('bucket'))

    success = "Товар был оплачен! Перейдите в заказы"
    flash(success, "success")
    return redirect(url_for('bucket'))


@app.route('/pay_all', methods=['POST'])
def pay_all():
    if 'user_id' not in session:
        return redirect('/')

    payment_result = database.pay_all(session['user_id'])
    
    if not payment_result:
        error = "Ошибка при покупке товаров"
        flash(error, "error")
        return redirect(url_for('bucket'))
    
    if "error" in payment_result:
        error = payment_result["error"]
        flash(error, "error")
        return redirect(url_for('bucket'))
    
    success = "Все товары в корзине былы оплачены! Перейдите в заказы"
    flash(success, "success")
    return redirect(url_for('bucket'))


@app.route('/orders', methods=['GET'])
def orders():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('orders.html')


@app.route('/api/orders', methods=['GET'])
def api_orders():
    if 'user_id' not in session:
        return jsonify({"error":"Access denied"})

    orders = database.orders(session['user_id'])
    return jsonify({"orders":orders}) 


@app.route('/orders/<order_id>', methods=['GET'])
def order_by_id(order_id):
    if 'user_id' not in session:
        return redirect('/')
    
    if not database.check_access_to_order(session['user_id'], order_id):
        return redirect('/')

    return render_template('order.html', order_id=order_id)
 

@app.route('/api/orders/<order_id>', methods=['GET'])
def api_orders_by_id(order_id):
    if 'user_id' not in session:
        return jsonify({"error":"Access denied"})
    
    if not database.check_access_to_order(session['user_id'], order_id):
        jsonify({"order":False})
    
    order = database.order_by_id(session['user_id'], order_id)
    return jsonify({"order":order})

#s
if __name__ == "__main__":
    database.init_db()
    app.run(debug=False, host="0.0.0.0")