"""Importing third-party libraries"""
import requests

"""Importing standard library modules"""
import json

"""Importing extensions"""
from my_exceptions import *

"""Read the currencies dictionary"""
currencies_dict = {}
with open("currencies.txt", encoding = "UTF-8") as f:
    service_str = ""
    for line in f.readlines():
        service_str += line
    currencies_dict = json.loads(service_str)

"""Сlass that returns an object, containing a dict with currencies rates in the attribute self.rates"""
class Exchange_Rates:
    def __init__(self, URL):
        self.URL = URL
        self.response = requests.get(self.URL)
        self.content = json.loads(self.response.content.decode("UTF-8"))["Valute"]
        self.rates = {}
        for key in self.content:
            self.rates[key] = {"Nominal": self.content[key]["Nominal"], "Rate": self.content[key]["Value"]}

"""Input validation function"""
def input_validation(string):
    service_str = string.split()
    if len(service_str) != 3:
        raise WrongAmountOfArguments
    if service_str[0] not in currencies_dict:
        raise WrongBaseCurrency(f"The base currency [{service_str[0]}] is incorrect or no data about. Command /values - available currencies")
    if service_str[1] not in currencies_dict:
        raise WrongQuoteCurrency(f"The qoute currency [{service_str[1]}] is incorrect or no data about. Command /values - available currencies")
    if not service_str[2].isdigit():
        raise WrongAmount(f"Wrong amount of base currency [{service_str[2]}]. Must be number")
    if int(service_str[2]) <= 0 or int(service_str[2]) > 1000000000:
        raise WrongAmount(f"Wrong amount of base currency [{service_str[2]}]. Must be greater than zero and less than a billion")
    return True
