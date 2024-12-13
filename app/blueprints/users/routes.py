from flask import request, jsonify
from app.blueprints.users import users_bp
from marshmallow import ValidationError
from app.models import User, db
from sqlalchemy import select
from app.blueprints.users.schemas import user_schema, users_schema
from werkzeug.security import check_password_hash
from app.models import User
from werkzeug.security import generate_password_hash



#===== Routes

@users_bp.route("/", methods=['POST'])
def create_user():
    try:
        # Validate and deserialize input data
        user_data = user_schema.load(request.json)

        # Hash the password before saving
        # password_hash = generate_password_hash(user_data['password'])

        # Create a new User instance with hashed password
        new_user = User(
    firstname=user_data['firstname'],
    lastname=user_data['lastname'],
    email=user_data['email'],
    password_hash=user_data['password_hash'],  # Store the hashed password
    rating=user_data.get('rating', 0)
)

        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user), 201

    except ValidationError as e:
        # Return validation error messages
        return jsonify({"errors": e.messages}), 400
    except Exception as e:
        # Catch other exceptions
        return jsonify({"error": str(e)}), 500

@users_bp.route("/", methods=["GET"])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()

    return users_schema.jsonify(users), 200

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.session.get(User, user_id)

    return user_schema.jsonify(user), 200

@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.get(User, user_id)

    if user == None:
        return jsonify({"message": "invalid id"}), 400
    
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in user_data.items():
        setattr(user, field, value)

    db.session.commit()
    return user_schema.jsonify(user), 200

@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.session.get(User, user_id)

    if user == None:
        return jsonify({'messge': 'invalid id'}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f"deleted user {user_id}!"})

@users_bp.route("/login", methods=["POST"])
def login():
    try:
        # Get login data from request
        login_data = request.json
        email = login_data.get('email')
        password = login_data.get('password_hash')

        # Check if email and password are provided
        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        # Query the database for the user with the given email
        user = User.query.filter_by(email=email).first()

        # Check if user exists
        if not user:
            return jsonify({"error": "User not found."}), 404

        # Check if the provided password matches the hashed password
        if not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid password."}), 401

        # Return a success message (you can also generate and return a JWT token here)
        return jsonify({"message": "Login successful", "user": user_schema.dump(user)}), 200

    except Exception as e:
        # Catch other exceptions and return an error
        return jsonify({"error": str(e)}), 500