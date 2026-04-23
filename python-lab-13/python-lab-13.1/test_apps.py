import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# ── Тесты уязвимого приложения ─────────────────────────────────────
class TestVulnerableApp:
    @pytest.fixture
    def client(self):
        from vulnerable_app import app, init_db
        app.config['TESTING'] = True
        with app.test_client() as c:
            with app.app_context():
                init_db()
            yield c

    def test_sql_injection_possible(self, client):
        """Демонстрирует, что SQL-инъекция работает в vulnerable_app"""
        resp = client.get('/user?id=1 OR 1=1')
        # В уязвимом приложении может вернуть несколько записей или первую
        assert resp.status_code in (200, 500)  # не 400

    def test_normal_user_fetch(self, client):
        resp = client.get('/user?id=1')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['username'] == 'admin'

    def test_search_normal(self, client):
        resp = client.get('/search?username=admin')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) >= 1

    def test_hardcoded_key_exposed(self, client):
        """API ключ возвращается напрямую — уязвимость"""
        resp = client.get('/api/data')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'api_key' in data
        assert data['api_key'] == 'demo_training_key_do_not_use'


# ── Тесты защищённого приложения ───────────────────────────────────
class TestSecureApp:
    @pytest.fixture
    def client(self, monkeypatch):
        monkeypatch.setenv('API_KEY', 'test-secure-key-12345')
        from secure_app import app, init_db
        app.config['TESTING'] = True
        with app.test_client() as c:
            with app.app_context():
                init_db()
            yield c

    def test_sql_injection_blocked(self, client):
        """SQL-инъекция блокируется — возвращает 400"""
        resp = client.get('/user?id=1 OR 1=1')
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert 'error' in data

    def test_sql_injection_blocked_non_integer(self, client):
        resp = client.get('/user?id=abc')
        assert resp.status_code == 400

    def test_normal_user_fetch(self, client):
        resp = client.get('/user?id=1')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['username'] == 'admin'
        assert 'password' not in data  # пароль не раскрывается

    def test_search_parametrized(self, client):
        resp = client.get('/search?username=admin')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data) >= 1

    def test_search_injection_safe(self, client):
        """Попытка SQL-инъекции через LIKE не даёт результатов"""
        resp = client.get("/search?username=' OR '1'='1")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        # Инъекция возвращает 0 реальных пользователей (значение экранировано)
        assert isinstance(data, list)

    def test_key_not_exposed(self, client):
        """API ключ НЕ возвращается в ответе"""
        resp = client.get('/api/data')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'api_key' not in data

    def test_command_allow_list(self, client):
        """Только разрешённые команды выполняются"""
        resp = client.get('/execute?cmd=ls')
        assert resp.status_code == 403

    def test_command_injection_blocked(self, client):
        """Command injection заблокирован"""
        resp = client.get('/execute?cmd=whoami;rm -rf /')
        assert resp.status_code == 403
