from tqdm import tqdm
import time
import re

if __name__ == '__main__':
    # 由3-gram文件生成2-gram和1-gram文件
    # gram = ['', 'fake-1-gram.arpa', 'fake-2-gram.arpa', 'fake-3-gram.arpa']  # 表示n-gram文件名称
    # gram = ['', 'zhwiki-split-miu-1.arpa', 'zhwiki-split-miu-2.arpa', 'zhwiki-split-miu-3.arpa']
    gram = ['', '20220525125620-1.arpa', '20220525125620-2.arpa', '20220525125620-3.arpa']
    flag = [True, True, True]  # 表示当前内容是否属于n-gram
    with open(gram[3], 'r', encoding='utf-8') as infile, \
         open(gram[2], 'w', encoding='utf-8') as out2, \
         open(gram[1], 'w', encoding='utf-8') as out1:
        for line in tqdm(infile.readlines()):
            if flag[1]:
                if re.match('^ngram 2=.*', line) or re.match('^ngram 3=.*', line):
                    pass
                elif line == '\\2-grams:\n':
                    flag[1] = False
                else:
                    out1.write(line)

            if flag[2]:
                if re.match('^ngram 3=.*', line):
                    pass
                elif line == '\\3-grams:\n':
                    break
                    # flag[2] = False
                else:
                    out2.write(line)

        out1.write('\\end\\\n')
        out2.write('\\end\\\n')
