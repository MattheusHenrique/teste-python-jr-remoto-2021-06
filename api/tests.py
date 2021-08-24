from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from .models import PackageRelease, Project
from .serializers import package_validation, PackageSerializer


class ProjectTestCase(TestCase):
    def test_deve_retornar_atributos(self):
        self.assertTrue(hasattr(Project, 'name'))

    def test_deve_criar_item(self):
        project = Project.objects.create(name='titan')
        self.assertIsNotNone(project)

    def test_deve_acertar_metodos(self):
        project = Project.objects.create(name='titan')
        self.assertEquals(project.name, 'titan')
        self.assertEquals(str(project), 'titan')


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
        self.assertEquals(package.version, '')
        self.assertEquals(str(package), 'Django ')

    def test_package_com_versao(self):
        project = Project.objects.create(name='titan')
        package = PackageRelease.objects.create(name='Django', version='3.2.5', project=project)
        self.assertEquals(package.version, '3.2.5')
        self.assertEquals(str(package), 'Django 3.2.5')


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

        self.assertEquals(data, {'name': 'Django', 'version': ''})

    def test_serializacao_de_package_com_versao(self):
        project = Project.objects.create(name='titan2')
        package = PackageRelease.objects.create(name="Django", version="3.5.6", project=project)

        factory = APIRequestFactory()
        request = factory.post('/project/', {})
        data = PackageSerializer(package, context={'request': request}).data

        self.assertEquals(data, {'name': 'Django', 'version': '3.5.6'})


class APITestCase(APITestCase):

    def test_requisicao_get_para_listar_projetos(self):
        response = self.client.get('http://testserver/api/projects/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_requisicao_post_para_criar_projetos_sem_versao(self):
        data = {
            "name": "titan",
            "packages": [{"name": "Django"}]
        }
        response = self.client.post('http://testserver/api/projects/', data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_requisicao_post_para_criar_projetos_com_nome_de_pacote_errado(self):
        data = {
            "name": "titan",
            "packages": [{"name": "Djangfo"}]
        }
        response = self.client.post('http://testserver/api/projects/', data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "One or more packages doesn't exist"})

    def test_requisicao_post_para_criar_projeto_com_pacote_versao_errada(self):
        data = {
            "name": "titan",
            "packages": [{"name": "Django", "version": "5"}]
        }
        response = self.client.post('http://testserver/api/projects/', data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "One or more packages doesn't exist"})

    def test_requisicao_post_para_criar_projeto_com_pacote_vazio(self):
        data = {
            "name": "titan",
            "packages": []
        }
        response = self.client.post('http://testserver/api/projects/', data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "At least one package must exist"})

    def test_requisicao_delete_para_apagar_projeto(self):
        # Cria dados para excluir em seguida.
        data = {
            "name": "titan",
            "packages": [{"name": "Django", "version": "3.2.6"}]
        }
        self.client.post('http://testserver/api/projects/', data=data, format='json')
        response = self.client.delete('http://testserver/api/projects/titan/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_requisicao_delete_com_nome_de_projeto_errado(self):
        response = self.client.delete('http://testserver/api/projects/titan/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
