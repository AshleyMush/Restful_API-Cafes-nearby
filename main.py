from flask import Flask, jsonify, render_template, request
from models import db, Cafe
import random

from sqlalchemy import Integer, String, Boolean



app = Flask(__name__)


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db.init_app(app)




# used to create the database file
# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    return render_template("index.html")





# HTTP POST - Create Record


# --------------------------------------------- HTTP GET - (Read) Record
# Read a Random Record from the Database
@app.route("/random")
def get_random_cafe():

    all_cafes = Cafe.query.all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })


# Read all Records from the Database
@app.route("/all")
def get_all_cafes():
    all_cafes = Cafe.query.all()
    return jsonify(cafes =[cafe.to_dict() for cafe in all_cafes])

"""
List Comprehension: 

for cafe in get_all_cafes:
    cafe.to_dict()
    return jsonify(cafes=[cafe.to_dict()]

"""


# Read a Record by ID from the Database
@app.route("/search")
def get_cafe_by_location():
    query_location = request.args.get("loc")
    cafes_at_location = Cafe.query.filter_by(location=query_location).all()

    if cafes_at_location:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes_at_location])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404
                            #  Key       : Value


@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name = request.form.get("name"),
        map_url = request.form.get("map_url"),
        img_url = request.form.get("img_url"),
        location = request.form.get("location"),
        seats = request.form.get("seats"),
        coffee_price = request.form.get("coffee_price"),
        has_sockets = int(request.form.get("has_sockets")),
        has_wifi = int(request.form.get("has_wifi")),
        has_toilet = int(request.form.get("has_toilet")),
        can_take_calls = int(request.form.get("can_take_calls"))
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response = {"Success":"Successfully added new cafe"})













# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
