from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """
    
    def __init__(self, inner):
        self.inner = inner
        
    def __call__(self, scope):
        headers = dict(scope['headers'])
        query = dict((x.split('=') for x in scope['query_string'].decode().split("&")))
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    token = Token.objects.get(key=token_key)
                    scope['user'] = token.user
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        elif query.get('token', None):
            token = query['token']
            token = Token.objects.get(key=token)
            scope['user'] = token.user
        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
