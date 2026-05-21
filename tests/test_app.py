import re
import tempfile
import unittest
from pathlib import Path

from app import create_app
from app.repositories.user_repository import UserRepository


class SubscriptionAppTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "DATABASE": str(Path(self.temp_dir.name) / "test.sqlite3"),
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def csrf_from(self, html: str) -> str:
        return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)

    def register_user(self, email: str = "ana@example.com", nome: str = "Ana"):
        page = self.client.get("/cadastro").data.decode()
        return self.client.post(
            "/cadastro",
            data={
                "csrf_token": self.csrf_from(page),
                "nome": nome,
                "email": email,
                "senha": "Segredo1!",
                "confirmar_senha": "Segredo1!",
            },
            follow_redirects=True,
        )

    def login_user(self, email: str = "ana@example.com", senha: str = "Segredo1!"):
        page = self.client.get("/login").data.decode()
        return self.client.post(
            "/login",
            data={"csrf_token": self.csrf_from(page), "email": email, "senha": senha},
            follow_redirects=True,
        )

    def logout_user(self):
        page = self.client.get("/").data.decode()
        return self.client.post("/logout", data={"csrf_token": self.csrf_from(page)}, follow_redirects=True)

    def create_subscription(self, **overrides):
        new_page = self.client.get("/nova").data.decode()
        data = {
            "csrf_token": self.csrf_from(new_page),
            "nome": "Assinatura teste",
            "valor": "10",
            "frequencia": "mensal",
            "vencimento": "10",
            "categoria": "outros",
            "divisao": "1",
            "ativo": "on",
        }
        data.update(overrides)
        return self.client.post("/nova", data=data, follow_redirects=True)

    def test_crud_and_summary_calculation(self):
        self.register_user()
        new_page = self.client.get("/nova").data.decode()
        token = self.csrf_from(new_page)

        response = self.client.post(
            "/nova",
            data={
                "csrf_token": token,
                "nome": "Netflix",
                "valor": "55.90",
                "frequencia": "mensal",
                "vencimento": "15",
                "categoria": "streaming",
                "divisao": "2",
                "ativo": "on",
            },
            follow_redirects=True,
        )

        html = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Netflix", html)
        self.assertIn("R$ 27,95", html)
        self.assertIn('id="filter-categoria"', html)
        self.assertIn('id="filter-frequencia"', html)
        self.assertIn('data-categoria="streaming"', html)
        self.assertIn('data-frequencia="mensal"', html)
        self.assertIn("Ações de Netflix", html)
        self.assertIn("Duplicar", html)
        self.assertIn('id="theme-toggle"', html)
        self.assertIn('data-theme="dark"', html)

        edit_page = self.client.get("/editar/1").data.decode()
        token = self.csrf_from(edit_page)
        response = self.client.post(
            "/editar/1",
            data={
                "csrf_token": token,
                "nome": "Curso",
                "valor": "1200",
                "frequencia": "anual",
                "vencimento": "20",
                "categoria": "educação",
                "divisao": "4",
                "ativo": "on",
            },
            follow_redirects=True,
        )

        html = response.data.decode()
        self.assertIn("Curso", html)
        self.assertIn("R$ 25,00", html)
        self.assertIn("R$ 1.200,00", html)
        self.assertIn("Total real mensal", html)
        self.assertIn("Assinaturas inativas", html)
        self.assertIn("Nenhuma assinatura inativa.", html)

        token = self.csrf_from(html)
        response = self.client.post("/excluir/1", data={"csrf_token": token}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        html = response.data.decode()
        self.assertIn("Assinatura marcada como inativa.", html)
        self.assertIn("Curso", html)
        self.assertIn("Reativar", html)
        self.assertIn("Nenhuma assinatura ativa cadastrada.", html)
        self.assertIn("R$ 0,00", html)

        token = self.csrf_from(html)
        response = self.client.post("/reativar/1", data={"csrf_token": token}, follow_redirects=True)

        html = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Assinatura reativada com sucesso.", html)
        self.assertIn('data-categoria="educação"', html)
        self.assertIn("Nenhuma assinatura inativa.", html)

        token = self.csrf_from(html)
        response = self.client.post("/duplicar/1", data={"csrf_token": token}, follow_redirects=True)

        html = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Assinatura duplicada com sucesso.", html)
        self.assertIn("Curso (copia)", html)

    def test_example_subscriptions_with_monthly_annual_and_splits(self):
        self.register_user()
        examples = [
            {
                "nome": "Spotify",
                "valor": "20",
                "frequencia": "mensal",
                "vencimento": "5",
                "categoria": "streaming",
                "divisao": "1",
            },
            {
                "nome": "Netflix Familia",
                "valor": "60",
                "frequencia": "mensal",
                "vencimento": "12",
                "categoria": "streaming",
                "divisao": "3",
            },
            {
                "nome": "Curso Online",
                "valor": "1200",
                "frequencia": "anual",
                "vencimento": "20",
                "categoria": "educação",
                "divisao": "1",
            },
            {
                "nome": "Antivirus",
                "valor": "240",
                "frequencia": "anual",
                "vencimento": "25",
                "categoria": "outros",
                "divisao": "4",
            },
        ]

        for example in examples:
            response = self.create_subscription(**example)
            self.assertEqual(response.status_code, 200)

        html = response.data.decode()
        self.assertIn("Spotify", html)
        self.assertIn("Netflix Familia", html)
        self.assertIn("Curso Online", html)
        self.assertIn("Antivirus", html)

        self.assertIn("R$ 20,00", html)
        self.assertIn("R$ 100,00", html)
        self.assertIn("R$ 5,00", html)

        self.assertIn("R$ 145,00", html)

        report_response = self.client.get("/dashboard")
        report_html = report_response.data.decode()

        self.assertEqual(report_response.status_code, 200)
        self.assertIn("Análise das suas assinaturas", report_html)
        self.assertIn("Distribuição por categoria", report_html)
        self.assertIn("Vencimentos nos próximos 7 dias", report_html)
        self.assertIn("Maiores custos reais", report_html)
        self.assertIn("R$ 200,00", report_html)
        self.assertIn("R$ 145,00", report_html)
        self.assertIn("R$ 2.400,00", report_html)
        self.assertIn("R$ 1.740,00", report_html)

    def test_post_routes_require_csrf(self):
        self.register_user()
        self.create_subscription(nome="CSRF teste")

        post_routes = [
            ("/nova", {}),
            (
                "/editar/1",
                {
                    "nome": "Sem CSRF",
                    "valor": "10",
                    "frequencia": "mensal",
                    "vencimento": "10",
                    "categoria": "outros",
                    "divisao": "1",
                    "ativo": "on",
                },
            ),
            ("/excluir/1", {}),
            ("/duplicar/1", {}),
            ("/reativar/1", {}),
        ]

        for path, data in post_routes:
            with self.subTest(path=path):
                response = self.client.post(path, data=data)
                self.assertEqual(response.status_code, 400)

    def test_auth_post_routes_require_existing_csrf_token(self):
        post_routes = [
            ("/cadastro", {"nome": "Sem token", "email": "sem-token@example.com", "senha": "Segredo1!"}),
            ("/login", {"email": "ana@example.com", "senha": "Segredo1!"}),
            ("/logout", {}),
        ]

        for path, data in post_routes:
            with self.subTest(path=path):
                response = self.client.post(path, data=data)
                self.assertEqual(response.status_code, 400)

    def test_invalid_form_displays_validation_errors(self):
        self.register_user()
        new_page = self.client.get("/nova").data.decode()
        response = self.client.post(
            "/nova",
            data={
                "csrf_token": self.csrf_from(new_page),
                "nome": "",
                "valor": "abc",
                "frequencia": "semanal",
                "vencimento": "40",
                "categoria": "lazer",
                "divisao": "0",
                "ativo": "on",
            },
        )

        html = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Informe o nome da assinatura.", html)
        self.assertIn("Informe um valor numérico válido.", html)
        self.assertIn("Escolha uma frequencia valida.", html)
        self.assertIn("Informe um dia entre 1 e 31.", html)
        self.assertIn("Escolha uma categoria valida.", html)
        self.assertIn("A divisão deve ser no mínimo 1.", html)

    def test_subscription_form_rejects_oversized_and_non_finite_values(self):
        self.register_user()

        invalid_cases = [
            ({"nome": "A" * 121}, "O nome deve ter no máximo 120 caracteres."),
            ({"valor": "NaN"}, "Informe um valor numérico válido."),
            ({"valor": "Infinity"}, "Informe um valor numérico válido."),
            ({"valor": "1000000.01"}, "Informe um valor de até R$ 1.000.000,00."),
            ({"divisao": "1001"}, "A divisão deve ser no máximo 1000."),
        ]

        for overrides, expected_message in invalid_cases:
            with self.subTest(overrides=overrides):
                response = self.create_subscription(**overrides)
                html = response.data.decode()
                self.assertEqual(response.status_code, 200)
                self.assertIn(expected_message, html)

    def test_missing_subscription_post_routes_return_404(self):
        self.register_user()
        new_page = self.client.get("/nova").data.decode()
        token = self.csrf_from(new_page)

        for path in ["/excluir/999", "/reativar/999", "/duplicar/999"]:
            with self.subTest(path=path):
                response = self.client.post(path, data={"csrf_token": token})
                self.assertEqual(response.status_code, 404)

    def test_duplicate_inactive_subscription_stays_inactive(self):
        self.register_user()
        self.create_subscription(nome="Antigo", valor="24", frequencia="mensal")
        html = self.client.get("/").data.decode()
        token = self.csrf_from(html)

        response = self.client.post("/excluir/1", data={"csrf_token": token}, follow_redirects=True)
        html = response.data.decode()
        token = self.csrf_from(html)

        response = self.client.post("/duplicar/1", data={"csrf_token": token}, follow_redirects=True)
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Antigo (copia)", html)
        self.assertIn("2 inativas", html)
        self.assertIn("Nenhuma assinatura ativa cadastrada.", html)

    def test_register_login_logout_and_password_hash(self):
        response = self.register_user(email="maria@example.com", nome="Maria")
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cadastro realizado com sucesso.", html)
        self.assertIn("Olá, Maria", html)
        self.assertIn("Dashboard", html)
        self.assertIn("Análise das suas assinaturas", html)

        with self.app.app_context():
            user = UserRepository().get_by_email("maria@example.com")

        self.assertIsNotNone(user)
        self.assertNotEqual(user.password_hash, "Segredo1!")
        self.assertTrue(user.password_hash.startswith("scrypt:"))

        response = self.logout_user()
        html = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Você saiu da sua conta.", html)
        self.assertIn("Entrar na conta", html)

        response = self.login_user(email="maria@example.com", senha="senha-errada")
        self.assertIn("E-mail ou senha inválidos.", response.data.decode())

        response = self.login_user(email="maria@example.com")
        html = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login realizado com sucesso.", html)
        self.assertIn("Olá, Maria", html)
        self.assertIn("Dashboard", html)
        self.assertIn("Análise das suas assinaturas", html)

    def test_register_requires_strong_password(self):
        weak_passwords = [
            ("segredo1!", "sem maiúscula"),
            ("SEGREDO1!", "sem minúscula"),
            ("Segredo1", "sem caractere especial"),
            ("Segredo1 ", "espaco nao conta como especial"),
            ("Se1!", "curta demais"),
        ]

        for password, reason in weak_passwords:
            with self.subTest(reason=reason):
                page = self.client.get("/cadastro").data.decode()
                response = self.client.post(
                    "/cadastro",
                    data={
                        "csrf_token": self.csrf_from(page),
                        "nome": "Teste",
                        "email": f"{reason.replace(' ', '-')}@example.com",
                        "senha": password,
                        "confirmar_senha": password,
                    },
                )
                html = response.data.decode()
                self.assertEqual(response.status_code, 200)
                self.assertIn("A senha deve ter pelo menos 6 caracteres", html)

        response = self.register_user(email="forte@example.com", nome="Forte")
        self.assertIn("Cadastro realizado com sucesso.", response.data.decode())

    def test_register_and_login_validate_email_format(self):
        invalid_emails = [
            "texto-sem-email",
            "usuario@",
            "@example.com",
            "usuario@example",
            "usuario example@example.com",
            "usuario@example..com",
        ]

        for email in invalid_emails:
            with self.subTest(route="cadastro", email=email):
                page = self.client.get("/cadastro").data.decode()
                response = self.client.post(
                    "/cadastro",
                    data={
                        "csrf_token": self.csrf_from(page),
                        "nome": "Email inválido",
                        "email": email,
                        "senha": "Segredo1!",
                        "confirmar_senha": "Segredo1!",
                    },
                )
                html = response.data.decode()
                self.assertEqual(response.status_code, 200)
                self.assertIn("Informe um e-mail válido.", html)

            with self.subTest(route="login", email=email):
                page = self.client.get("/login").data.decode()
                response = self.client.post(
                    "/login",
                    data={"csrf_token": self.csrf_from(page), "email": email, "senha": "Segredo1!"},
                )
                html = response.data.decode()
                self.assertEqual(response.status_code, 200)
                self.assertIn("Informe um e-mail válido.", html)

    def test_register_template_has_email_suggestion_and_password_confirmation_feedback(self):
        html = self.client.get("/cadastro").data.decode()

        self.assertIn("email-domain-suggestion", html)
        self.assertIn("gmail.com", html)
        self.assertIn("password-match-feedback", html)
        self.assertIn("As senhas conferem.", html)

    def test_register_rejects_duplicate_and_oversized_credentials(self):
        self.register_user(email="duplicado@example.com", nome="Primeiro")
        self.logout_user()

        response = self.register_user(email="DUPLICADO@example.com", nome="Segundo")
        html = response.data.decode()
        self.assertIn("Este e-mail já está cadastrado.", html)
        self.assertNotIn("Olá, Segundo", html)

        page = self.client.get("/cadastro").data.decode()
        response = self.client.post(
            "/cadastro",
            data={
                "csrf_token": self.csrf_from(page),
                "nome": "A" * 121,
                "email": ("a" * 245) + "@example.com",
                "senha": "A" + ("a" * 127) + "!",
                "confirmar_senha": "A" + ("a" * 127) + "!",
            },
        )
        html = response.data.decode()
        self.assertIn("O nome deve ter no máximo 120 caracteres.", html)
        self.assertIn("O e-mail deve ter no máximo 254 caracteres.", html)
        self.assertIn("A senha deve ter no máximo 128 caracteres.", html)

    def test_login_rejects_sql_injection_style_payload(self):
        self.register_user(email="seguro@example.com", nome="Seguro")
        self.logout_user()

        response = self.login_user(email="' OR 1=1 --", senha="' OR 1=1 --")
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Informe um e-mail válido.", html)
        self.assertNotIn("Olá, Seguro", html)

    def test_session_cookie_security_flags_are_configured(self):
        self.assertTrue(self.app.config["SESSION_COOKIE_HTTPONLY"])
        self.assertEqual(self.app.config["SESSION_COOKIE_SAMESITE"], "Lax")
        self.assertEqual(self.app.config["PERMANENT_SESSION_LIFETIME"].total_seconds(), 28800)

    def test_security_headers_are_set(self):
        response = self.client.get("/login")

        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertEqual(response.headers["Referrer-Policy"], "strict-origin-when-cross-origin")
        self.assertIn("camera=()", response.headers["Permissions-Policy"])

    def test_production_requires_real_secret_key(self):
        with self.assertRaises(RuntimeError):
            create_app(
                {
                    "TESTING": True,
                    "APP_ENV": "production",
                    "DATABASE": str(Path(self.temp_dir.name) / "prod.sqlite3"),
                }
            )

    def test_protected_pages_redirect_to_login_when_anonymous(self):
        for path in ["/", "/dashboard", "/relatorios", "/nova", "/editar/1"]:
            with self.subTest(path=path):
                response = self.client.get(path, follow_redirects=False)
                self.assertEqual(response.status_code, 302)
                self.assertIn("/login", response.headers["Location"])

    def test_dashboard_navigation_and_sidebar_controls(self):
        self.register_user()

        response = self.client.get("/relatorios", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.headers["Location"])

        dashboard_html = self.client.get("/dashboard").data.decode()
        self.assertIn("Dashboard", dashboard_html)
        self.assertIn('id="sidebar-collapse-toggle"', dashboard_html)
        self.assertIn("subscription-sidebar", dashboard_html)
        self.assertIn("Recolher menu lateral", dashboard_html)
        self.assertIn("Sair", dashboard_html)
        self.assertNotIn(">Painel<", dashboard_html)

    def test_users_only_see_their_own_subscriptions(self):
        self.register_user(email="ana@example.com", nome="Ana")
        self.create_subscription(nome="Netflix Ana", categoria="streaming")
        self.logout_user()

        self.register_user(email="bia@example.com", nome="Bia")
        self.create_subscription(nome="Spotify Bia", categoria="streaming")

        html = self.client.get("/").data.decode()
        self.assertIn("Spotify Bia", html)
        self.assertNotIn("Netflix Ana", html)

        token = self.csrf_from(html)
        for path in ["/editar/1", "/excluir/1", "/duplicar/1", "/reativar/1"]:
            with self.subTest(path=path):
                if path.startswith("/editar"):
                    response = self.client.get(path)
                else:
                    response = self.client.post(path, data={"csrf_token": token})
                self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
