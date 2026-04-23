const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const ROOT = __dirname;
const DB_PATH = path.join(ROOT, 'comments.db');

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForServer(url, timeoutMs = 15000) {
  const deadline = Date.now() + timeoutMs;
  let lastError;

  while (Date.now() < deadline) {
    try {
      const response = await fetch(url);
      if (response.ok) {
        return;
      }
      lastError = new Error(`Unexpected status: ${response.status}`);
    } catch (error) {
      lastError = error;
    }

    await sleep(300);
  }

  throw lastError || new Error(`Server did not start: ${url}`);
}

function resetDatabase() {
  if (fs.existsSync(DB_PATH)) {
    fs.unlinkSync(DB_PATH);
  }
}

function startNodeProcess(scriptName, extraEnv = {}) {
  const child = spawn(process.execPath, [scriptName], {
    cwd: ROOT,
    env: { ...process.env, ...extraEnv },
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  child.stdout.on('data', (chunk) => {
    process.stdout.write(`[${scriptName}] ${chunk}`);
  });

  child.stderr.on('data', (chunk) => {
    process.stderr.write(`[${scriptName}] ${chunk}`);
  });

  return child;
}

async function stopProcess(child) {
  if (!child || child.killed) {
    return;
  }

  child.kill('SIGTERM');
  await sleep(600);

  if (!child.killed) {
    child.kill('SIGKILL');
  }
}

async function postForm(url, data) {
  const body = new URLSearchParams(data);
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
    redirect: 'manual',
  });
}

async function testVulnerableApp() {
  console.log('\n=== Checking vulnerable_app.js ===');
  resetDatabase();
  const child = startNodeProcess('vulnerable_app.js');

  try {
    await waitForServer('http://127.0.0.1:3000/');

    const config = await fetch('http://127.0.0.1:3000/api/config').then((r) => r.json());
    assert.ok(config.api_key, 'Vulnerable app should expose API key');
    assert.equal(config.debug, true, 'Vulnerable app should expose debug mode');

    const xssPayload = "<script>alert('stored-xss')</script>";
    const postResponse = await postForm('http://127.0.0.1:3000/comment', {
      username: 'attacker',
      comment: xssPayload,
    });
    assert.ok([200, 302].includes(postResponse.status), 'Comment submission should succeed');

    const homePage = await fetch('http://127.0.0.1:3000/').then((r) => r.text());
    assert.ok(homePage.includes(xssPayload), 'Stored XSS payload should remain unescaped');

    console.log('OK: vulnerable app exposes config secret and stores raw XSS payload.');
  } finally {
    await stopProcess(child);
  }
}

async function testSecureApp() {
  console.log('\n=== Checking secure_app.js ===');
  resetDatabase();
  const child = startNodeProcess('secure_app.js', { API_KEY: 'secure-demo-key' });

  try {
    await waitForServer('http://127.0.0.1:3001/');

    const configResponse = await fetch('http://127.0.0.1:3001/api/config');
    const config = await configResponse.json();
    assert.ok(!('api_key' in config), 'Secure app should not expose API key');
    assert.equal(config.status, 'ok', 'Secure app should return healthy config payload');

    const cspHeader = configResponse.headers.get('content-security-policy');
    assert.ok(cspHeader && cspHeader.includes("default-src 'self'"), 'CSP header should be present');

    const invalidSort = await fetch('http://127.0.0.1:3001/api/comments?sort=id DESC');
    assert.equal(invalidSort.status, 400, 'Invalid ORDER BY should be blocked');

    const xssPayload = "<script>alert('stored-xss')</script>";
    const postResponse = await postForm('http://127.0.0.1:3001/comment', {
      username: 'attacker',
      comment: xssPayload,
    });
    assert.ok([200, 302].includes(postResponse.status), 'Secure comment submission should succeed');

    const homePage = await fetch('http://127.0.0.1:3001/').then((r) => r.text());
    assert.ok(!homePage.includes(xssPayload), 'Secure app should not render raw XSS payload');
    assert.ok(
      homePage.includes('&lt;script&gt;alert') || homePage.includes('&amp;lt;script&amp;gt;alert'),
      'Secure app should escape XSS payload'
    );

    console.log('OK: secure app blocks raw XSS rendering, validates sort, and sends CSP.');
  } finally {
    await stopProcess(child);
  }
}

async function main() {
  try {
    await testVulnerableApp();
    await testSecureApp();
    console.log('\nAll Node.js security demo checks passed.');
  } catch (error) {
    console.error('\nSecurity demo failed.');
    console.error(error);
    process.exitCode = 1;
  }
}

main();
