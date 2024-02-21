from rest_framework.authtoken.models import Token

def get_user_by_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
        return user
    except Token.DoesNotExist:
        return None
