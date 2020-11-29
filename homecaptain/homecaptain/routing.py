# mysite/routing.py
from django.urls import path

from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import apps.hcauth.routing
from apps.hcauth.token_auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            apps.hcauth.routing.websocket_urlpatterns
        )
    ),
})
