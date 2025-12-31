import argparse
parser = argparse.ArgumentParser()
parser.add_argument("gff3")
parser.add_argument("fasta")
args = parser.parse_args()


chr_seq = {}
with open(args.fasta) as f2:
    for line in f2:
        line = line.rstrip()
        if line.startswith(">"):
            chr, num = line.split(" ")
            chr = chr.split(">")[1]
            chr_seq[chr] = []
        else:
            chr_seq[chr] += line

pos_lst = []
with open(args.gff3) as f1:
    for line in f1:
        line = line.rstrip()
        line = line.split('\t')
        if line[2] == "CDS":
            chr = line[0]
            start = int(line[3])
            end = int(line[4])
            dir = line[6]
            seq = chr_seq[chr][start-1:end]
            if dir == "-":
                seq = seq[::-1]
                for i in range(len(seq)):
                    if seq[i] == "A":seq[i] = "T"
                    if seq[i] == "T":seq[i] = "A"
                    if seq[i] == "C":seq[i] = "G"
                    if seq[i] == "G":seq[i] = "C"
            print(line[-1], "".join(seq))
                   

    