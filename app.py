from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta

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

@app.route('/list_exe', methods=['POST'])
def list_exe():
    name = request.form.get('name')
    price = request.form.get('price')
    explanation = request.form.get('explanation')
    category = request.form.get('category')
    stock = request.form.get('stock')
    
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