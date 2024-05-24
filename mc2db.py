import sys
import re
import os
import subprocess
from tqdm import tqdm

pair_symbols = [('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]

def parse_mc_annotate(file_path):
    """Parse mc-annotate output file."""
    stacking_pairs = []
    base_pairs = []

    ires = 0
    residues = []
    residue_ids = dict()
    bps = []
    chains = []
    chain_lengths = dict()
    seq = []
    section = ''
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.endswith('----'):
                ind = line.find(' ---')
                section = line[:ind]
            elif section == 'Residue conformations':
                l = re.split('\s+', line.strip())
                res_name = l[0]
                chain = res_name[0]
                res_type = l[2]
                if res_type in ['A', 'U', 'G', 'C']:
                    if chain not in chain_lengths:
                        chains.append(chain)
                        chain_lengths[chain] = 0
                    chain_lengths[chain] += 1
                    residues.append(res_name)
                    residue_ids[res_name] = ires
                    seq.append(res_type)
                    ires += 1
            elif line != '' and section == 'Base-pairs':
                l = re.split('\s+', line.strip())
                bp_type = l[3]
                if bp_type in ['Ww/Ww', 'Ww/Ws', 'Ws/Ww']:
                    r1, r2 = l[0].split('-')
                    if r1 in residue_ids and r2 in residue_ids:
                        i1 = residue_ids[r1]
                        i2 = residue_ids[r2]
                        bps.append([i1,i2])
    return len(residues), bps, ''.join(seq), [chain_lengths[c] for c in chains]

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

def bps2db(n, bps):
    ss = ['.' for i in range(n)]
    for i,j in bps:
        level = determine_level(ss, i, j)
        if level != -1:
            ss[i] = pair_symbols[level][0]
            ss[j] = pair_symbols[level][1]
    return ss

def add_chain_breaks(chain_lengths, s):
    chains = []
    i = 0
    for chain_length in chain_lengths:
        chain = ''
        for _ in range(chain_length):
            chain += s[i]
            i += 1
        chains.append(chain)
    return ' '.join(chains)


mc_dir = "rna_only"
mc_files = [f for f in os.listdir(mc_dir) if f.endswith(".info")]
for mc_file in tqdm(mc_files):
    input_file = os.path.join(mc_dir, mc_file)
    output_file = input_file.replace(".info", ".db")
    n, bps, seq, chain_lengths = parse_mc_annotate(input_file)
    db = bps2db(n, bps)
    f = open(output_file, 'w+')
    f.write(add_chain_breaks(chain_lengths, seq))
    f.write('\n')
    f.write(add_chain_breaks(chain_lengths, db))
    f.close()

print("All MC-Annotate files have been processed.")



