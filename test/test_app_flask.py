import os
import ejercicioFlask_getpost as app_weather
import weather_class
import unittest
import tempfile
import json
import datetime

from predictionDB import get_all_predictions, get_number_documents
from predictionDB import delete_all_documents

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Creamos el cliente que se va a utilizar.
        self.app = app_weather.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

        # declaro los valores que me hacen falta
        self.city = "Salamanca"
        self.temperature = "26"

        self.city2 = "Granada"
        self.temperature2 = "10"
        self.post_temperature = "45"

        # To test the database, we are going to try it with a clean
        # database
        delete_all_documents()
    # --------------------------------------------------------------------------
    def tearDown(self):
        pass

    # --------------------------------------------------------------------------
    def test_1_app_run(self):
        self.assertEqual(app_weather.app.debug, False)
        pass

    # --------------------------------------------------------------------------
    def test_2_get_home(self):
        # Hacemos una petición a la ruta inicial. Primero vamos a probar
        # metiendo la ruta de forma correcta.
        result = self.app.get('/')

        # Esta es la razón por la que hay que poner ahí una b:
        # https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal

        # ALTERNATIVAS EQUIVALENTES:
        # self.assertEqual((result.data).decode('utf-8'), 'My project page :)' )
        # self.assertEqual(result.data, b'My project page :)' )
        self.assertEqual(result.get_json(), {'status':'OK'},
         "Comprobación de quedevuelve status OK")

        # Comprobamos que el código sea 200 para garantizar que es correcto.
        self.assertEqual(result.status_code, 200, "El estado generado es 200")
        # Comprobamos el tipo del contenido al que se está haciendo get.
        self.assertEqual(result.content_type,"application/json",
         "Content-type es del tipo application/json")


        # If we do another get, we have to get the same result
        result_again = self.app.get('/')
        self.assertEqual(result.get_json(), result_again.get_json(),
        "Si volvemos a hacer un get del contenido, sigue siendo el mismo")


        pass

    # --------------------------------------------------------------------------
    def test_3_create_prediction(self):

        # 1. COMPROBACIÓN DE GET
        result = self.app.get('http://127.0.0.1:5000/predictions')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, "application/json")

        # Inicialmente la lista de predicciones está vacía. Vamos a comprobar
        # que el resultado sea el que realmente se espera.
        # text_result = result.get_data(as_text=True)

        # Compare dict to dict:
        # https://www.youtube.com/watch?v=kvux1SiRIJQ&t=217s

        cursor = get_all_predictions()
        actual_list_of_preds = []

        for document in cursor:
            next_dict = document
            next_dict.pop('_id')
            actual_list_of_preds.append(next_dict)

        self.assertEqual(result.get_json(), {'predictions':actual_list_of_preds},
        "Comprobación de que el contenido es correcto")

        # 2. Vamos a probar a meter una ruta incorrecta y ver si no funciona.
        result = self.app.get('/ruta_mala')

        # Comprobamos que el código sea 200 para garantizar que es correcto.
        self.assertEqual(result.status_code, 404)
        # Comprobamos el tipo del contenido al que se está haciendo get.
        self.assertEqual(result.content_type, "application/json", "Content-type es del tipo application/json")

        self.assertEqual(result.get_json(), {'error':'Not found'},
        "Comprobación de que el contenido es correcto" )

        pass


    def test_4_get_prediction(self):


        # Initially, there is not predictions, so the structure is empty
        result = self.app.get('/predictions/0')
        # Comprobamos que el código sea 200 para garantizar que es correcto.
        self.assertEqual(result.status_code, 404, "El estado generado es 404")
        # Comprobamos el tipo del contenido al que se está haciendo get.
        self.assertEqual(result.content_type, "application/json", "Content-type es del tipo application/json")
        self.assertEqual(result.get_json(), {'error':'Not found'},
        "Comprobación de que el contenido es correcto" )


        # We can try to access to another imaginary prediction, and again it is
        # generated an 404 error, because there is not information to show.

        # When we didnt have any Database, we didnt have persistent data. So,
        # by the time we started the service, we didnt have any prediction inside.
        # Now, with the database included, when we start the application, we
        # already have data, and we have to prove it. To test that the functionality
        # is correct with nonexistent data, we are going to try to access to a very
        # high number of id.

        # We can try to access to another imaginary prediction, and again it is
        # generated an 404 error, because there is not information to show.
        result = self.app.get('/predictions/1')

        # We have to check the status code.
        self.assertEqual(result.status_code, 404,  "El estado generado es 404")

        # We have to check if content-type is correct.
        self.assertEqual(result.content_type, "application/json", "Content-type es del tipo application/json")
        self.assertEqual(result.get_json(), {'error':'Not found'},
        "Comprobación de que el contenido es correcto" )

        # So, we have to add a prediction if we want to get results.
        # Firstly,create a dictionary called data with the values we want to put
        data = {
            "city": self.city,
            "temperature": self.temperature
        }
        datos = json.dumps(data)

        # We have to specify the headers (in other case generate an error)
        # https://stackoverflow.com/questions/41653058/flask-testing-a-put-request-with-custom-headers
        headers = {'content-type': 'application/json'}

        # At this moment, with no resources in the route, we have length 0
        # We are going to save this value, because can be intereseting to
        # prove how it increase in one point after doing a correct put (because
        # we'll have append an prediction)
        actual_len = get_number_documents()
        # We send a put with the data and headers above
        result_put = self.app.put('/predictions',
        data=datos,headers=headers)

        # We check the status. If status is 200, it's ok
        self.assertEqual(result_put.status_code, 200, "El estado generado es 200")
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_put.content_type, "application/json",
        "Content-type es del tipo application/json")
        # We check we have a new value in the vector comparting lengths
        self.assertEqual(get_number_documents(),actual_len+1)


        result = self.app.get('/predictions/1')


        # The object we have just created is saved in last one in Predictions
        # vector, so we can easily check if the information we have saved is
        # the same one we have saved before.

        cursor = get_all_predictions()
        actual_list_of_preds = []

        for document in cursor:
            next_dict = document
            next_dict.pop('_id')
            actual_list_of_preds.append(next_dict)

        self.assertEqual(result.get_json(), actual_list_of_preds[-1],
        "Comprobación de que el contenido es correcto")

        # If we try to get the content again, the result must be the same
        result_again = self.app.get('/predictions/1')
        self.assertEqual(result.get_json(), result_again.get_json(),
        "Comprobación de que el contenido es el mismo al hacer otro get")


        # Create an Prediction object
        # self.object_prediction = weather_class.Prediction(self.city, self.temperature)

        # Duda: no puedo crear un objeto para comprobar que funciona porque al
        # estar usando IDs que se asignan solos, si creo un objeto, me pondría
        # un ID más que el valor que intento comparar (me pondría ID=2 en este
        # caso).

        # That's the reason why I'll compare with a dict which has the
        # same content

        my_dict = {
            "city": self.city,
            "temperature": self.temperature,
            "ID": get_number_documents(),
            "date": datetime.datetime.now().strftime('%d-%m-%Y')
        }

        self.assertEqual(result.get_json(), my_dict,
        "Comprobación de que el contenido es correcto")

        # If we change one value, for example: ID value, we can check it
        # doesn't work:
        my_dict["ID"]=2
        self.assertNotEqual(result.get_json(), my_dict,
        "Comprobación de que el contenido es correcto de nuevo,por si acaso")


        #And now, if we create a new Prediction, its correct these dictionary.

        data2 = {
            "city": self.city2,
            "temperature": self.temperature2
        }
        datos2 = json.dumps(data2)
        result_new_put = self.app.put('/predictions',
        data=datos2,headers=headers)


        my_second_dict = {
            "city": self.city2,
            "temperature": self.temperature2,
            "ID": get_number_documents(),
            "date": datetime.datetime.now().strftime('%d-%m-%Y')
        }
        self.assertEqual(result_new_put.get_json(), my_second_dict,
        "Comprobación de que el contenido es correcto")

        # In the same way, if we get this last prediction that we have added,
        # we'll get the same content

        result = self.app.get('/predictions/' +
                str(get_number_documents()))

        cursor = get_all_predictions()
        actual_list_of_preds = []

        for document in cursor:
            next_dict = document
            next_dict.pop('_id')
            actual_list_of_preds.append(next_dict)

        self.assertEqual(result.get_json(), actual_list_of_preds[-1],
        "Comprobación de que el contenido guardado es correcto")


        # At this moment we have 2 resources, we can test it:
        self.assertEqual(get_number_documents(),2,
        "Comprobación de que el número de recursos actual es correcto")



        # POST
        post_dictionary = {
            "city": self.city2,
            "temperature": self.post_temperature,
            "ID": 2,
            "date": datetime.datetime.now().strftime('%d-%m-%Y')
        }

        result_post = self.app.post('/predictions',
        data=json.dumps(post_dictionary),headers=headers)

        # We check status, must be MODIFIED
        self.assertEqual(result_post.status_code, 201, "El estado generado es 201")
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_post.content_type, "application/json",
        "Content-type es del tipo application/json")
        self.assertEqual(result_post.get_json(),{'prediction':post_dictionary},
        "Comprobación de que el contenido es correcto")

        # Now we want to make sure that we have, in the second document of the
        # DataBase, the correct information
        self.assertEqual(get_all_predictions().__getitem__(1)["temperature"],
        post_dictionary["temperature"], "Actualizado valor en el vector de predicciones")

        #  POST TO AN UNEXISTENT RESOURCE:
        # We try to modify a resource that doesnt exist
        post_dictionary['ID']=1111
        result_post = self.app.post('/predictions',
        data=json.dumps(post_dictionary),headers=headers)

        # We check status, must be OK, because 404 because resource doesnt exist
        self.assertEqual(result_post.status_code, 404)
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_post.content_type, "application/json")


        cursor = get_all_predictions()
        actual_list_of_preds = []

        for document in cursor:
            next_dict = document
            next_dict.pop('_id')
            actual_list_of_preds.append(next_dict)

        self.assertEqual(result_post.get_json(),{'error': 'Not found'})

        #  DELETE:
        result_delete = self.app.delete('/predictions',
        data=json.dumps({'ID':1}),headers=headers)

        cursor = get_all_predictions()
        actual_list_of_preds = []

        for document in cursor:
            next_dict = document
            next_dict.pop('_id')
            actual_list_of_preds.append(next_dict)

        # After doing delete, the size of the vector should have decreased
        self.assertEqual(get_number_documents(),1,
        "Comprobación de que el número de recursos actual es correcto")

        # Now we have to prove that the content we deleted above is the right
        # one. We can check the content in the ''result'' var. This var should
        # have the content of the second dict (only)
        # Tenemos que tener una lista de diccionarios que contenga, como unico
        # diccionario ese que no hemos borrado
        self.assertEqual(result_delete.get_json(),{'msg': "Deleted"},
        "Comprobación de que el borrado ha sido correcto")

        self.assertEqual(result_delete.status_code, 200, "El estado generado es 200")
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_delete.content_type, "application/json",
        "Content-type es del tipo application/json")


        # We are going to try to delete a resource that doesnt exists:
        result_delete = self.app.delete('/predictions',
        data=json.dumps({'ID':666}),headers=headers)

        # self.assert  Equal(result_delete.get_json(), {'predictions':[my_second_dict]})
        self.assertEqual(result_delete.get_json(),{'msg': "Deleted"},
        "Comprobación de que el contenido devuelto es correcto")
        self.assertEqual(result_delete.status_code, 200, "El estado generado es 200")
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_delete.content_type, "application/json",
        "Content-type es del tipo application/json")


        # https://coverage.readthedocs.io/en/coverage-4.2/excluding.html
        # To test the database, we are going to try it with a clean
        # database
        delete_all_documents()
        pass


if __name__ == '__main__':
    unittest.main()
