# Create your views here.

from django.contrib.auth.models import Group
from django.http import Http404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import DepartmentSerializer


class DepartmentCreateView(generics.CreateAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            is_exists = Group.objects.filter(name=name.upper()).exists()

            if not is_exists:
                Group.objects.create(name=name.upper())
                return Response({'detail': 'Department created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Department with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class DepartmentListView( generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    def list(self, request, *args, **kwargs):
        authenticated_user = request.user
        #user_roles = fetchusergroups(authenticated_user.id)
        # role_data = [{'name': role.name, 'id': role.id} for role in user_roles]
        return Response([], status=status.HTTP_200_OK)



class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        role_id = self.kwargs['pk']
        try:
            return Group.objects.get(id=role_id)
        except Group.DoesNotExist:
            raise NotFound({'detail': 'Record Not Found'})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Department updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        role_id = kwargs['pk']
        try:
            instance = Group.objects.get(id=role_id)
            print(f"Found instance {instance}")
            instance.delete()
            return Response({'detail': 'Record deleted successfully'}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            raise Http404({'detail': 'Record Not Found'})
