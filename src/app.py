import os
from flask import Flask, request, jsonify, url_for
from sqlalchemy import select
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Characters, Planets, Vehicles, User, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#endpoint para obtener todos los usuarios
@app.route('/user', methods=['GET'])
def get_all_users():
    data = db.session.scalars(select(User)).all()
    if not data:  
        return jsonify({"error": "No users found"}), 404
    results = list(map(lambda item: item.serialize(), data))
    response_body = {
        "results":results
    }
    return jsonify(response_body), 200

#endpoint para obtener todos los personajes
@app.route('/character', methods=['GET'])
def get_all_characters():
    data = db.session.scalars(select(Characters)).all()
    if not data:  
        return jsonify({"error": "No characters found"}), 404
    results = list(map(lambda item: item.serialize(), data))
    response_body = {
        "results":results
    }
    return jsonify(response_body), 200

#endpoint para obtener todos los planetas
@app.route('/planet', methods=['GET'])
def get_all_planets():
    data = db.session.scalars(select(Planets)).all()
    if not data:  
        return jsonify({"error": "No planets found"}), 404
    results = list(map(lambda item: item.serialize(), data))
    response_body = {
        "results":results
    }
    return jsonify(response_body), 200

#endpoint para obtener todos los vehiculos
@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    data = db.session.scalars(select(Vehicles)).all()
    if not data:  
        return jsonify({"error": "No vehicles found"}), 404
    results = list(map(lambda item: item.serialize(), data))
    response_body = {
        "results":results
    }
    return jsonify(response_body), 200

#endpoint para obtener un solo usuario
@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    try:
        user = db.session.execute(select(User).filter_by(id=id)).scalar_one()
        response_body = {
            "result": user.serialize()
        }
        return jsonify(response_body), 200
    except:
        return jsonify({"msg": "user does not exist"}), 404

#endpoint para obtener un solo personaje
@app.route('/character/<int:id>', methods=['GET'])
def get_single_character(id):
    try:
        user = db.session.execute(select(Characters).filter_by(id=id)).scalar_one()
        response_body = {
            "result": user.serialize()
        }
        return jsonify(response_body), 200
    except:
        return jsonify({"msg": "character does not exist"}), 404

#endpoint para obtener un solo planeta
@app.route('/planet/<int:id>', methods=['GET'])
def get_single_planet(id):
    try:
        user = db.session.execute(select(Planets).filter_by(id=id)).scalar_one()
        response_body = {
            "result": user.serialize()
        }
        return jsonify(response_body), 200
    except:
        return jsonify({"msg": "planet does not exist"}), 404

#endpoint para obtener un solo vehiculo
@app.route('/vehicle/<int:id>', methods=['GET'])
def get_single_vehicle(id):
    try:
        user = db.session.execute(select(Vehicles).filter_by(id=id)).scalar_one()
        response_body = {
            "result": user.serialize()
        }
        return jsonify(response_body), 200
    except:
        return jsonify({"msg": "vehicle does not exist"}), 404

#endpoint para agregar un user
@app.route('/user', methods=['POST'])
def create_user():
    request_data = request.json
    if "email" not in request_data or "password" not in request_data:
        return jsonify({"error": "Email and password are required"}), 400   
    existing_user = User.query.filter_by(email=request_data["email"]).first()
    if existing_user:
        return jsonify({"error": "Email is already registered"}), 400   
    user = User(email=request_data["email"], password=request_data["password"])
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": f"user with ID {user.id} created"
    }
    return jsonify(response_body), 200

#endpoint para agregar un character
@app.route('/character', methods=['POST'])
def create_character():
    request_data = request.json
    existing_character = Characters.query.filter_by(name=request_data["name"]).first()
    if existing_character:
            return jsonify({"error": "Character with this name already exists"}), 400
    user = Characters(name=request_data["name"], birth_year=request_data["birth_year"], height=request_data["height"], skin_color=request_data["skin_color"], eye_color=request_data["eye_color"])
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": f"character with ID {user.id} created"
    }
    return jsonify(response_body), 200

#endpoint para agregar un planeta
@app.route('/planet', methods=['POST'])
def create_planet():
    request_data = request.json
    existing_character = Planets.query.filter_by(name=request_data["name"]).first()
    if existing_character:
            return jsonify({"error": "Planet with this name already exists"}), 400
    user = Planets(name=request_data["name"], climate=request_data["climate"], diameter=request_data["diameter"], population=request_data["population"], terrain=request_data["terrain"])
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": f"planet with ID {user.id} created"
    }
    return jsonify(response_body), 200

#endpoint para agregar un vehiculo
@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    request_data = request.json
    existing_vehicle = Vehicles.query.filter_by(name=request_data["name"]).first()
    if existing_vehicle:
            return jsonify({"error": "Vehicle with this name already exists"}), 400
    user = Vehicles(name=request_data["name"], model=request_data["model"], cargo_capacity=request_data["cargo_capacity"], length=request_data["length"], passengers=request_data["passengers"])
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": f"vehicle with ID {user.id} created"
    }
    return jsonify(response_body), 200

