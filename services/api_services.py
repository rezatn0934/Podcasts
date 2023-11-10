from fastapi import Request
from db.mongo_db import get_mongo_db
from db.redis_db import get_redis_client
from schemas.interaction import InteractionSchema, ActionTypeEnum, BaseInteractionSchema
from services.django_httpx_client import get_django_client


class APIService:
    def __init__(self, redis_db, mongo_db, django_client):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the redis_db and account_client attributes for use in other functions.

        :param self: Represent the instance of the class
        :param redis_db: Create a connection to the redis database
        :param account_client: Create a client object that can be used to call the account service
        :return: A new instance of the class
        :doc-author: Trelent
        """
        self.redis_db = redis_db
        self.mongo_db = mongo_db
        self.django_client = django_client

    async def channels_list(self, request: Request):
        response = await self.django_client.get_channels(request=request)
        return response.json()

    async def get_channels_items(self, user_id: str, channel_id: int, request: Request):
        response = await self.django_client.get_channels_items(request=request, channel_id=channel_id)
        data = response.json()
        channel_info = data.get('channel')
        items = data.get('items')
        collection = self.mongo_db['interaction']
        doc = await collection.find_one({'_id': channel_id})

        if doc:
            for item in items:
                item_id = item['id']
                item_doc = doc.get(str(item_id))
                if item_doc:
                    interactions = {key: value for key, value in item_doc.items()}
                    item['bookmarked'] = any(user_id == user['user_id'] for user in interactions.get('bookmark', []))
                    item['liked'] = any(user_id == user['user_id'] for user in interactions.get('like', []))
                    item['comments'] = interactions.get('comment', 'no comment yet')

        return {'channel_info': channel_info, 'items': items}

    async def get_single_item(self, user_id: str, podcast_id: int, request: Request):
        response = await self.django_client.get_single_item(request=request, podcast_id=podcast_id)
        data = response.json()
        channel_id = data.get('channel')
        collection = self.mongo_db['interaction']
        doc = await collection.find_one({'_id': channel_id})
        item = {}

        if doc:
            item_doc = doc.get(str(podcast_id))
            if item_doc:
                item = {key: value for key, value in item_doc.items()}
                for key, value in item_doc.items():
                    item[f'{key}ed'] = any(user_id == user['user_id'] for user in value)
        data['liked'] = item.get('likeed', '')
        data['bookmarked'] = item.get('bookmarked', '')
        data['comments'] = item.get('comment', 'no comment yet')

        return data

    async def interaction_with_item(self, user_id, interaction: InteractionSchema):
        collection_name = "interaction"
        item_collection = self.mongo_db[collection_name]

        filter_query = {'_id': interaction.channel_id}
        update_query = {}

        if interaction.action_type == ActionTypeEnum.comment:
            update_query['$push'] = {
                f"{interaction.podcast_id}.comment": {
                    'user_id': user_id,
                    'content': interaction.content
                }
            }
        else:
            update_query['$addToSet'] = {
                f"{interaction.podcast_id}.{interaction.action_type.value}": {
                    'user_id': user_id}
            }

        result = await item_collection.update_one(
            filter_query,
            update_query,
            upsert=True
        )

        if result.modified_count > 0 or result.upserted_id is not None:
            return {'status': 'success', 'message': 'Interaction recorded successfully.'}
        elif result.matched_count > 0 and interaction.action_type != ActionTypeEnum.comment:
            return {'status': 'failure', 'message': 'Interaction already exists.'}
        else:
            return {'status': 'failure', 'message': 'Failed to record interaction.'}

    async def remove_interaction(self, user_id, interaction: BaseInteractionSchema):
        collection_name = "interaction"
        item_collection = self.mongo_db[collection_name]

        interaction_type = interaction.action_type.value

        update_query = {
            '$pull': {
                f"{interaction.podcast_id}.{interaction_type}": {
                    'user_id': user_id
                }
            }
        }

        result = await item_collection.update_one(
            {'_id': interaction.channel_id},
            update_query
        )

        if result.modified_count > 0:
            return {'status': 'success', 'message': 'Interaction removed successfully.'}
        else:
            return {'status': 'failure', 'message': 'Interaction not found.'}


api_service = APIService(get_redis_client(), get_mongo_db(), get_django_client())


def get_api_service():
    return api_service
