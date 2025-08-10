from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

config = dotenv_values(".env")


# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#     ___       __     __                      __     _                   "
#    /   |     / /_   / /_   ___     ____     / /_   (_)  ____     ____   " 
#   / /| |    / __/  / __/  / _ \   / __ \   / __/  / /  / __ \   / __ \  "
#  / ___ |   / /_   / /_   /  __/  / / / /  / /_   / /  / /_/ /  / / / /  "
# /_/  |_|   \__/   \__/   \___/  /_/ /_/   \__/  /_/   \____/  /_/ /_/   "
###########################################################################
# """
# 🔥 PLEASE PLACE YOUR MONGODB URI HERE (↓) 🔥
uri = config['MONGODB_URI']
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
db = client["memnotes"]
nc = db["notes"]
uc = db["users"]


def get_user(username):
    user = uc.find_one({"username": username})
    return user


def all_users():
    users = [x["username"] for x in uc.find()]
    return users


def create_account(username, password):
    uc.insert_one({"username": username, "password": password})


def get_notes(username):
    cursor = nc.find({"username": username})
    all_contents = [doc for doc in cursor]
    return all_contents


def create_note(title, content, username, time, code):
    nc.insert_one(
        {
            "title": title,
            "content": content,
            "username": username,
            "time": time,
            "code": code,
        }
    )


def delete_note(username, title, content):
    nc.delete_one({"username": username, "title": title, "content": content})


def edit_note(code, new_content):
    nc.update_one({"code": code}, {"$set": {"content": new_content}})


def search_notes(query, username, db):
    data = nc.find(
        {
            "username": username,
            "content": {"$regex": f"{query}", "$options": "i", "$options": "i"},
        }
    )
    data = [x for x in data]
    data = [
        (
            x["title"],
            x["content"],
            x["time"].strftime("%b %d, %Y at %I:%M %p"),
            x["code"],
        )
        for x in data
    ]
    return data if data else None
