from pypinyin import lazy_pinyin
from tqdm import tqdm


if __name__ == '__main__':
    with open('train.txt', 'r', encoding='utf-8') as infile, open('train-c.txt', 'w', encoding='utf-8') as outfile:
        for line in tqdm(infile.readlines()):
            line = ''.join([word.split('/')[0] for word in line.split()])
            line = [char + '/' + ''.join(lazy_pinyin(char)) + '/c' for char in line]
            line = ' '.join(line) + '\n'
            outfile.write(line)
