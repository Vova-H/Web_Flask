from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    dis = db.Column(db.String(300), nullable=True)
    price = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return '<Product %r>' % self.id  # функция возвращающая обьект+ его id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/posters')
def poster():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template("posters.html", products=products)


@app.route('/posters/<int:id>')
def poster_view(id):
    product = Product.query.get(id)
    return render_template("post_view.html", product=product)


@app.route('/posters/<int:id>/del')
def poster_delete(id):
    product = Product.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/posters')
    except:
        return "Произошла ошибка при удалении объявления"


@app.route('/posters/<int:id>/up', methods=['POST', 'GET'])
def post_update(id):
    product = Product.query.get(id)
    if request.method == "POST":
        product.title = request.form['title']
        product.dis = request.form['dis']
        product.price = request.form['price']

        try:
            db.session.commit()
            return redirect('/posters')

        except:
            return "Произошла ошибка при редактировании"
    else:

        return render_template("post_update.html", product=product)


@app.route('/create_product', methods=['POST', 'GET'])
def create_product():
    if request.method == "POST":
        title = request.form['title']
        dis = request.form['dis']
        price = request.form['price']

        product = Product(title=title, dis=dis, price=price)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/posters')

        except:
            return "Произошла ошибка "
    else:

        return render_template("create_product.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
