import argparse
parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("k", type=int, default=3)
args = parser.parse_args()

dict = {}

k = args.k
seq = []
with open(args.infile) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith(">"):
            continue
        else:
            seq.append(line)

str_seq = "".join(seq)
for i in range (len(str_seq)+1-k):
    kmer = str_seq[i:i+k]
    if kmer not in dict:
        dict[kmer] = []
    dict[kmer].append(str(i+1))

for kmer in dict:
    pos = dict[kmer]
    print(kmer, " ".join(pos))
            
