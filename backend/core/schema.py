import graphene

import api.schema

class Query(api.schema.Query, graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(api.schema.Mutation, graphene.ObjectType):
    # Combine the mutations from different apps
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)