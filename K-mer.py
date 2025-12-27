import argparse
parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--k", type=int, default=3)
parser.add_argument("--negative", action="store_true")
args = parser.parse_args()


k = args.k

# read file, store seq
seq = []
with open(args.infile) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith(">"):
            continue
        else:
            seq.append(line)
str_seq = "".join(seq)

# positive strand kmer dictionary
p_kmer_pos = {}
for i in range (len(str_seq)+1-k):
    kmer = str_seq[i:i+k]
    if kmer not in p_kmer_pos:
        p_kmer_pos[kmer] = []
    p_kmer_pos[kmer].append(str(i+1))
            

# negative strand kmer dictionary
n_kmer_pos = {}
for kmer in p_kmer_pos:
    # reverse
    rev_kmer = kmer[::-1]
    # complimentss
    rev_comp_kmer = ""
    for nt in rev_kmer:
        if nt == "A":
            rev_comp_kmer += "T"
        elif nt == "T":
            rev_comp_kmer += "A"
        elif nt == "C":
            rev_comp_kmer += "G"
        elif nt == "G":
            rev_comp_kmer += "C"
        else:
            print("unknown nt")
    for p_pos in p_kmer_pos[kmer]:
        if rev_comp_kmer not in n_kmer_pos:
            n_kmer_pos[rev_comp_kmer] = []
        n_kmer_pos[rev_comp_kmer].append(str(-int(p_pos)))

# combine positive negative kmer dictionary
all_kmer_dict = {}
for kmer in p_kmer_pos:
    all_kmer_dict[kmer] = p_kmer_pos[kmer]
for kmer in n_kmer_pos:
    if kmer not in all_kmer_dict:
        all_kmer_dict[kmer] = []
    all_kmer_dict[kmer].extend((n_kmer_pos[kmer]))


# print kmer and position 
if args.negative:
    for kmer in all_kmer_dict:
        pos = all_kmer_dict[kmer]
        print(kmer, " ".join(pos))
else:
    for kmer in p_kmer_pos:
        pos = p_kmer_pos[kmer]
        print(kmer, " ".join(pos))