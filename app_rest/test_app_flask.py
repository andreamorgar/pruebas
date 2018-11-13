import os
import ejercicioFlask_getpost as app_weather
import weather_class
import unittest
import tempfile
import json
import datetime

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

    # --------------------------------------------------------------------------
    def tearDown(self):
        pass

    # --------------------------------------------------------------------------
    def test_app_run(self):
        self.assertEqual(app_weather.app.debug, False)
        pass

    # --------------------------------------------------------------------------
    def test_get_home(self):
        # Hacemos una petición a la ruta inicial. Primero vamos a probar
        # metiendo la ruta de forma correcta.
        result = self.app.get('http://127.0.0.1:5000/')

        # Esta es la razón por la que hay que poner ahí una b:
        # https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal

        # ALTERNATIVAS EQUIVALENTES:
        # self.assertEqual((result.data).decode('utf-8'), 'My project page :)' )
        # self.assertEqual(result.data, b'My project page :)' )
        self.assertEqual(result.get_json(), {'status':'OK'} )

        # Comprobamos que el código sea 200 para garantizar que es correcto.
        self.assertEqual(result.status_code, 200)
        # Comprobamos el tipo del contenido al que se está haciendo get.
        self.assertEqual(result.content_type,"application/json")


        # If we do another get, we have to get the same result
        result_again = self.app.get('http://127.0.0.1:5000/')
        self.assertEqual(result.get_json(), result_again.get_json())


        pass

    # --------------------------------------------------------------------------
    def test_create_prediction(self):

        # 1. COMPROBACIÓN DE GET
        result = self.app.get('http://127.0.0.1:5000/predictions')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, "application/json")

        # Inicialmente la lista de predicciones está vacía. Vamos a comprobar
        # que el resultado sea el que realmente se espera.
        # text_result = result.get_data(as_text=True)

        # Compare dict to dict:
        # https://www.youtube.com/watch?v=kvux1SiRIJQ&t=217s
        self.assertEqual(result.get_json(), {'predictions':app_weather.predictions})


        # 2. Vamos a probar a meter una ruta incorrecta y ver si no funciona.
        result = self.app.get('http://127.0.0.1:5000/ruta_mala')

        # Comprobamos que el código sea 200 para garantizar que es correcto.
        self.assertEqual(result.status_code, 404)
        # Comprobamos el tipo del contenido al que se está haciendo get.
        self.assertEqual(result.content_type, "application/json")

        self.assertEqual(result.get_json(), {'error':'Not found'} ) # -------------repasar esto.

        pass


    def test_get_prediction(self):

        # Initially, there is not predictions, so the structure is empty
        result = self.app.get('http://127.0.0.1:5000/predictions/0')
        # Comprobamos que el código sea 200 para garantizar que es correcto.
        self.assertEqual(result.status_code, 200)
        # Comprobamos el tipo del contenido al que se está haciendo get.
        self.assertEqual(result.content_type, "application/json")
        self.assertEqual(result.get_json(), {'error':'Nonexistent resource'} )

        # We can try to access to another imaginary prediction, and again it is
        # generated an 404 error, because there is not information to show.
        result = self.app.get('http://127.0.0.1:5000/predictions/1')
        # Comprobamos que el código sea 200 para garantizar que es correcto.
        self.assertEqual(result.status_code, 200)

        # Comprobamos el tipo del contenido al que se está haciendo get.
        self.assertEqual(result.content_type, "application/json")
        self.assertEqual(result.get_json(), {'error':'Nonexistent resource'} )


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
        actual_len = len(app_weather.predictions)
        # We send a put with the data and headers above
        result_put = self.app.put('http://127.0.0.1:5000/predictions',
        data=datos,headers=headers)

        # We check the status. If status is 200, it's ok
        self.assertEqual(result_put.status_code, 200)
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_put.content_type, "application/json")
        # We check we have a new value in the vector comparting lengths
        self.assertEqual(len(app_weather.predictions),actual_len+1)


        result = self.app.get('http://127.0.0.1:5000/predictions/1')


        # The object we have just created is saved in last one in Predictions
        # vector, so we can easily check if the information we have saved is
        # the same one we have saved before.

        self.assertEqual(result.get_json(), app_weather.predictions[-1])

        # If we try to get the content again, the result must be the same
        result_again = self.app.get('http://127.0.0.1:5000/predictions/1')
        self.assertEqual(result.get_json(), result_again.get_json())


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
            "ID": len(app_weather.predictions),
            "date": datetime.datetime.now().strftime('%d-%m-%Y')
        }

        self.assertEqual(result.get_json(), my_dict)

        # If we change one value, for example: ID value, we can check that it
        # doesn't work:
        my_dict["ID"]=2
        self.assertNotEqual(result.get_json(), my_dict)



        #And now, if we create a new Prediction, its correct these dictionary.

        data2 = {
            "city": self.city2,
            "temperature": self.temperature2
        }
        datos2 = json.dumps(data2)
        result_new_put = self.app.put('http://127.0.0.1:5000/predictions',
        data=datos2,headers=headers)

        # print(result_new_put.get_json())
        # print(my_dict)

        my_second_dict = {
            "city": self.city2,
            "temperature": self.temperature2,
            "ID": len(app_weather.predictions),
            "date": datetime.datetime.now().strftime('%d-%m-%Y')
        }
        self.assertEqual(result_new_put.get_json(), my_second_dict)

        # In the same way, if we get this last prediction that we have added,
        # we'll get the same content

        result = self.app.get('http://127.0.0.1:5000/predictions/' +
                str(len(app_weather.predictions)))

        self.assertEqual(result.get_json(), app_weather.predictions[-1])


        # At this moment we have 2 resources, we can test it:
        self.assertEqual(len(app_weather.predictions),2)

        # print(app_weather.predictions)

        #  DELETE:
        result_delete = self.app.delete('http://127.0.0.1:5000/predictions',
        data=json.dumps({'ID':1}),headers=headers)

        # After doing delete, the size of the vector should have decreased
        self.assertEqual(len(app_weather.predictions),1)

        # Now we have to prove that the content we deleted above is the right
        # one. We can check the content in the ''result'' var. This var should
        # have the content of the second dict (only)
        # Tenemos que tener una lista de diccionarios que contenga, como unico
        # diccionario ese que no hemos borrado
        self.assertEqual(result_delete.get_json(), {'predictions':[my_second_dict]})


        self.assertEqual(result_delete.status_code, 200)
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_delete.content_type, "application/json")


        # We are going to try to delete a resource that doesnt exists:
        result_delete = self.app.delete('http://127.0.0.1:5000/predictions',
        data=json.dumps({'ID':666}),headers=headers)

        # self.assert  Equal(result_delete.get_json(), {'predictions':[my_second_dict]})
        self.assertEqual(result_delete.get_json(),{'predictions': app_weather.predictions})
        self.assertEqual(result_delete.status_code, 200)
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_delete.content_type, "application/json")


        #  POST TO AN EXISTENT RESOURCE:
        # Now we are going to modify the resource that we have still in the
        # vector.
        post_dictionary = {
            "city": self.city2,
            "temperature": self.post_temperature,
            "ID": 2,
            "date": datetime.datetime.now().strftime('%d-%m-%Y')
        }

        result_post = self.app.post('http://127.0.0.1:5000/predictions',
        data=json.dumps(post_dictionary),headers=headers)

        # We check status, must be MODIFIED
        self.assertEqual(result_post.status_code, 201)
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_post.content_type, "application/json")
        self.assertEqual(result_post.get_json(),{'prediction':post_dictionary})



        #  POST TO AN UNEXISTENT RESOURCE:
        # We try to modify a resource that doesnt exist
        post_dictionary['ID']=1
        result_post = self.app.post('http://127.0.0.1:5000/predictions',
        data=json.dumps(post_dictionary),headers=headers)

        # We check status, must be OK, because we didnt modified anything
        self.assertEqual(result_post.status_code, 200)
        # We check MIME, that has to be json because we send info as json type.
        self.assertEqual(result_post.content_type, "application/json")
        self.assertEqual(result_post.get_json(),{'predictions': app_weather.predictions})



        # https://coverage.readthedocs.io/en/coverage-4.2/excluding.html

if __name__ == '__main__':
    unittest.main()
