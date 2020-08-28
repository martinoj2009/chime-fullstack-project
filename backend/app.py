import sqlalchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc
import traceback

# import db & models
from models import db, menu_item, tag

app = Flask(__name__.split('.')[0])
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///menu.db"
db.init_app(app)


@app.route("/api/v1/get/item", methods=["GET"])
def getMenuItem():
    menuid = request.headers.get('id')

    if menuid is None:
        return jsonify({
            "message": "You must provide an id in the header"
        }), 400

    result = db.session.query(menu_item).filter(menu_item.id == menuid)

    return {
               "results": [(dict(row.items())) for row in result]
           }, 200


@app.route("/api/v1/get/items", methods=["GET"])
def getMenuItems():
    results = menu_item.query.limit(100).all()
    items = []
    for item in results:
        items.append({'name': item.name, 'id': item.id, 'description': item.description, 'price': item.price})
    return jsonify({
        "results": items
    }), 200


@app.route("/api/v1/add/item", methods=["POST"])
def addMenuItem():
    item_name = request.headers.get("name")
    item_tag = request.headers.get('tag')
    desc = request.headers.get("description")
    price = request.headers.get("price")

    print("Adding menu item: {0}. Tag: {1}".format(item_name, item_tag))

    # User must at least provide a name for the item
    if item_name is None:
        return {
            "message": "You must provide at least a name"
        }, 400

    try:
        new_item = menu_item(name=item_name, tag=item_tag, description=desc, price=price)
        db.session.add(new_item)
        db.session.commit()
    except:
        traceback.print_exc()
        return jsonify({
            "Message": "There was an error adding in the new item"
        }), 500

    # Should confirm the db commit returned back 1 row change
    return {
               "results": "okay"
           }, 200


@app.route("/api/v1/del/item", methods=["DELETE"])
def deleteMenuItem():
    menuid = request.headers.get('id')

    if menuid is None:
        return jsonify({
            "message": "You must provide an id in the header"
        }), 400

    try:
        db.session.query(menu_item).filter(menu_item.id == menuid).delete()
        db.session.commit()
    except:
        traceback.print_exc()
        return {
            "message": "Was not able to delete the requested id"
        }, 500

    return {
               "results": "{0} deleted".format(menuid)
           }, 200

# TAGS
@app.route("/api/v1/get/tag", methods=["GET"])
def getTag():
    menuid = request.headers.get('id')

    if menuid is None:
        return jsonify({
            "message": "You must provide an id in the header"
        }), 400

    results = tag.query.limit(100).all()
    items = []
    for item in results:
        items.append({'name': item.name, 'id': item.id})

    return jsonify({
        "results": items
    }), 200


@app.route("/api/v1/get/tags", methods=["GET"])
def getTags():
    results = tag.query.limit(100).all()
    items = []
    for item in results:
        items.append({'name': item.name, 'id': item.id})
    return jsonify({
        "results": items
    }), 200


@app.route("/api/v1/add/tag", methods=["POST"])
def addTag():
    name = request.headers.get("name")
    print("Adding tag: {0}".format(name))

    if name is None:
        return jsonify({
            "message": "You must provide a name"
        }), 400

    try:
        new_item = tag(name=name)
        db.session.add(new_item)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        traceback.print_exc()
        return jsonify({
            "message": "The requested tag already exists"
        }), 200
    except:
        traceback.print_exc()
        return jsonify({
            "message": "Unknown error has occured."
        }), 500

    # Should confirm the db commit returned back 1 row change
    return {
               "results": "tag added"
           }, 200


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
