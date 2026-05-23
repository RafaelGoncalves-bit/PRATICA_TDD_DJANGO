from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.forms import DeleteLinkForm, LinkForm, LoginForm
from core.models import LinkModel


class LinkFormTest(TestCase):
    def test_valid_data_creates_link(self):
        form = LinkForm({
            'titulo': 'Teste',
            'link': 'https://example.com',
            'observacao': 'Observação de teste',
        })
        self.assertTrue(form.is_valid())
        link = form.save()
        self.assertEqual(link.titulo, 'Teste')
        self.assertEqual(link.link, 'https://example.com')
        self.assertEqual(link.observacao, 'Observação de teste')

    def test_invalid_url_is_rejected(self):
        form = LinkForm({
            'titulo': 'Teste',
            'link': 'não-é-url',
            'observacao': 'Observação de teste',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('link', form.errors)

    def test_duplicate_link_is_rejected(self):
        LinkModel.objects.create(
            titulo='Existente',
            link='https://example.com',
            observacao='Link já existente',
        )
        form = LinkForm({
            'titulo': 'Teste',
            'link': 'https://example.com',
            'observacao': 'Tentativa duplicada',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('link', form.errors)
        self.assertEqual(form.errors['link'], ['Este link já existe. Não pode ser igual.'])

    def test_duplicate_link_allowed_on_same_instance(self):
        link = LinkModel.objects.create(
            titulo='Existente',
            link='https://example.com',
            observacao='Link já existente',
        )
        form = LinkForm({
            'titulo': 'Existente',
            'link': 'https://example.com',
            'observacao': 'Mesmo link',
        }, instance=link)
        self.assertTrue(form.is_valid())


class DeleteLinkFormTest(TestCase):
    def test_valid_data(self):
        form = DeleteLinkForm({'link_id': 1})
        self.assertTrue(form.is_valid())

    def test_invalid_link_id(self):
        form = DeleteLinkForm({'link_id': 0})
        self.assertFalse(form.is_valid())
        self.assertIn('link_id', form.errors)


class LinkViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='teste@cps.sp.gov.br',
            password='password123',
        )
        self.client.force_login(self.user)

    def test_criar_get_renders_form(self):
        response = self.client.get(reverse('criar'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cadastrar Link')

    def test_criar_post_creates_link_and_redirects(self):
        response = self.client.post(reverse('criar'), {
            'titulo': 'Novo Link',
            'link': 'https://example.com',
            'observacao': 'Link de exemplo',
        })
        self.assertEqual(LinkModel.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('listar'))

    def test_editar_get_renders_form(self):
        link = LinkModel.objects.create(
            titulo='Link Original',
            link='https://original.com',
            observacao='Observação original',
        )
        response = self.client.get(reverse('editar', args=[link.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Salvar')

    def test_editar_post_updates_link(self):
        link = LinkModel.objects.create(
            titulo='Link Original',
            link='https://original.com',
            observacao='Observação original',
        )
        response = self.client.post(reverse('editar', args=[link.id]), {
            'titulo': 'Link Atualizado',
            'link': 'https://updated.com',
            'observacao': 'Observação atualizada',
        })
        link.refresh_from_db()
        self.assertEqual(link.titulo, 'Link Atualizado')
        self.assertEqual(link.link, 'https://updated.com')
        self.assertEqual(link.observacao, 'Observação atualizada')
        self.assertRedirects(response, reverse('listar'))

    def test_excluir_post_deletes_link(self):
        link = LinkModel.objects.create(
            titulo='Link Para Deletar',
            link='https://delete.com',
            observacao='Observação antes de excluir',
        )
        response = self.client.post(reverse('excluir', args=[link.id]), {
            'link_id': link.id,
        })
        self.assertEqual(LinkModel.objects.filter(id=link.id).count(), 0)
        self.assertRedirects(response, reverse('listar'))

    def test_excluir_get_redirects(self):
        link = LinkModel.objects.create(
            titulo='Link Para Deletar',
            link='https://delete.com',
            observacao='Observação antes de excluir',
        )
        response = self.client.get(reverse('excluir', args=[link.id]))
        self.assertRedirects(response, reverse('listar'))


class LoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='loginuser',
            email='user@cps.sp.gov.br',
            password='securepass',
        )

    def test_login_form_valid_credentials(self):
        form = LoginForm({
            'email': 'user@cps.sp.gov.br',
            'password': 'securepass',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.user, self.user)

    def test_login_form_invalid_email_domain(self):
        form = LoginForm({
            'email': 'user@example.com',
            'password': 'securepass',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
