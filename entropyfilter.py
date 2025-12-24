import argparse
import math
parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--window_size", type = int, default = 11)
parser.add_argument("--entropy_threshold", type = float, default = 1.4)
parser.add_argument("--softmask", action="store_true")
args = parser.parse_args()


win_size = args.window_size
entropy_threshold = args.entropy_threshold


# calculate entropy
def entropy (seq):
    count = {}
    for i in seq:
        if i not in count:
            count[i] = 1
        else:
            count[i] += 1
    
    ent = 0
    for i in count:
        p = count[i]/len(seq)
        ent -= p * math.log2(p)
    return ent

# read file
with open (args.infile) as fp:
    seq = []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if seq: 
                seq = "".join(seq)
                # sliding win
                mask = [False] * len(seq)
                for i in range(len(seq)-win_size+1):
                    win_seq = seq[i:i+win_size]
                    ent = entropy(win_seq)
                    if ent < entropy_threshold:
                        for j in range(i, i+win_size):
                            mask[j] = True

                # result
                masked_seq = []
                for i in range(len(seq)):
                    if mask[i] == True:
                        if args.softmask:
                            masked_seq.append(seq[i].lower())
                        else:
                            masked_seq.append('N')
                    else:
                        masked_seq.append(seq[i])
                print(header)
                print("".join(masked_seq))
            header = line
            seq = []
        else:
            seq.append(line)

    if seq: 
        seq = "".join(seq)
        # sliding win
        mask = [False] * len(seq)
        for i in range(len(seq)-win_size+1):
            win_seq = seq[i:i+win_size]
            ent = entropy(win_seq)
            if ent < entropy_threshold:
                for j in range(i, i+win_size):
                    mask[j] = True

        # result
        masked_seq = []
        for i in range(len(seq)):
            if mask[i] == True:
                if args.softmask:
                    masked_seq.append(seq[i].lower())
                else:
                    masked_seq.append('N')
            else:
                masked_seq.append(seq[i])
        print(header)
        print("".join(masked_seq))