#endpoint para borrar un usuario
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()
        if not user:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        response_body = {
            "msg": f"User {user.email} with ID {user.id} was deleted, along with their favorites."
        }
        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#endpoint para borrar un personaje
@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    user = db.session.execute(db.select(Characters).filter_by(id=id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "Character not found"}), 404
    db.session.delete(user)
    db.session.commit()
    response_body = {
        "msg":f"character with {user.id}, named {user.name} deleted"
    }
    return jsonify(response_body), 200

#endpoint para borrar un planeta
@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    user = db.session.execute(db.select(Planets).filter_by(id=id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "Planet not found"}), 404
    db.session.delete(user)
    db.session.commit()
    response_body = {
        "msg":f"Planet with {user.id}, named {user.name} deleted"
    }
    return jsonify(response_body), 200

#endpoint para borrar un vehiculo
@app.route('/vehicle/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    user = db.session.execute(db.select(Vehicles).filter_by(id=id)).scalar_one_or_none()
    if not user:
        return jsonify({"error": "Vehicle not found"}), 404
    db.session.delete(user)
    db.session.commit()
    response_body = {
        "msg":f"Vehicle with {user.id}, named {user.name} deleted"
    }
    return jsonify(response_body), 200

#endpoint para obtener todos los favoritos de un usuario
@app.route('/user/<int:user_id>/favorite', methods=['GET'])
def get_user_favorites(user_id):
    try:
        favorite_planets = db.session.scalars(select(Favorites).filter_by(user_id=user_id)).all()
        favorite_characters = db.session.scalars(select(Favorites).filter_by(user_id=user_id)).all()
        response_body = {
            "favorite_planets": [favorite.serialize() for favorite in favorite_planets],
            "favorite_characters": [favorite.serialize() for favorite in favorite_characters]
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# endpoint para agregar un personaje a favoritos
@app.route('/favorite/character', methods=['POST'])
def add_favorite_character():
    request_data = request.json
    user_id = request_data.get('user_id')
    character_id = request_data.get('character_id')

    if not user_id or not character_id:
        return jsonify({"error": "user_id and character_id are required"}), 400

    try:
        character = db.session.execute(select(Characters).filter_by(id=character_id)).scalar_one_or_none()
        if not character:
            return jsonify({"error": f"Character with ID {character_id} not found."}), 404
        existing_favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, character_id=character_id)).scalar_one_or_none()
        if existing_favorite:
            return jsonify({"error": "This character is already in your favorites."}), 400

        # Añadir el personaje a los favoritos
        new_favorite = Favorites(user_id=user_id, character_id=character_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"msg": f"Character {character_id} added to user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# endpoint para eliminar un personaje de favoritos
@app.route('/favorite/character', methods=['DELETE'])
def delete_favorite_character():
    request_data = request.json
    user_id = request_data.get('user_id')
    character_id = request_data.get('character_id')

    if not user_id or not character_id:
        return jsonify({"error": "user_id and character_id are required"}), 400

    try:
        # Verificar si el personaje está en los favoritos
        favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, character_id=character_id)).scalar_one_or_none()
        if not favorite:
            return jsonify({"error": "Character not found in your favorites."}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": f"Character {character_id} removed from user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# endpoint para agregar un planeta a favoritos
@app.route('/favorite/planet', methods=['POST'])
def add_favorite_planet():
    request_data = request.json
    user_id = request_data.get('user_id')
    planet_id = request_data.get('planet_id')

    if not user_id or not planet_id:
        return jsonify({"error": "user_id and planet_id are required"}), 400

    try:
        # Verificar si el planeta ya está en los favoritos
        existing_favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, planet_id=planet_id)).scalar_one_or_none()
        if existing_favorite:
            return jsonify({"error": "This planet is already in your favorites."}), 400

        # Añadir el planeta a los favoritos
        new_favorite = Favorites(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"msg": f"Planet {planet_id} added to user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# endpoint para eliminar un planeta de favoritos
@app.route('/favorite/planet', methods=['DELETE'])
def delete_favorite_planet():
    request_data = request.json
    user_id = request_data.get('user_id')
    planet_id = request_data.get('planet_id')

    if not user_id or not planet_id:
        return jsonify({"error": "user_id and planet_id are required"}), 400

    try:
        # Verificar si el planeta está en los favoritos
        favorite = db.session.execute(select(Favorites).filter_by(user_id=user_id, planet_id=planet_id)).scalar_one_or_none()
        if not favorite:
            return jsonify({"error": "Planet not found in your favorites."}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": f"Planet {planet_id} removed from user {user_id}'s favorites."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
