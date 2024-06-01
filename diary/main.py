from flask import Flask, render_template,request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


app.secret_key = "DENEME"
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfaya erişmek için giriş yapmalısınız")
            return redirect("/")
    return decorated_function


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'
    

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(30), nullable=False)





@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            users_db = User.query.all()
            for user in users_db:
                if form_login == user.email and form_password == user.password:
                    session["logged_in"] = True
                    session["email"] = user.email
                    return redirect('/index')
                else:
                    error = 'Hatalı giriş veya şifre'
            return render_template('login.html', error=error)


            
        else:
            return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        
        kullanıcı = User(email=email, password=password)
        db.session.add(kullanıcı)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


@app.route('/index')
@login_required
def index():
    cards = Card.query.order_by(Card.id).all()
    print(session["email"])
    return render_template('index.html', cards=cards)

@app.route('/card/<int:id>')
@login_required
def card(id):
    card = Card.query.get(id)
    print(session["email"])
    return render_template('card.html', card=card)

@app.route('/create')
@login_required
def create():
    print(session["email"])
    return render_template('create_card.html')

@app.route('/form_create', methods=['GET','POST'])
@login_required
def form_create():
    print(session["email"])
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        card = Card(title=title, subtitle=subtitle, text=text)
        
        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
         db.create_all()
    app.run(debug=True)
