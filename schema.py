from graphql.core.type.definition import GraphQLArgument, GraphQLField, GraphQLNonNull, \
    GraphQLObjectType, GraphQLList
from graphql.core.type.scalars import GraphQLString, GraphQLInt
from graphql.core.type.schema import GraphQLSchema

from data import get_user, get_comments_for, get_post, create_post

from _relay import get_node_by_id, resolve_node_type


@resolve_node_type
def node_interface(obj):
    return {
        'Post': PostType,
        'User': UserType,
    }[obj.type]


@get_node_by_id(node_interface)
def node(id, info):
    assert info.schema == schema
    if id in userData:
        return userData[id]
    else:
        return photoData[id]



UserType = GraphQLObjectType('UserType', {
    'email': GraphQLField(GraphQLString),
    'name': GraphQLField(GraphQLString),
})


PostType = GraphQLObjectType('PostType', lambda: {
    'post_id': GraphQLField(GraphQLInt, resolver=lambda obj, *_: obj.id),
    'parent':  GraphQLField(GraphQLInt),
    'title': GraphQLField(GraphQLString),
    'text': GraphQLField(GraphQLString),
    'author': GraphQLField(UserType, resolver=lambda *_: get_user()),
    'comments': GraphQLField(
        GraphQLList(PostType),
        description= 'Posted comments',
        resolver=lambda post, *_: get_comments_for(post.id)
    ),
    'tags': GraphQLField(
        GraphQLList(GraphQLString),
        description='Tags',
    ),
})



QueryRootType = GraphQLObjectType(
    name='QueryRoot',
    fields={
        'User': GraphQLField(UserType, resolver=lambda *_: get_user()),
        'getPost': GraphQLField(
            PostType,
            args={
                'id': GraphQLArgument(GraphQLInt)
            },
            resolver=lambda obj, args, *_: get_post(args.get('id'))
        ),
    }
)


MutationType = GraphQLObjectType('Mutation', {
    'addPost': GraphQLField(
        PostType,
        args={
            'parent': GraphQLArgument(GraphQLInt),
            'title': GraphQLArgument(GraphQLString),
            'text': GraphQLArgument(GraphQLString),
            'tags': GraphQLArgument(GraphQLList(GraphQLString)),
        },
        resolver=lambda obj, args, *_: create_post(**args))
})



schema = GraphQLSchema(query=QueryRootType, mutation=MutationType)
