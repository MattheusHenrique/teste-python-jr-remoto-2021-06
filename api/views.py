from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "name"

    def delete(self, request, pk=None, *args, **kwargs):

        try:
            project = Project.objects.get(name__exact=pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        project.delete()
        return Response("successfully deleted")
