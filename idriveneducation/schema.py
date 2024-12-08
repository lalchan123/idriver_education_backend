import graphene
import channels_graphql_ws
import channels

from courseapp import schema

class Query(schema.Query, graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    
class Mutation(schema.Mutation, graphene.ObjectType):
    pass   

class Subscription(schema.Subscription):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
      
    async def on_connect(self, payload):
        print("New client connected!")

    schema = schema