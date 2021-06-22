# experiment result

imp = [
    0,
    15.4,
    25,
    50,
    0,
    50,
    27.3,
    10,
    0,
    27.1,
    33.3,
    33.3,
    26.6,
    24.4,
    -8,
    39.9,
    38.7,
    39.9
]

avg_imp = 0
for i in imp:
    avg_imp += i
avg_imp = avg_imp/len(imp)
print('avg_imp', avg_imp)
