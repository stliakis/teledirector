import redis


class BaseDirectorHub(object):
    pass


class RedisDirectorHub(BaseDirectorHub):
    def __init__(self, redis_url):
        self.redis = redis.Redis(host=redis_url.split(":")[0], port=int(redis_url.split(":")[1]), db=0)

    def add_chat_id(self, chat_id, hub_name="main"):
        self.redis.sadd("telegram-director:hubs", hub_name)
        self.redis.sadd("telegram-director:hub:%s" % hub_name, chat_id)

    def get_all_hubs(self):
        return self.redis.smembers("telegram-director:hubs")

    def get_chat_ids(self, hub_name="main"):
        return self.redis.smembers("telegram-director:hub:%s" % hub_name)

    def remove_chat_id(self, chat_id, hub_name="main"):
        self.redis.srem("telegram-director:hub:%s" % hub_name, chat_id)

    def remove_chat_id_from_all_hubs(self, chat_id):
        for hub in self.get_all_hubs():
            self.remove_chat_id(chat_id, hub)
