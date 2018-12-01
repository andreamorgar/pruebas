from pymongo import *


# Include URI of mLab
# client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)

client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("predictions")
mongoPrediction = db.mongoPrediction

#-------------------------------------------------------------------------------
# Function if we want to get a prediction from the Database
# This function has only one parameter: ID from the prediction that we want to
# get
def getDocument(document_id):
    predictionDocument = mongoPrediction.find_one({"ID":document_id})
    return predictionDocument

#-------------------------------------------------------------------------------
# Function pushDocument
# With this function, we can add a new document in the collection
def pushDocument(document):
    mongoPrediction.insert_one(document)
    pass
#-------------------------------------------------------------------------------
# Function updateDocument
# With this function, we can update an existent document from the database
def updateDocument(document, updates):
    mongoPrediction.update_one({'_id': document['_id']},{'$set': updates}, upsert=False)
    pass
#-------------------------------------------------------------------------------
# Function to get a cursor with the whole content of the Database
def get_all_predictions():
    return mongoPrediction.find({})
    pass

#-------------------------------------------------------------------------------
# With this function we can delete from the database the document in the parameter
def delete_document(document):
    mongoPrediction.delete_one(document)
    pass
#-------------------------------------------------------------------------------
# With this function we can get the size of the database in terms of the number
# of documents in the database
def get_number_documents():
    return mongoPrediction. estimated_document_count()

#-------------------------------------------------------------------------------
# Function to delete all the documents in the database. Util when we want to test
# the functionality of the database with not real params
def delete_all_documents():
    mongoPrediction.delete_many({})
    pass
