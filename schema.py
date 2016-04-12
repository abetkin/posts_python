from graphql.core.type.definition import GraphQLArgument, GraphQLField, GraphQLNonNull, \
    GraphQLObjectType, GraphQLList
from graphql.core.type.scalars import GraphQLString, GraphQLInt
from graphql.core.type.schema import GraphQLSchema
from graphql.core.type import GraphQLID, GraphQLInputObjectType, \
    GraphQLInputObjectField

from data import Node, get_user, get_comments_for, get_post, create_post

from _relay import get_node_by_id, resolve_node_type

from util import asobj

@resolve_node_type
def node_interface(obj):
    return {
        'Post': PostType,
        'User': UserType,
    }[obj.__class__.__name__]


@get_node_by_id(node_interface)
def node_field(id, info):
    assert info.schema == schema
    return Node.instances[id]

def global_id_field():
    return GraphQLField(
        GraphQLNonNull(GraphQLID),
        description='The ID of an object',
        resolver=lambda obj, *_: id(obj),
    )

UserType = GraphQLObjectType(
    'User', {
        'id': global_id_field(),
        'email': GraphQLField(GraphQLString),
        'name': GraphQLField(GraphQLString),
    },
    interfaces=[node_interface])


PostType = GraphQLObjectType(
    'Post', lambda: {
        'id': global_id_field(),
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
    },
    interfaces=[node_interface])



QueryRootType = GraphQLObjectType(
    name='Query',
    fields={
        'node': node_field,
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




input_fields = {
    'parent_id': GraphQLInputObjectField(GraphQLInt),
    'title': GraphQLInputObjectField(GraphQLString),
    'text': GraphQLInputObjectField(GraphQLString),
    'tags': GraphQLInputObjectField(GraphQLList(GraphQLString)),
}

input_fields.update(clientMutationId = GraphQLInputObjectField(
    GraphQLNonNull(GraphQLString)
))


def addPost(obj, args, _i):
    params = dict(args.get('input'))
    params['parent'] = params.pop('parent_id')
    result = asobj({'post': create_post(**params)})
    result.clientMutationId = params['clientMutationId']
    return result

MutationType = GraphQLObjectType('Mutation', {
    'addPost': GraphQLField(
        GraphQLObjectType(
            'AddPostPayload',
            fields = {
                'clientMutationId':
                    GraphQLField(GraphQLNonNull(GraphQLString)),
                'post':
                    GraphQLField(PostType),
            }),
        args = {
            'input': GraphQLArgument(GraphQLNonNull(GraphQLInputObjectType(
                name='AddPostInput',
                fields=input_fields))),
        },
        resolver=addPost
    ),

})

class RelayMutation:
    'TODO'

    def get_input_fields(self):
        1

    def get_output_fields(self):
        1

    def _resolver(self, obj, args, info):
        1

    def resolve(self, input):
        1

    def build(self):
        1

schema = GraphQLSchema(query=QueryRootType, mutation=MutationType)
