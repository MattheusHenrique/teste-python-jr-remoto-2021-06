import json
import requests
from rest_framework import serializers
from api.models import PackageRelease, Project

global_url = 'https://pypi.org/'


# Usar parttern match porém so possivel com pyhon 3.9.6
# Atualizar no futuro.
def package_validation(package) -> bool:
    url = "{}/pypi/{}/json/".format(global_url, package['name'])
    response_json = requests.get(url)
    if response_json.status_code == 200:
        parsed = json.loads(response_json.text)
        if package.get('version') is None:
            package['version'] = parsed['info']['version']
        else:
            if package.get('version') in parsed['releases']:
                return True
            else:
                return False
    else:
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

    # Muitas operaçoes dentro da funçao. Refatoraçao necessaria
    def create(self, validated_data):
        packages = validated_data.pop('packages')
        packages_verificate = []
        # Flag caso o um pacote não exista.
        package_exist = True

        # Cria o projeto para que os pacotes sejao relacionados a ele.
        project = Project.objects.create(name=validated_data['name'])

        for package in packages:

            if package_validation(package) is False:
                package_exist = False
                break

            package = PackageRelease.objects.create(
                **package,
                project_id=project.id
            )
            packages_verificate.append(package)

        # Verifica se houve falha na busca dos pacotes.
        if package_exist is True:
            project.packages.set([packages_verificate][0])
            return project
        else:
            project.delete()
            raise serializers.ValidationError(
                {"error": "One or more packages doesn't exist"}
            )
