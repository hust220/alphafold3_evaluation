import sys
import re

ct_file = sys.argv[1]
out_file = sys.argv[2]

pair_symbols = [('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]

lines = []
for line in open(ct_file):
    l = re.split('\s+', line.strip())
    if len(l) == 6:
        lines.append(l)

n = len(lines)

#numbers = [int(line[0]) for line in lines]
sequence = [line[1] for line in lines]
#paired_numbers = [int(line[4]) for line in lines]
#names = [line[5] for line in lines]

ss = ['.' for i in range(n)]

pairs = [[int(line[0]), int(line[4])] for line in lines]

ids = []
id2index = {}
for i in range(n):
    a, b = pairs[i]
    ids.append(a)
    id2index[a] = i

def determine_level(ss, a, b):
    if ss[a] != '.' or ss[b] != '.':
        return -1
    level = 0
    while True:
        score = 0
        for i in range(a + 1, b):
            if ss[i] == pair_symbols[level][0]:
                score += 1
            elif ss[i] == pair_symbols[level][1]:
                score -= 1
        if score == 0:
            return level
        level += 1
        if level >= len(pair_symbols):
            return -1

for p in pairs:
    if p[1] != 0:
        i = id2index[p[0]]
        j = id2index[p[1]]

        level = determine_level(ss, i, j)

        if level != -1:
            ss[i] = pair_symbols[level][0]
            ss[j] = pair_symbols[level][1]

f = open(out_file, 'w+')
f.write(''.join(sequence) + '\n')
f.write(''.join(ss) + '\n')
f.close()

