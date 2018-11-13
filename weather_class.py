
import datetime
import json


# Definimos métodos porque nos conviene que se comporte como un dict
# https://gist.github.com/turicas/1510860


# How to document a class in Python:
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

class Prediction:
    """Common base class for prediction taken from AEMET API

    Attributes:
        city (str):           refers to the city when the prediction is taken
        temperature (float):  refers to the temperature in the city we refered above
        date (str):           actual date, when the predition is load to the database
        ID (int):             identificator of the object prediction

    By default, initially the ID is 0, and, when a object from the class is
    created, its ID value takes the next one avaiable.
    """
    ID = 0

    def __init__(self, city, temperature):

        """ Args:
            city (str): refers to the city where the predition is taken.
            temperature (float): value of temperature for the city above.

        """
        self.city = city
        self.temperature = temperature

        """ The date value is automatically genered by the day where the predition
        is introduced in the database """
        now = datetime.datetime.now().strftime('%d-%m-%Y')
        self.date = now

        """ The ID value is automatically asigned by the moment we create the
        object. """
        Prediction.ID += 1
        self.ID = Prediction.ID


    # def __setitem__(self,key,value):
    #     assert type(value) is str
    #     self.__dict__[key] = value

    def set_city(self,value):
        """ Method that allows to modify the value of the city

            Args:
            value (str): refers to the new value that the attribute city is
            going to take

            Returns:
            None
        """
        self.city = value

    def set_temperature(self,value):
        """ Method that allows to modify the value of the temperature

            Args:
            value (str): refers to the new value that the attribute temperature
            is going to take

            Returns:
            None
        """
        self.temperature = value

    def __getitem__(self, key):
        """ Method to get the value of an attribute of the class. For this
        functionality, it works in the same way than  a dict object.

            Args:
            key (str): refers to the name of the attribute we want to know
            the value

            Returns:
            Value associated to the attribute called 'key'

        """
        return self.__dict__[key]

    def __len__(self):
        """ Method to get the value of the number of attribute in the class.

            Args:
            No args

            Returns:
            An int value that represents the number of attributes in the class
        """
        return len(self.__dict__)

    def __repr__(self):

        """ Method to get a string representation with the information in class.

            Args:
            No args

            Returns:
            A str with all the content of the attributes and their values.
        """
        return repr(self.__dict__) # pragma: no cover



# ------------------------------------------------------------------------------
# if __name__ == '__main__':


    # my_prediction = Prediction ("Granada", "30")
    # my_prediction2 = Prediction("Malaga","24")
    #
    # my_prediction["ciy"] = "almeria"
    # print(type(my_prediction.city))
    # my_prediction.set_temperature(40)
    #
    #
    # preds = [my_prediction.__dict__,my_prediction2.__dict__]
    #
    #
    # json_preds = json.dumps(preds)
    #
    # print(my_prediction.__doc__)
