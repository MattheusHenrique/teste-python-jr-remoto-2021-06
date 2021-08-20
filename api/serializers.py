import json

import requests
from rest_framework import serializers

from api.models import PackageRelease, Project


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ['name', 'version']
        extra_kwargs = {'version': {'required': False}}


# Verifica os pacotes e se não existir retorna erro.
global_url = 'https://pypi.org/'


def package_pypi_validation(package):
    url = "{}/pypi/{}/json/".format(global_url, package['name'])
    response_json = requests.get(url)
    if response_json.status_code == 200:
        parsed = json.loads(response_json.text)
        if package.get('version') is None:
            package['version'] = parsed['info']['version']
        return True
    else:
        return False


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'packages']

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        # variaveis auxiliares para facilar o codigo
        packages = validated_data.pop('packages')
        packages_verificate = []
        # Flag para lançamento de erro caso False
        package_exist = True

        project = Project.objects.create(name=validated_data['name'])

        for package in packages:

            if package_pypi_validation(package) is False:
                package_exist = False

            package_pypi_validation(package)

            package = PackageRelease.objects.create(
                **package,
                project_id=project.id
            )
            packages_verificate.append(package)

        # Se a flag for falsa então lança erro
        if package_exist is True:
            project.packages.set([packages_verificate][0])
            return project
        else:
            project.delete()
            raise serializers.ValidationError(
                {"error": "One or more packages doesn't exist"}
            )
