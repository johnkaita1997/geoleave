# Create your views here.

from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils import SchoolIdMixin, UUID_from_PrimaryKey
from .models import Leavetype
from .serializers import LeavetypeSerializer


class LeavetypeCreateView(SchoolIdMixin, generics.CreateAPIView):
    serializer_class = LeavetypeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        school_id = self.check_school_id(self.request)
        if not school_id:
            return JsonResponse({'detail': 'Invalid school in token'}, status=401)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['school'] = school_id
            self.perform_create(serializer)
            return Response({'detail': 'Leavetype created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class LeavetypeListView(SchoolIdMixin, generics.ListAPIView):
    serializer_class = LeavetypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        school_id = self.check_school_id(self.request)
        if not school_id:
            return Leavetype.objects.none()
        queryset = Leavetype.objects.filter(school=school_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({}, status=200)
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class LeavetypeDetailView(SchoolIdMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Leavetype.objects.all()
    serializer_class = LeavetypeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        primarykey = self.kwargs['pk']
        try:
            id = UUID_from_PrimaryKey(primarykey)
            return Leavetype.objects.get(id=id)
        except (ValueError, Leavetype.DoesNotExist):
            raise NotFound({'detail': 'Record Not Found'})

    def update(self, request, *args, **kwargs):
        school_id = self.check_school_id(request)
        if not school_id:
            return JsonResponse({'detail': 'Invalid school_id in token'}, status=401)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.validated_data['school_id'] = school_id
            self.perform_update(serializer)
            return Response({'detail': 'Leavetype updated successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        school_id = self.check_school_id(request)
        if not school_id:
            return JsonResponse({'error': 'Invalid school_id in token'}, status=401)

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Record deleted successfully'}, status=status.HTTP_200_OK)
