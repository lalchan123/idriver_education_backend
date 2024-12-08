from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path 
from channels.auth import AuthMiddlewareStack
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer

from idriveneducation.schema import MyGraphqlWsConsumer


from accountapp.consumers import *


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(URLRouter([
        path('graphql', MyGraphqlWsConsumer.as_asgi()),
        path('ws/sc/', MySyncConsumer.as_asgi()),
        path('ws/asc/', MyASyncConsumer.as_asgi()),
        path('ws/chat/', ChatConsumer.as_asgi()),
    ]))
})

