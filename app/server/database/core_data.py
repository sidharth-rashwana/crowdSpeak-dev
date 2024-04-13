from typing import Any
from app.server.database.db import mongo
from app.server.utils import date_utils
from app.server.model.login import SignUp
from pymongo.collection import ReturnDocument
from pydantic import EmailStr
from bson.objectid import ObjectId
from app.server.utils import date_utils


async def create_one(collection_name: str,
                     data: dict[str, Any]) -> dict[str, Any]:
    """Insert one operation on database

    Returns:
        dict[str, Any]: inserted document
    """
    try:
        collection = mongo.get_collection(collection_name)
        if "_id" not in data:
            # Generate a unique string ID if _id is not provided
            data["_id"] = str(ObjectId())

        timestamp = date_utils.get_current_timestamp()
        data.update({'createdAt': timestamp})
        result = await collection.insert_one(data)
    except Exception as e:
        raise Exception("Failed to insert document: " + str(e))

    if not result.acknowledged:
        raise Exception("Failed to acknowledge document insertion")

    return {'acknowledge': result.acknowledged,
            '_id': data["_id"], 'status': 'SUCCESS'}


async def create_many(collection_name: str,
                      data: list[SignUp]) -> dict[str, Any]:
    """Insert one operation on database

    Returns:
        dict[str, Any]: inserted document acknowledgement and id
    """
    try:
        collection = mongo.get_collection(collection_name)
        result = await collection.insert_many(data)
    except Exception as e:
        raise Exception("Failed to insert document: " + str(e))

    if not result.acknowledged:
        raise Exception("Failed to acknowledge document insertion")

    return {
        'acknowledge': result.acknowledged,
        '_id': str(
            result.inserted_ids),
        'status': 'SUCCESS'}


async def read_one(collection_name: str,
                   data: dict[str, Any]) -> dict[str, Any]:
    """Read one operation on database

    Returns:
        dict[str, Any]: response
    """
    try:
        collection = mongo.get_collection(collection_name)
        result = await collection.find_one(data)

        if result is None:
            return {'status': 404, 'msg': 'not found'}

        result = dict(result)
        result['status'] = 200
        return result

    except Exception as e:
        raise Exception(str(e))


async def read_many(collection_name: str,
                    filter: dict[str, Any]) -> list[dict[str, Any]]:
    """Read all documents based on filter

    Returns:
        list[dict[str, Any]]: response
    """
    try:
        collection = mongo.get_collection(collection_name)
        cursor = collection.find(filter)
        documents = await cursor.to_list(length=None)
        return documents

    except Exception as e:
        raise Exception(str(e))


async def read_all(collection_name: str) -> list[dict[str, Any]]:
    """Read all documents

    Returns:
        list[dict[str, Any]]: response
    """
    try:
        collection = mongo.get_collection(collection_name)
        cursor = collection.find()
        documents = await cursor.to_list(length=None)
        return documents

    except Exception as e:
        raise Exception(str(e))


async def update_one(collection_name: str, filter_by,
                     update_by) -> dict[str, Any]:
    """update one operation on database

    Returns:
        dict[str, Any]: response
    """
    try:
        collection = mongo.get_collection(collection_name)
        result = await collection.find_one_and_update(filter_by, update_by, return_document=ReturnDocument.AFTER)
        if not result:
            raise Exception("Update failed: Document not found")
        return result
    except Exception as e:
        raise Exception(f"Update failed: {e}")


async def delete_one(collection_name: str, email: EmailStr) -> dict[str, Any]:
    """delete one document from collection in database


    Returns:
        dict[str, Any]: response
    """
    try:
        collection = mongo.get_collection(collection_name)
        result = await collection.delete_one(email)
        if result.deleted_count == 0:
            return {'status': 404, 'msg': 'not found'}

        if not result.acknowledged:
            raise Exception("Failed to acknowledge User deletion")

        return {'acknowledge': result.acknowledged,
                'msg': f'User with {email} is deleted.'}

    except Exception as e:
        raise Exception(f"Delete failed: {e}")


async def delete_all(collection_name: str) -> dict[str, Any]:
    """delete all documents from collection in database


    Returns:
        dict[str, Any]: response
    """
    try:
        collection = mongo.get_collection(collection_name)
        result = await collection.delete_many({})

        if result is None:
            return {'status': 404, 'msg': 'No element present to delete'}

        if not result.acknowledged:
            raise Exception("Failed to acknowledge documents deletion")

        return {'acknowledge': result.acknowledged,
                'deletedCount': f'Total records deleted {result.deleted_count}'}

    except Exception as e:
        raise Exception(f"Delete failed: {e}")
