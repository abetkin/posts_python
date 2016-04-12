'''
adapted from graphql-relay-py

'''


from graphql.core.type import (
    GraphQLArgument,
    GraphQLNonNull,
    GraphQLID,
    GraphQLField,
    GraphQLInterfaceType,
)

from functools import wraps

def get_node_by_id(node_interface):
    '''
    Constructs the node type.
    '''
    def decorate(get_node_by_id):
        return GraphQLField(
            node_interface,
            description='Fetches an object given its ID',
            args={
                'id': GraphQLArgument(
                    GraphQLNonNull(GraphQLID),
                    description='The ID of an object'
                )
            },
            resolver=lambda obj, args, info: get_node_by_id(args.get('id'), info)
        )
    return decorate

def resolve_node_type(get_node_type):
    '''
    Constructs the node interface.
    '''
    return GraphQLInterfaceType(
        'Node',
        description='An object with an ID',
        fields=lambda: {
            'id': GraphQLField(
                GraphQLNonNull(GraphQLID),
                description='The id of the object.',
            ),
        },
        resolve_type=get_node_type
    )

