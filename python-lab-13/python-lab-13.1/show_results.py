import json

with open('bandit_before.json') as f:
    d = json.load(f)

print('=== VULNERABLE APP - Bandit Results ===')
for i in d['results']:
    sev = i['issue_severity']
    tid = i['test_id']
    line = i['line_number']
    text = i['issue_text'][:70]
    print(f'[{sev:6}] {tid} line {line}: {text}')

m = d['metrics']['_totals']
high   = m['SEVERITY.HIGH']
medium = m['SEVERITY.MEDIUM']
low    = m['SEVERITY.LOW']
print(f'\nTotals: HIGH={high}, MEDIUM={medium}, LOW={low}')
print()

with open('bandit_after.json') as f:
    d2 = json.load(f)

print('=== SECURE APP - Bandit Results ===')
if not d2['results']:
    print('No issues found!')
for i in d2['results']:
    sev = i['issue_severity']
    tid = i['test_id']
    line = i['line_number']
    text = i['issue_text'][:70]
    print(f'[{sev:6}] {tid} line {line}: {text}')

m2 = d2['metrics']['_totals']
h2 = m2['SEVERITY.HIGH']
me2 = m2['SEVERITY.MEDIUM']
l2 = m2['SEVERITY.LOW']
print(f'\nTotals: HIGH={h2}, MEDIUM={me2}, LOW={l2}')
