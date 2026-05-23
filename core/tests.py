from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.forms import LinkForm, LoginForm
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
