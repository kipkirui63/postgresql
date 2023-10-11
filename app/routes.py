from app import app, db
from flask import request, jsonify , make_response
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError



from app.models import User




api = Api(app)
app.config['JWT_SECRET_KEY'] = 'gwklgn4gn42gmrmkrg'
jwt = JWTManager(app)



class UserRegistrationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first() is not None:
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=args['email']).first() is not None:
            return {'message': 'Email already exists'}, 400
        

                # Create a new User instance and add it to the database
        new_user = User(
            username=args['username'],
            email=args['email'],
            password=args['password'],
        )
        db.session.add(new_user)
        db.session.commit()

        # Generate an access token for the newly registered user
        access_token = create_access_token(identity=new_user.id)

        return {
            'message': 'User registered successfully',
            'access_token': access_token
        }, 201


class UserLoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()

        if user and user.password == args['password']:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            return user.as_dict()
        except NoAuthorizationError:
            response = jsonify({'message': 'Missing or invalid Authorization header'})
            response.status_code = 401  # Unauthorized status code
            return response

    @jwt_required()
    def put(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('email', type=str)
            parser.add_argument('phonenumber', type=int)
            args = parser.parse_args()

            for key, value in args.items():
                if value is not None:
                    setattr(user, key, value)

            db.session.commit()
            return {'message': 'User updated successfully'}
        except NoAuthorizationError:
            response = jsonify({'message': 'Missing or invalid Authorization header'})
            response.status_code = 401  # Unauthorized status code
            return response

    @jwt_required()
    def delete(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        except NoAuthorizationError:
            response = jsonify({'message': 'Missing or invalid Authorization header'})
            response.status_code = 401  # Unauthorized status code
            return response


api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(UserRegistrationResource, '/register')
api.add_resource(UserLoginResource, '/login')
