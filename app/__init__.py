# #import Flask, SQLAlchemy
# from flask import Flask, sessions, jsonify, request, abort, json
# from flask_sqlalchemy import SQLAlchemy
# from .config import app_config

# #create SQLAlchemy OBJ
# db = SQLAlchemy()

# #gets a configuration obj (class in ./config.py file)
# def create_app(config_name):
#     from .models import User, Bucketlist, Activities

#     """ creates a new Flask object """
#     app = Flask(__name__, instance_relative_config=True)
#     #add configurations from config file
#     app.config.from_object(app_config[config_name])
#     #app.config.from_pyfile('config.py')
#     #connect instane to db
#     db.init_app(app)

#     @app.route('/bucketlists/', methods=['POST', 'GET'])
#     def bucketlists():
#         if request.method == 'POST':
#             data = request.get_json()
#             title = data['title']
#             description = data['description']
#             # userid = sessions['user']and userid
#             if title and description:
#                 user_id = 1
#                 id = 1
#                 # get by value
# # bd = Bucketlist.query.filter_by(id=value, user_id=curr_user)
# # .....first()login verification
# # get all
# # bd = Bucketlist.query.filter_by(id).all

# # delete 


# # update
# # bd = Bucketlist.query.filter_by(id=value, user_id=curr_user)
# # obj.title
# # obj.session.commit()
# # insert
#                 bl = Bucketlist.query.filter_by(title = title).first()
#                 if bl:
#                     return "You already have a bucketlist with that name", 409

#                 bucketlist = Bucketlist(id=id, title=title, description=description, user_id=user_id)
#                 db.session.add(bucketlist)
#                 db.commit()
#                 # response = jsonify({'id': bl.id, 'title': bl.title})
#                 return ({'title' : title, 'message': 'You have created a new bucket list'}), 201

#         else:
#             bl = Bucketlist.get_all()
#             results = []
#             for bucketlist in bl:
#                 result_obj = {'id': bl.id, 'name': bl.title, 'description': bl.description}
#                 results.append(result_obj)
#             response = jsonify(results)
#             response = json.loads(response.decode('utf-8'))
#             response.status_code = 200
#             return response

#     @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
#     def bucketlist_updates(id, **kwargs):
#         '''b '''
#         bucketlist = Bucketlist.query.filter_by(id=id).first()
#         if not bucketlist:
#             abort(404)
        
#         if request.method == 'DELETE':
#             bucketlist.delete()
#             return {"message": "bucketlist {} deleted successfully".format(bucketlist.id)}, 200
        
#         elif request.method == 'PUT':
#             title = str(request.data.get('name', ''))
#             bucketlist.title = title
#             bucketlist.save()
#             response=jsonify({'id': bucketlist.id, 'title': bucketlist.title})
#             response.status_code = 200
#             return response

#     return app