import argparse
parser = argparse.ArgumentParser()
parser.add_argument("infile1")
parser.add_argument("infile2")
args = parser.parse_args()

lst1 = []
with open (args.infile1) as f1:
    for line in f1:
        line = line.rstrip()
        chr, pos = line.split(":")
        start, end = pos.split("-")
        lst1.append([chr, start, end])
        
lst2 = []
with open (args.infile2) as f2:
    for line in f2:
        line = line.rstrip()
        chr, pos = line.split(":")
        start, end = pos.split("-")
        lst2.append([chr, start, end])

for feature1 in lst1:
    for feature2 in lst2:
        if feature1[0] == feature2[0]:
            if (feature1[1] <= feature2[2]) and (feature2[1] <= feature1[2]):
                print(feature1, "overlaps", feature2)
