from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def login(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    try: 
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Usuario inválido")

    pwd_valid = check_password(password,user.password)

    if not pwd_valid:
        return Response("Contraseña inválida")

    token, _ = Token.objects.get_or_create(user=user)

    return Response(token.key)





# Create your views here.
