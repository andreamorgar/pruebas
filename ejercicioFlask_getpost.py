#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import abort
import weather_class as weather
import json
import os
from predictionDB import getDocument, pushDocument, updateDocument
from predictionDB import get_all_predictions, delete_document

app = Flask(__name__)




@app.route('/')
def get_home():
    return jsonify({'status': 'OK'})

# ------------------------------------------------------------------------------

# Now let's write the second version of the GET method for our predictions resource.
# If you look at the table above this will be the one that is used to return the
# data of a single prediction:
@app.route('/predictions/<int:prediction_id>', methods=['GET']) #funciona
def get_prediction(prediction_id):
    if request.method == 'GET':
        # We want to find in the collection the document with the ID equal to

        result = getDocument(prediction_id)
        if result is None:
            abort(404)

        # dict_result= result.__getitem__(0)
        result.pop('_id')
        # print(result)

        return jsonify(result)
# ------------------------------------------------------------------------------

def get_predictions(): # funciona
    cursor = get_all_predictions()
    actual_list_of_preds = []

    for document in cursor:
        next_dict = document
        next_dict.pop('_id')
        actual_list_of_preds.append(next_dict)
        # print(next_dict)

    return jsonify({'predictions': actual_list_of_preds })

# ------------------------------------------------------------------------------
# Method with POST
# We are going to add a new prediction
@app.route('/predictions', methods=['GET','PUT', 'POST', 'DELETE'])
def create_prediction():
    #Depending of the especification in curl, we can do different things

    # If we detect we want to do a GET of the prediction we have registered...
    if request.method == 'GET':
        return get_predictions();
    # --------------------------------------------------------------------------

    # If we detect we want to do a PUT of a new prediction ...
    elif request.method == 'PUT':
        # Create an object from class Prediction with the information inserted
        # in the curl
        prediction = weather.Prediction(request.json['city'],request.json['temperature'] )

        # We push the new prediction to the Database
        record = {
            "ID": prediction['ID'],
            "city": prediction['city'],
            "date": prediction['date'],
            "temperature": prediction['temperature']
        }
        pushDocument(record)

        return jsonify(prediction.__dict__)

    # --------------------------------------------------------------------------
    elif request.method == 'POST': #funciona
        id = request.json['ID']
        city = request.json['city']
        temperature = request.json['temperature']

        pred = getDocument(id)
        if pred is None:
            return abort(404)

        record = {
            "city": city,
            "temperature": temperature
        }

        # dict_result= pred.__getitem__(0)
        updateDocument(pred,record)
        updated_pred = getDocument(id)
        updated_pred.pop('_id')

        return jsonify({'prediction': updated_pred}),201
        # return jsonify(updated_pred),201

    # --------------------------------------------------------------------------
    elif request.method == 'DELETE':
        # Search for the prediction with the ID introduced
        id = request.json['ID']
        not_wanted_query = getDocument(id)

        if not_wanted_query is None:
            return jsonify({'msg': "Deleted"})


        delete_document(not_wanted_query)


        return jsonify({'msg': "Deleted"})


# ------------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True) # pragma: no cover
