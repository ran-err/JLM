from tqdm import tqdm

if __name__ == '__main__':
    # with open('r9397.miu.segWithCYHZ.5kk.adddict.ali.txt', 'r', encoding='utf-8') as infile, \
    #      open('pd-miu-train.txt', 'w', encoding='utf-8') as outfile:
    with open('r9397.miu.segWithCYHZ.test2k.ali.txt', 'r', encoding='utf-8') as infile, \
         open('pd-miu-test.txt', 'w', encoding='utf-8') as outfile:
        for line in tqdm(infile.readlines()):
            line: str
            new_line = []
            tokens = line.strip().split()
            tokens = [token.split('_') for token in tokens]
            for pinyin, word in tokens:
                new_line.append(word + '/' + pinyin + '/w')
            outfile.write(' '.join(new_line) + '\n')
