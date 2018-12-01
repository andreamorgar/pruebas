import os
import weather_class
import unittest
import tempfile
import json

from predictionDB import getDocument, pushDocument, updateDocument
from predictionDB import get_all_predictions, delete_document
from predictionDB import get_number_documents, delete_all_documents


class TestCase(unittest.TestCase):

    # --------------------------------------------------------------------------
    def setUp(self):

        delete_all_documents()

        # We create values to test the database
        self.city = "Salamanca"
        self.temperature = "26"

        self.city2 = "Granada"
        self.temperature2 = "10"
        self.post_temperature = "45"

    # --------------------------------------------------------------------------
    def test_1_test_document(self):

        # At the first time, the database is empty:

        self.assertEqual(get_number_documents(), 0,
         "Al principio no hay documentos en la base de datos")

        # We are going to create a document, to test with it. Firstly, we have
        # to create a dictionary, because it is easy to import to the basedata
        dict_testing={ "ID":1, "city":self.city, "temperature":self.temperature}
        pushDocument(dict_testing)

        # By this moment, the size of the database has to be 1
        self.assertEqual(get_number_documents(), 1,
         "Comprobación de que aumenta el número de documentos")

        # We can access to the document we have create in the database:
        document = getDocument(1)
        self.assertEqual(dict_testing, document, "El documento que hemos subido tiene "
         + "la misma información que el alojado en la base de datos")


        self.assertEqual(dict_testing, get_all_predictions().__getitem__(0),
        "El documento que hemos subido tiene "
         + "la misma información que el alojado en la base de datos")


        # Now, with the same document we have already got from the database, we
        # are going to update one of its key values
        updated_dict ={ "city":self.city2}
        updateDocument(document,updated_dict)

        # To test the update, we have to get again the document
        document = getDocument(1)

        # We create a new dict with the data that its supposed to be at the
        # document. But first, we dont know the id of the document (that one
        # that it is created by mongo, so we ommit it, because it is not affecting
        # our test)
        document.pop('_id')
        updated_document={ "ID":1, "city":self.city2, "temperature":self.temperature}
        self.assertEqual(updated_document, document,
        "El documento en la base de datos se ha actualizado de forma correcta")

        # And we have to test if we can delete the document
        delete_document(document)
        # By now, the number of documents in database is 0 again.
        self.assertEqual(get_number_documents(), 0, "No hay documentos en la base de datos")


        # At last, we create two new documents, because we want to test the
        # function that delete all documents from the database
        pushDocument(dict_testing)
        dict_testing2={ "ID":1, "city":self.city2, "temperature":self.temperature2}
        pushDocument(dict_testing2)

        self.assertEqual(get_number_documents(), 2,
        "Número de documentos en la base de datos es correcto")

        delete_all_documents()
        self.assertEqual(get_number_documents(), 0,
        "Número de documentos en la base de datos es correcto")

        pass
