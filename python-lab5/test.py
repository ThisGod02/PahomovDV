st = "ZpglnRxqenU"
s = list(st.lower())
result = '1' * 12
print(result)
for s1 in s:
    result += s1.upper()
    print(st.lower().find(s1))
    result += s1 ** (int(st.lower().find(s1)) + 1) + '-'