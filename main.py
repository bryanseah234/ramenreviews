import csv
import json
from flask import Flask,render_template,request,redirect,url_for
from flask_restful import Api,Resource,reqparse
from functions import createone,insertall,insertone,searchsome,searchsome,searchsome,updatesome,deleteall,deletesome,selectall


app = Flask(__name__)
api = Api(app)
DATABASE = 'ratings'
CSV = 'ratings'
TABLE = 'Ratings'
#--------------------------------------------------------------------------------
class CreateOne(Resource):
  def get(self):
    status = createone(DATABASE, TABLE)
    if status == False:
      return 'Database and table not created.', 404
    else:
      return 'Database and table created.', 201
#--------------------------------------------------------------------------------
class AddOne(Resource):
  def put(self):
    args = request.form
    for key, value in args.items():
      if value is None:
          del args[key]
    insertone(DATABASE, TABLE, args)
    return 'Added one ramen review to database.', 201
#--------------------------------------------------------------------------------
class AddMany(Resource):
  def get(self):
    status = insertall(DATABASE, CSV)
    if status == False:
      return 'Not all ramen reviews from csv added.', 404
    else:
      return 'Added all ramen reviews from csv to database.', 201
#--------------------------------------------------------------------------------
class EditSome(Resource):
  def put(self):
    args = request.form
    for key, value in args.items():
      if value is None:
          del args[key]
    status = updatesome(DATABASE, TABLE, args)
    if status == False:
      return 'Ramen reviews not edited. Check post params again.', 404
    else:
      return 'Edited some ramen reviews.', 200
#--------------------------------------------------------------------------------
class DeleteSome(Resource):
  def put(self):
    args = request.form
    for key, value in args.items():
      if value is None:
          del args[key]
    status = deletesome(DATABASE, TABLE, args)
    if status == False:
      return 'No ramen reviews deleted. Check post params again.', 404
    else:
      return 'Deleted some ramen reviews.', 200
#--------------------------------------------------------------------------------
class DeleteAll(Resource):
  def get(self):
    try:
      deleteall(DATABASE, TABLE)
    except Exception as e:
      print(e)
    return 'Deleted all ramen reviews.', 200
#--------------------------------------------------------------------------------
class SearchSome(Resource):
  def put(self):
    args = request.form
    for key, value in args.items():
      if value is None:
          del args[key]
    results = searchsome(DATABASE, TABLE, args)
    if results == False:
      return 'No ramen reviews found. Check post params again.', 404
    else:
      j = json.dumps(results, indent=2)
      print(f'Searched for ramen reviews. Results are {j}')
      return j, 200
#--------------------------------------------------------------------------------
class SelectAll(Resource):
  def get(self):
    try:
      results = selectall(DATABASE, TABLE)
      j = json.dumps(results, indent=2)
      print(f'Selected all ramen reviews. Results are {j}')
      return j, 200
    except Exception as e:
      print(e)
      return 'Something went wrong, please try again.', 404
#--------------------------------------------------------------------------------
api.add_resource(CreateOne, '/api/createone') #no need args (get)
api.add_resource(SearchSome, '/api/searchsome')
api.add_resource(DeleteAll, '/api/deleteall') #no need args (get)
api.add_resource(DeleteSome, '/api/deletesome')
api.add_resource(EditSome, '/api/editsome')
api.add_resource(AddMany, '/api/addmany') #no need args (get)
api.add_resource(AddOne, '/api/addone')
api.add_resource(SelectAll, '/api/selectall') #no need args (get)
#--------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/documentation', methods=['GET'])
def docs():
    return render_template('documentation.html')


@app.route('/help', methods=['GET','POST'])
def help():
    return render_template('help.html')

@app.route('/display', methods=['GET'])
def display():
    data = selectall(DATABASE, TABLE)
    return render_template('display.html', data=data)    


if __name__ == '__main__':
    app.run(debug=False)
