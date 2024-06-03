from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Card
from rest_framework.response import Response
from .serializers import CardSerializer
from rest_framework import status

class CardViewSet(APIView):
    queryset = Card.objects.all()

    # Require authentication for this endpoint
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards = Card.objects.filter(user=request.user)
        title = request.query_params.get('title')
        ordering = request.query_params.get('ordering', '-creation_date')
        
        if title:
            cards = Card.objects.filter(user=request.user, title__icontains=title)
    
        cards = cards.order_by(ordering)

        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
