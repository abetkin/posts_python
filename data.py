from graphql.core.type.definition import GraphQLArgument, GraphQLField, GraphQLNonNull, \
    GraphQLObjectType, GraphQLList
from graphql.core.type.scalars import GraphQLString, GraphQLInt
from graphql.core.type.schema import GraphQLSchema

from util import asobj



import itertools
import weakref

class Node:
    '''
    Remembers instance id when it's created
    '''
    instances = weakref.WeakValueDictionary()

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls, *args, **kwargs)
        cls.instances[id(instance)] = instance
        return instance

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Post(Node):
    pass

class User(Node):
    pass


blog = Post(
    parent = None,
    id = 1,
    title = 'Blog',
    text = 'Any posts are welcome',
    tags = ['root', 'moderated'],
    comments = [],
)




post = Post(
    id = 2,
    parent = 1,
    text = 'Let there be text',
    tags = ['misc'],
)


posts = [blog, post]

me = User(name = 'vitalik', email = 'abvit89@gmail.com')


def get_user():
    return me

def get_comments_for(post_id):
    return (p for p in posts if p.parent == post_id)

def get_post(post_id):
    return next(p for p in posts if p.id == post_id)

def create_post(**data):
    post = Post(**data)
    post.id = len(posts) + 1
    posts.append(post)
    return get_post(post.parent)