from enum import Enum as PyEnum
from graphql import GraphQLEnumType, GraphQLInputObjectType, GraphQLInterfaceType, GraphQLObjectType, GraphQLScalarType, GraphQLUnionType

class GrapheneGraphQLType:
    """
    A class for extending the base GraphQLType with the related
    graphene_type
    """

    def __init__(self, *args, **kwargs):
        self.graphene_type = kwargs.pop('graphene_type')
        super(GrapheneGraphQLType, self).__init__(*args, **kwargs)

    def __copy__(self):
        result = GrapheneGraphQLType(graphene_type=self.graphene_type)
        result.__dict__.update(self.__dict__)
        return result

class GrapheneInterfaceType(GrapheneGraphQLType, GraphQLInterfaceType):
    pass

class GrapheneUnionType(GrapheneGraphQLType, GraphQLUnionType):
    pass

class GrapheneObjectType(GrapheneGraphQLType, GraphQLObjectType):
    pass

class GrapheneScalarType(GrapheneGraphQLType, GraphQLScalarType):
    pass

class GrapheneEnumType(GrapheneGraphQLType, GraphQLEnumType):
    pass

class GrapheneInputObjectType(GrapheneGraphQLType, GraphQLInputObjectType):
    pass