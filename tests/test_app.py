import re
import tempfile
import unittest
from pathlib import Path

from app import create_app


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

        report_response = self.client.get("/relatorios")
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


if __name__ == "__main__":
    unittest.main()
