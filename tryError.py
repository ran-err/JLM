if __name__ == '__main__':
    with open('tryError.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            tokens = line.strip().split(' ')
            readings = []
            for x in tokens:
                if x.split('/')[1] != '':
                    s = x.split('/')[1]
                else:
                    s = x.split('/')[0]
                readings.append(s)

            #readings = ''.join([x.split('/')[1] if x.split('/')[1] != '' else x.split('/')[0] for x in tokens])
