#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import abort
import weather_class as weather
import json


app = Flask(__name__)


predictions = []
predictions_objects = []


@app.route('/')
def get_home():
    return jsonify({'status': 'OK'})
    # return jsonify({'status': "OK"})
# Fist we are going to do a simple get.

# we now have a get_predictions function that is associated with the
# /todo/api/v1.0/predictions  URI, and only for the GET HTTP method

# ------------------------------------------------------------------------------

# Now let's write the second version of the GET method for our predictions resource.
# If you look at the table above this will be the one that is used to return the
# data of a single prediction:
@app.route('/predictions/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    if request.method == 'GET':
        prediction = [prediction for prediction in predictions if prediction['ID'] == prediction_id]
        if len(prediction) == 0:
            return jsonify({'error': 'Nonexistent resource'})

        return jsonify(predictions[prediction_id-1])


# ------------------------------------------------------------------------------

def get_predictions():
    return jsonify({'predictions': predictions})

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
    #....
    # If we detect we want to do a PUT of a new prediction ...
    elif request.method == 'PUT':
        # Create an object from class Prediction with the information inserted
        # in the curl
        prediction = weather.Prediction(request.json['city'],request.json['temperature'] )

        # We need to add the object as a dict, for an easily convertion to json
        predictions.append(prediction.__dict__)
        predictions_objects.append(prediction)

        # print(prediction)
        return jsonify(prediction.__dict__)
        # return jsonify({'prediction': prediction.__dict__}),200

    # --------------------------------------------------------------------------
    elif request.method == 'POST':
        id = request.json['ID']
        city = request.json['city']
        temperature = request.json['temperature']

        # Search for the prediction with the ID introduced
        pos = -1
        for i, pred in enumerate(predictions):
            if pred['ID'] == id:
                pos = i
                predictions_objects[pos].set_city(city)
                predictions_objects[pos].set_temperature(temperature)

                # predictions[i]['city'] = city
                # predictions[i]['temperature'] = temperature

        # We have to be sure of have send an ID existent. In other case, we
        # abort to notificate the problem

        # We abort this instruction and we send the error to the function
        # called  "not found ". In that case, the response is OK, because
        # the resource doesnt exists, but the request was correct
        if pos == -1:
            return jsonify({'predictions': predictions}),200

        return jsonify({'prediction': predictions[pos]}),201

        # return jsonify({'prediction': predictions[pos]})


    elif request.method == 'DELETE':
        # Search for the prediction with the ID introduced
        id = request.json['ID']
        pos = -1
        for i, pred in enumerate(predictions):
            if pred['ID'] == id:
                pos = i
        # We have to be sure of have send an ID existent. In other case, we
        # abort to notificate the problem. If the resource doesnt exists, we
        # send  an OK response, because its problem from the HITO
            pass
        if pos == -1:
            return jsonify({'predictions': predictions})

        del predictions[pos]
        del predictions_objects[pos]

        return jsonify({'predictions': predictions})



# ------------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True) # pragma: no cover
