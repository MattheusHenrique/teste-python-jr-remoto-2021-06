import json
import requests
from rest_framework import serializers
from api.models import PackageRelease, Project


def package_validation(package) -> bool:
    """ Consumes the pypi API to verify that the data received is correct and adds the latest version if not
    specified. Returns true if exists packages"""
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
        verified_packages = []  # Project Package List
        package_exist = True  # Flag to mark if any packages do not exist.
        project = Project.objects.create(name=validated_data['name'])

        if len(packages) == 0:  # If no package is passed, returns error.
            project.delete()
            raise serializers.ValidationError(
                {"error": "At least one package must exist"}
            )

        for package in packages:
            # If any package does not exist the interaction stops and returns an error.
            package_exist = package_validation(package)
            if package_exist is False:
                break

            package = PackageRelease.objects.create(
                **package,
                project_id=project.id
            )
            verified_packages.append(package)

        # Checks if the search for packages failed.
        if package_exist is True:
            project.packages.set([verified_packages][0])
            return project

        # If the project is invalid.
        project.delete()
        raise serializers.ValidationError(
            {"error": "One or more packages doesn't exist"}
        )
