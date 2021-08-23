import json
import requests
from rest_framework import serializers
from api.models import PackageRelease, Project


def package_validation(package) -> bool:  # Atualizar para pattern match quando possivel (python 3.9.6)
    base_url = 'https://pypi.org/'
    url = f"{base_url}/pypi/{package['name']}/json/"
    response_json = requests.get(url)

    if response_json.status_code == 200:
        parsed = json.loads(response_json.text)

        if package.get('version') is None:
            package['version'] = parsed['info']['version']
            return True

        if package.get('version') in parsed['releases']:
            return True

    return False


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ['name', 'version']
        extra_kwargs = {'version': {'required': False}}


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'packages']

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        packages = validated_data.pop('packages')
        verified_packages = []  # Lista de pacotes do projeto
        package_exist = True  # Flag para marcar se algum pacote não existe.
        project = Project.objects.create(name=validated_data['name'])

        for package in packages:
            # Se algum pacote não existir a interação para e retorna erro.
            package_exist = package_validation(package)
            if package_exist is False:
                break

            package = PackageRelease.objects.create(
                **package,
                project_id=project.id
            )
            verified_packages.append(package)

        # Verifica se houve falha na busca dos pacotes.
        if package_exist is True:
            project.packages.set([verified_packages][0])
            return project

        # Caso o projeto esteja invalido.
        project.delete()
        raise serializers.ValidationError(
            {"error": "One or more packages doesn't exist"}
        )
