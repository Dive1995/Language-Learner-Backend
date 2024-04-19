from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv(find_dotenv())

MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING")

connection_string = f"{MONGO_CONNECTION_STRING}"

if connection_string:
    client = MongoClient(connection_string)

    language_learning_db = client.language_learning

    user_collection = language_learning_db.users

def add_new_vocabulary(args):
    user_id = ObjectId(args["id"])

    update_existing_list = user_collection.update_one(
        {"_id": user_id ,"videoHistory.video_id": args["videoId"]},
        { "$addToSet": {"videoHistory.$.vocabList": args['vocabulary']}}
    )

    if(update_existing_list.matched_count == 0):
        add_new_list = user_collection.update_one(
            {"_id": user_id},
            {"$addToSet": {"videoHistory": {"video_id": args["videoId"], "vocabList":[args['vocabulary']]}}}
        )
    
    
    existing_user = get_user_by_id(user_id)

    return {"id": str(existing_user['_id']),"name": existing_user['name'], "email": existing_user['email'], "given_name": existing_user['given_name'], "family_name":existing_user['family_name'], "videoHistory": existing_user.get('videoHistory', [])}


def get_user_by_id(id):
    return user_collection.find_one({"_id": id})


def create_user(user):
    user["videoHistory"] = [];
    result = user_collection.insert_one(user);
    
    if(result.acknowledged):
        return {"id": str(result.inserted_id),"name": user.name, "email": user.email, "given_name": user.given_name, "family_name":user.family_name, "videoHistory":user["videoHistory"]}    
    
    return {"message": "User hasn't added successfully, please try again later."}

def get_or_update_user(user):
    existing_user = user_collection.find_one({"email": user.email})

    if(existing_user):
        return {"id": str(existing_user['_id']),"name": existing_user['name'], "email": existing_user['email'], "given_name": existing_user['given_name'], "family_name":existing_user['family_name'], "videoHistory": existing_user.get('videoHistory', [])}
    else:
        return create_user(user)