from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Card
from rest_framework.response import Response
from .serializers import CardSerializer
from rest_framework import status

class CardViewSet(APIView):
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards = self.get_queryset(request)
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self, request):
        # ვუზრუნველყოთ მხოლოდ user-ის შესაბამისი card-ის წამოღება ბაზიდან
        queryset = Card.objects.filter(user=request.user)

        # შექმნის თარიღის მიხედვით ordering-ის შესაძლებლობა
        ordering = request.query_params.get('ordering', '-creation_date')
        if ordering:
            queryset = queryset.order_by(ordering)

        # title-ით ფილტრაცია
        title = request.query_params.get('title')
        if title:
            queryset = Card.objects.filter(user=request.user, title__icontains=title)

        return queryset
