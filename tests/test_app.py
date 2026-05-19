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
        self.assertIn("R$ 300,00", html)

        token = self.csrf_from(html)
        response = self.client.post("/excluir/1", data={"csrf_token": token}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Curso", response.data.decode())


if __name__ == "__main__":
    unittest.main()
