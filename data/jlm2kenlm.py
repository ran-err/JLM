from tqdm import tqdm
if __name__ == '__main__':
    with open('test.txt', 'r', encoding='utf-8') as infile, open('test-formated.txt', 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()
        for line in tqdm(lines, total=len(lines)):
            line = [word.split('/')[0] for word in line.split()]
            outfile.write(' '.join(line) + '\n')

