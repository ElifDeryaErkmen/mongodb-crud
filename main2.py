from bson import BSONTIM
from dotenv import load_dotenv, find_dotenv
import os
import pprint
import jsonschema
from pymongo import MongoClient
import json
from pprint import PrettyPrinter
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://derya:{password}@cluster0.afc45yb.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)

dbs = client.list_database_names()
production = client.production

def create_book_collection():
    book_validator = {
            "$jsonschema" : {
                "bsonType": "object",
                "required": ["title", "authors", "publish_date", "type", "copies"],
                "properties": {
                    "title": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "authors": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "objectId",
                            "description": "must be an objectid and is required"
                        }
                    },
                    "publish_date": {
                        "bsonType": "date",
                        "description": "must be a date and is required"
                    },
                    "type": {
                        "enum": ["Fiction", "Non-Fiction"],
                        "description": "can only be one of the enum values and is required"
                    },
                    "copies": {
                        "bsonType": "int",
                        "minimum": 0,
                        "description": "must be an integer greater than 0 and is required."
                    },
                }
            }
        }



    try:
        production.create_collection("book")
    except Exception as e:
        print(e)

    production.command("collMod", "book", validator=book_validator)

create_book_collection()