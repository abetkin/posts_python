from graphql.core.type.definition import GraphQLArgument, GraphQLField, GraphQLNonNull, \
    GraphQLObjectType, GraphQLList
from graphql.core.type.scalars import GraphQLString, GraphQLInt
from graphql.core.type.schema import GraphQLSchema

from util import asobj

def to_global_id(type, id):
    '''
    Takes a type name and an ID specific to that type name, and returns a
    "global ID" that is unique among all types.
    '''
    return base64(':'.join([type, str(id)]))


def from_global_id(global_id):
    '''
    Takes the "global ID" created by toGlobalID, and retuns the type name and ID
    used to create it.
    '''
    unbased_global_id = unbase64(global_id)
    _type, _id = unbased_global_id.split(':', 1)
    return ResolvedGlobalId(_type, _id)


class Node:
    instances = {}

    @classmethod
    def global_id(cls, id_fetcher=None):
        return GraphQLField(
            GraphQLNonNull(GraphQLID),
            description='The ID of an object',
            resolver=lambda obj, *
            _: to_global_id(type_name, id_fetcher(obj) if id_fetcher else obj.id)
        )

    def __new__(cls, **kwargs):
        1


class Post(Node):
    1


class blog:
    parent = None
    id = 1
    title = 'Blog'
    text = 'Any posts are welcome'
    tags = ['root', 'moderated']
    comments = []

    type = 'Post'


class post:
    id = 2
    parent = 1
    text = 'Let there be text'
    tags = ['misc']

    type = 'Post'

posts = [blog, post]


def get_user():
    class me:
        name = 'vitalik',
        email = 'abvit89@gmail.com'

        type = 'User'
    return me

def get_comments_for(post_id):
    return (p for p in posts if p.parent == post_id)

def get_post(post_id):
    return next(p for p in posts if p.id == post_id)

def create_post(**data):
    data = asobj(data)
    posts.append(data)
    return get_post(data.parent)