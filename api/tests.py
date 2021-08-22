from django.test import TestCase
from .models import PackageRelease, Project
from .serializers import package_validation, PackageSerializer
from rest_framework.test import APIRequestFactory


class ProjectTestCase(TestCase):
    def test_deve_retornar_atributos(self):
        self.assertTrue(hasattr(Project, 'name'))

    def test_deve_criar_item(self):
        project = Project.objects.create(name='titan')
        self.assertIsNotNone(project)

    def test_deve_acertar_metodos(self):
        project = Project.objects.create(name='titan')
        self.assertEqual(project.name, 'titan')
        self.assertEqual(str(project), 'titan')


class PackageReleaseTestCase(TestCase):
    def test_deve_retornar_atributos(self):
        self.assertTrue(hasattr(PackageRelease, 'name'))
        self.assertTrue(hasattr(PackageRelease, 'version'))

    def test_deve_criar_item(self):
        project = Project.objects.create(name='titan')
        package = PackageRelease.objects.create(name='Django', version='3', project=project)
        self.assertIsNotNone(package)

    def test_package_sem_versao(self):
        project = Project.objects.create(name='titan')
        package = PackageRelease.objects.create(name='Django', project=project)
        self.assertEqual(package.version, '')
        self.assertEqual(str(package), 'Django ')

    def test_package_com_versao(self):
        project = Project.objects.create(name='titan')
        package = PackageRelease.objects.create(name='Django', version='3.2.5', project=project)
        self.assertEqual(package.version, '3.2.5')
        self.assertEqual(str(package), 'Django 3.2.5')


class PackageValidationTestCase(TestCase):

    def test_deve_existir_pacote(self):
        package = {"name": "Django", "version": "3.2.5"}
        package_exist = package_validation(package)
        self.assertEqual(package_exist, True)

    def test_deve_buscar_ultima_versao_disponivel(self):
        package = {"name": "Django"}
        package_validation(package)
        self.assertEqual(package['version'], "3.2.6")

    def test_deve_falhar_nome_de_pacote_invalido(self):
        package = {"name": "Djanfo"}
        package_exist = package_validation(package)
        self.assertFalse(package_exist, True)

    def test_deve_falhar_versao_invalida(self):
        package = {"name": "Django", "version": "4.0"}
        package_exist = package_validation(package)
        self.assertFalse(package_exist, True)

    def test_deve_falhar_nome_e_versao_invalida(self):
        package = {"name": "Djafo", "version": "5.8.0"}
        package_exist = package_validation(package)
        self.assertFalse(package_exist, True)


class PackageReleaseSerializerTestCase(TestCase):

    def test_serializacao_de_package_sem_versao(self):
        project = Project.objects.create(name='titan')
        package = PackageRelease.objects.create(name="Django", project=project)

        factory = APIRequestFactory()
        request = factory.post('/project/', {})
        data = PackageSerializer(package, context={'request': request}).data

        self.assertEqual(data, {'name': 'Django', 'version': ''})

    def test_serializacao_de_package_com_versao(self):
        project = Project.objects.create(name='titan2')
        package = PackageRelease.objects.create(name="Django", version="3.5.6", project=project)

        factory = APIRequestFactory()
        request = factory.post('/project/', {})
        data = PackageSerializer(package, context={'request': request}).data

        self.assertEqual(data, {'name': 'Django', 'version': '3.5.6'})

