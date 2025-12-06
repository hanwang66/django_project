from rest_framework import viewsets
from rest_framework.response import Response
from .models import RealEstate
from .serializers import RealEstateSerializer

class RealEstateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()  # 获取所有 queryset
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)