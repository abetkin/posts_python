'''
adapted from graphql-relay-py

'''

from util import base64, unbase64

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




class ResolvedGlobalId(object):

    def __init__(self, type, id):
        self.type = type
        self.id = id


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


def global_id_field(type_name, id_fetcher=None):
    '''
    Creates the configuration for an id field on a node, using `to_global_id` to
    construct the ID from the provided typename. The type-specific ID is fetcher
    by calling id_fetcher on the object, or if not provided, by accessing the `id`
    property on the object.
    '''
    return GraphQLField(
        GraphQLNonNull(GraphQLID),
        description='The ID of an object',
        resolver=lambda obj, *
        _: to_global_id(type_name, id_fetcher(obj) if id_fetcher else obj.id)
    )
