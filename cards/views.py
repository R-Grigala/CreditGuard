from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Card
from .serializers import CardSerializer

class CardViewSet(viewsets.ViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['created_at']
    filterset_fields = ['title']

    def user_card(self, request):
        # Retrieve cards created by the authenticated user
        cards = Card.objects.filter(user=request.user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
