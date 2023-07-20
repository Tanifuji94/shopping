from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

conn.commit()


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg =  request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')
    
    if db.login(user_name, password):
        session['user'] = True 
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('mypage'))
    else :    
        error = 'ログインに失敗しました。'
        input_data ={
            'user_name' : user_name,
            'password' : password
        }
        return render_template('index.html', error=error, data=input_data)
    
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))
    
@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else :
        return redirect(url_for('index'))
    
@app.route('/search')
def sample_search():
    return render_template('search.html')
    
@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/question')
def question_form():
    return render_template('question.html')

@app.route('/list')
def sample_list():
    goods_list = db.select_all_goods()
    return render_template('list.html', goods=goods_list)

@app.route('/sample-register')
def sample_register():
    return render_template('goods.html')

@app.route('/cart_form')
def cart_form():
    return render_template('cart.html')

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form['quantity'])
    
    # カートがセッションに存在しない場合、空のリストを初期化
    cart = session.get('cart', [])
    
    # カートに追加する商品情報を取得
    product = db.select_product_by_id(product_id)
    
    # カートに商品を追加
    cart.append({
        'product_id': product[0],
        'name': product[1],
        'price': product[2],
        'quantity': quantity
    })
    
    # カート情報をセッションに保存
    session['cart'] = cart
    
    return render_template('cart.html')

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    # Remove the item from the cart by matching the product_id
    cart = [item for item in cart if item['product_id'] != product_id]
    session['cart'] = cart
    return render_template('cart.html')


@app.route('/list_exe', methods=['POST'])
def list_exe():
    name = request.form.get('name')
    price = request.form.get('price')
    explanation = request.form.get('explanation')
    category = request.form.get('category')
    stock = request.form.get('stock')
    
    if name == '':
        error = '商品名が未入力です。'
        return render_template('goods.html', error=error)
    if price == '':
        error = '商品の価格が未入力です。'
        return render_template('goods.html', error=error)
    if category == '':
        error = '商品のカテゴリーが未入力です。'
        return render_template('goods.html', error=error)
    if stock == '':
        error = '商品の在庫が未入力です。'
        return render_template('goods.html', error=error)
    
    db.insert_goods(name, price, explanation, category, stock)
    
    goods_list = db.select_all_goods()
    
    return render_template('list.html', goods=goods_list)

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/submit', methods=['POST'])
def submit():

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    return render_template('thank.html', name=name)

@app.route('/delete_form')
def delete_form():
    return render_template('delete_form.html')

@app.route('/delete_shopping', methods=['POST'])
def delete_shopping():
    shopping = request.form.get('id')
    
    if shopping == '':
        error = '未入力です。'
        return render_template('delete_form.html', error=error)
        
    count = db.delete_shopping(shopping)
        
    if count == 1:
        msg = '削除が完了しました。'
        return render_template('delete_form.html', msg=msg)
    else:
        error = '削除に失敗しました。'
        return render_template('delete_form.html', error=error)

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')
    
    if user_name == '':
        error = 'ユーザー名が未入力です。'
        return render_template('register.html', error=error)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error=error)
    
    count = db.insert_user(user_name, password)
    
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)