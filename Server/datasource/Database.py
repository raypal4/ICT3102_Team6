import pymongo

class Database:
    client = pymongo.MongoClient(
        "mongodb+srv://ray:raynoldtan@cluster0.xhxln.mongodb.net/ICT3102?retryWrites=true&w=majority")
    db = client["ICT3102"]