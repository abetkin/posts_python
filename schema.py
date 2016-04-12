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



class RelayMutation:
    name = None

    def get_input_fields(self):
        raise NotADirectoryError

    def get_output_fields(self):
        raise NotImplementedError

    def mutate(self, **params):
        raise NotImplementedError

    def _resolver(self, obj, args, info):
        params = args.get('input')
        result = self.mutate(**params)
        result.clientMutationId = params['clientMutationId']
        return result

    @classmethod
    def build(cls):
        self = cls()
        output_fields = self.get_output_fields()
        output_fields.update({
            'clientMutationId': GraphQLField(GraphQLNonNull(GraphQLString))
        })
        output_type = GraphQLObjectType(
            self.name + 'Payload',
            fields=output_fields)
        input_fields = self.get_input_fields()
        input_fields.update({
            'clientMutationId':
                GraphQLInputObjectField(GraphQLNonNull(GraphQLString))
        })
        input_arg = GraphQLArgument(GraphQLNonNull(GraphQLInputObjectType(
            name=self.name + 'Input',
            fields=input_fields)))
        return GraphQLField(
            output_type,
            args = {
                'input': input_arg,
            },
            resolver=self._resolver
        )




class AddPostMutation(RelayMutation):
    name = 'AddPost'

    def get_input_fields(self):
        return {
            'parent_id': GraphQLInputObjectField(GraphQLInt),
            'title': GraphQLInputObjectField(GraphQLString),
            'text': GraphQLInputObjectField(GraphQLString),
            'tags': GraphQLInputObjectField(GraphQLList(GraphQLString)),
        }


    def get_output_fields(self):
        return {
            'post': GraphQLField(PostType),
        }

    def mutate(self, **params):
        params['parent'] = params.pop('parent_id')
        return asobj({'post': create_post(**params)})


MutationType = GraphQLObjectType('Mutation', {
    'addPost': AddPostMutation.build()

})


schema = GraphQLSchema(query=QueryRootType, mutation=MutationType)
