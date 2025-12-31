import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--skip_non_canonical", action="store_true")
args = parser.parse_args()

pos_lst = []
origin = False
ori_seq = []
with open(args.infile) as f:
    for line in f:
        line = line.strip()
        # build position list
        if line.startswith("gene"):
            line = line.split(" ")[-1]
            if line.startswith("complement"):
                line = line.split("complement")[-1]
                line = line.replace("(", "")
                line = line.replace(")", "")
                start, end = line.split("..")
                pos = [int(start), int(end), "-"]
                pos_lst.append(pos)
            else:
                start, end = line.split("..")
                pos = [int(start), int(end), "+"]
                pos_lst.append(pos)

        # when reach ORIGIN, build 
        elif line.startswith("ORIGIN"):
            origin = True
        elif origin == True:
            line = line.split(" ")
            pos = line[0]
            seq = "".join(line[1:])
            for nt in seq:
                ori_seq.append(nt)


pos_count = []
nt_pos_count = {}
for nt in "ATCG":
    nt_pos_count[nt] = []

for pos in pos_lst:
    start = pos[0]
    end = pos[1]
    dir = pos[2]
    seq = ori_seq[start-1:end]
    if dir == "-":
        seq = seq[::-1]
        for i in range (len(seq)):
            if seq[i] == 'A': seq[i] = 'T'
            if seq[i] == 'T': seq[i] = 'A'
            if seq[i] == 'C': seq[i] = 'G'
            if seq[i] == 'G': seq[i] = 'C'
    
    start_codon = "".join(seq[:3])
    if args.skip_non_canonical and start_codon != "atg":
        continue
    
    # position coverage
    if len(pos_count) == 0:
        pos_count = [1] * len(seq)
    elif len(seq) <= len(pos_count):
        for i in range(len(seq)):
            pos_count[i] += 1
    elif len(seq) > len(pos_count):
        for i in range(len(pos_count)):
            pos_count[i] += 1
        num_new = len(seq) - len(pos_count)
        pos_count.extend([1] * num_new)
    #print(pos_count)

    # count nt occurrance
    # buil enough space
    if len(nt_pos_count['A']) == 0:
        for nt in nt_pos_count:
            nt_pos_count[nt] = [0] * len(seq)
    elif len(seq) > len(nt_pos_count['A']) :
        num_new = len(seq) - len(nt_pos_count['A'])
        for nt in nt_pos_count:
            nt_pos_count[nt].extend([0] * num_new)
    # count nt
    for i in range(len(seq)):
        nt = seq[i].upper()
        nt_pos_count[nt][i] += 1
    
# probability
nt_pos_prob = {}
for nt in "ATCG":
    nt_pos_prob[nt] = []
for nt in "ATCG":
    for i in range(len(nt_pos_count[nt])):
        prob = nt_pos_count[nt][i] / pos_count[i]
        nt_pos_prob[nt].append(round(prob, 3))

json_string = json.dumps(nt_pos_prob)

print(json_string)