from pymongo import MongoClient


db_connection = MongoClient("mongodb+srv://GabrielSecret:Usman'sCluster1.@gabrielcluster.pzpglxe.mongodb.net/?retryWrites=true&w=majority")
db = db_connection.flask_mongodb_atlas
collection = db["shops_db"]