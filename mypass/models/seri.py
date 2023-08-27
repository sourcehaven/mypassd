import json
from json import JSONEncoder

from flask.json.provider import JSONProvider

from .entry import VaultEntry, Tag
from .user import User


class ModelPlusJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, VaultEntry):
            return {
                'id': o.id,
                'username': o.username,
                'password': o.password,
                'title': o.title,
                'website': o.website,
                'folder': o.folder,
                'notes': o.notes,
                'tags': o.tags,
                'parentid': o.parent_id
            }
        if isinstance(o, Tag):
            return {
                'id': o.id,
                'name': o.name,
                'createtime': o.create_time
            }
        if isinstance(o, User):
            return {
                'id': o.id,
                'username': o.username,
                'createtime': o.create_time,
                'email': o.email,
                'firstname': o.firstname,
                'lastname': o.lastname
            }
        return super().default(o)


class ModelPlusJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, cls=ModelPlusJSONEncoder, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)
