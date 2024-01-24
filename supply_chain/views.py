from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import NetworkEntity
from .permissions import IsActiveEmployee
from .serializers import NetworkEntityListSerializer, NetworkEntityCreateUpdateSerializer


class NetworkEntityViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели NetworkEntity, обеспечивающий базовые CRUD операции.
    Этот ViewSet использует разные сериализаторы для операций чтения и создания/обновления.
    Также применяется фильтрация по стране контакта и проверка разрешений для доступа к данным.
    """
    queryset = NetworkEntity.objects.all()
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact__country']

    def get_serializer_class(self):
        """
        Определяет сериализатор, который должен быть использован в зависимости от типа действия.

        Возвращает сериализатор NetworkEntityListSerializer для операций чтения ('list' и 'retrieve')
        и NetworkEntityCreateUpdateSerializer для всех остальных операций.
        """
        if self.action in ['list', 'retrieve']:
            return NetworkEntityListSerializer
        return NetworkEntityCreateUpdateSerializer
