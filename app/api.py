#import Flask, SQLAlchemy
from flask import Flask, sessions, jsonify, request, abort, json
from flask_sqlalchemy import SQLAlchemy
from .config import app_config
import bcrypt


#create SQLAlchemy OBJ
db = SQLAlchemy()

#gets a configuration obj (class in ./config.py file)
def create_app(config_name):
    from .models import User, Bucketlist, Activities

    """ creates a new Flask object """
    app = Flask(__name__, instance_relative_config=True)
    #add configurations from config file
    app.config.from_object(app_config[config_name])
    #app.config.from_pyfile('config.py')
    #connect instane to db
    db.init_app(app)

    global_user_id = None

    def login_required(global_uid, id, activity):
        if global_uid == None and activity == 'loging_in':
            global_uid = id
        elif global_uid == None and activity != 'loging_in':
            return jsonify(({'Error': "Access denied"}), 401)

    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        if request.method == 'POST':
            data = request.get_json()
            title = data['title']
            description = data['description']
            
            if title and description:
                bl = Bucketlist.query.filter_by(title = title).first()
                if bl:
                    return jsonify(({"Unsuccessful": "You already have a bucketlist with that name"}), 409)

                bucketlist = Bucketlist(title=title, description=description, user_id=9)
                db.session.add(bucketlist)
                db.session.commit()
                # response = jsonify({'id': bl.id, 'title': bl.title})
                return jsonify(({'title' : title, 'success': 'You have created a new bucket list'}), 201)

        else:
            bl = Bucketlist.get_all()
            results = []
            for bucketlist in bl:
                result_obj = {'id': bucketlist.id, 'name': bucketlist.title, 'description': bucketlist.description}
                results.append(result_obj)
            response = jsonify(results)
            # response = json.loads(response.decode('utf-8'))
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:bid>/', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_updates(bid, **kwargs):
        '''b '''
        bucketlist = Bucketlist.query.filter_by(id=bid).first()
        if not bucketlist:
            return jsonify(({"Error": "Bucketlist id {} not found".format(bid)}), 404)

        data = request.get_json()

        if request.method == 'DELETE':
            bucketlist.delete(bid)
            return jsonify({"message": "bucketlist {} deleted successfully".format(bucketlist.id)}, 200)
        
        elif request.method == 'PUT':
            if data['title'] or data['description']:
                #update the bucketlist item here
                #check if db items are equal to passed parameters
                if not data['title'] == bucketlist.title or not data['description'] == bucketlist.description:
                    updated = bucketlist.update(data['title'], data['description'])
                    if updated:
                        response=jsonify({'id': bucketlist.id, 'title': bucketlist.title})
                        response.status_code = 200
                    else:
                        response = "Update failed"
                    return response
                else:
                    return "Parameters passed equal to database value, update failed"
            return jsonify(({"Warning": "No updates passed, pass change parameters"}))
            
        elif request.method=='GET':
            return jsonify(({"Success": "Bucketlist {} retrieved successfully".format(bucketlist.title), 
                "Title": bucketlist.title, "Description": bucketlist.description}), 200)
        else:
            return jsonify(({"Error": "Invalid request"}), 403) 

    @app.route('/auth/register/', methods=['POST'])
    def register():
        data = request.get_json()
        email = data['email']
        name = data['name']
        password = data['password']
        confirm_password = data['confirm_password']
        # response = ""
        if not email:
            return jsonify(({'Error': "enter email\n"}), 409)
        if not name:
            return jsonify(({'Error': "enter name\n"}), 409)
        if not password:
            return jsonify(({'Error': "enter password\n"}), 409)
        if not confirm_password:
            return jsonify(({'Error': "enter confirm_password"}), 409)
        if password != confirm_password:
            return jsonify(({'Error': "password and confirm password don't match"}), 409)
        user_found = User.query.filter_by(email = email).first()
        if user_found:
            return jsonify(({'Error': "Email {} already exists".format(email)}), 409)
        user = User(name, email, password)
        # pw_bytes = password.encode('utf-8')
        # password_hash = user.password_hashing(pw_bytes)
        user = User(name=name, email=email, password_hash=password)
        db.session.add(user)
        db.session.commit()
        # response = jsonify({'id': bl.id, 'title': bl.title})
        return jsonify(({'username' : email, 'message': 'User created successfully'}), 201)

    @app.route("/auth/login/", methods=['POST'])
    def login():
        data = request.get_json()
        email = data['email']
        password = data['password']
        name = ""
        if not email:
            return jsonify(({'Error': "Email field should not be empty!"}), 409)
        if not password:
            return jsonify(({'Error': "Password field should not be empty!"}), 409)
        #user = User(name, email, password)
        user_found = User.query.filter_by(email=email).first()
        if user_found:
            # password_hash = user_found['password']
            if password == user_found.password_hash:
            # if bcrypt.hashpw(password, password_hash) == password_hash:
            # if user.verify_password(password, user_found['password']):
                return jsonify(({'Success': "Login successful"}), 200)
        else:
            return jsonify(({"Unsuccessful": "Wrong username password combination"}), 404)

    @app.route("/auth/logout/", methods=['POST'])
    def logout():
        '''reset session '''
        active = True
        if active:
            return jsonify(({"Success": "Logout successfull. Good-bye!"}), 200)
    
    @app.route("/bucketlists/<int:bid>/items/", methods=['POST', 'GET'])
    def items(bid):
        ''' Houses create and list items under a specific bucketlist'''
        bucketlist = Bucketlist.query.filter_by(id=bid).first()
        if not bucketlist:
            return jsonify(({"Error": "Bucketlist id {} not found".format(bid)}), 404)
        else:
            ''' if bucketlist found '''
            data = request.get_json()
            if request.method == 'POST':
                ''' add item to bucketlist '''
                item_title = data['item']
                description = data['item_description']
                if item_title and description:
                    item = Activities.query.filter_by(title=item_title, bucketlist_id=bid).first()
                    if item:
                        return jsonify(({"Unsuccessful": "You already have a bucketlist item with that name"}), 409)
                    item = Activities(title=item_title, description=description, bucketlist_id=bid)
                    db.session.add(item)
                    db.session.commit()
                    # response = jsonify({'id': bl.id, 'title': bl.title})
                    return jsonify(({'title' : item_title, 'success': 'You have added {} to {}'.format(item_title, bucketlist.title)}), 201)
                else:
                    return jsonify(({"Error": "Empty item parameter(s) passed"}))
            elif request.method == 'GET':
                ''' get all items in bucketlist with the id passed to it'''
                items = Bucketlist.get_all()
                results = []
                for item in items:
                    result_obj = {'id': item.id, 'name': item.title, 'description': item.description}
                    results.append(result_obj)
                response = jsonify(results)
                response = json.loads(response.decode('utf-8'))
                response.status_code = 200
                return response
        # else:
        #     return (({"Alert":"No items found for bucketlist id {}".format(bid)}), 404)
    
    @app.route('/bucketlists/<int:bid>/items/<int:item_id>/', methods=['GET', 'PUT', 'DELETE'])
    def activity_updates(bid, item_id, **kwargs):
        ''' handles update, delete and get item using item id '''
        #check if bucketlist exists (its id is passed on the request)
        bucketlist = Bucketlist.query.filter_by(id=bid).first()
        if not bucketlist:
            return jsonify(({"Error": "Bucketlist id {} not found".format(bid)}), 404)

        #get data passed together with the request
        data = request.get_json()
        #check if item, given via item id exists
        activity = Activities.query.filter_by(id=item_id).first()
        if request.method == 'DELETE':
            activity.delete(item_id)
            return jsonify({"message": "item {} deleted successfully".format(activity.title)}, 200)
        
        elif request.method == 'PUT':
            if data['item'] or data['item_description']:
                #update the bucketlist item here
                #check if db items are equal to passed parameters
                if data['item'] != activity.title or data['description'] != bucketlist.description:
                    item = activity.update(data['item'], data['item_description'])
                    response=jsonify({'success':"Edited item to {} successfully".format(data['item']), 'id': item.id, 'title': item.title})
                    response.status_code = 200
                    return response
                else:
                    return jsonify(({'Alert':"Parameters passed equal to database value, update failed"}), 200)
            return jsonify(({"Warning": "No updates passed, pass change parameters"}), 200)
            
        # elif request.method == 'GET':
        else:
            return jsonify(({"Success": "Item {} retrieved successfully".format(activity.title), 
                "Title": activity.title, "Description": activity.description}), 200)
        # else:
        #     return jsonify(({"Error": "Invalid request"}), 403) 
        
    return app