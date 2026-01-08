from rest_framework.views import APIView
from rest_framework.response import Response


class HomeAPIView(APIView):
    '''
    Стартовый API эндпоинт.
    Возвращает тестовое сообщение для проверки связки React ↔ Django.
    '''

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Главная страница'})

