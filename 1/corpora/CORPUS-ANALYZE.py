import sys, re
import matplotlib.pylab as plt

USAGE = """
This code reads specified files from the ud-treebanks,
translates them to ipa, and writes out the results in various formats.

Use:

   python CORPUS-ANALYZE.py <LANGUAGE>

where LANGUAGE is one of these:

 cmn eng emma fra hin pol rus spa tha

(those are: Mandarin, English, JaneAustensEnglishNovelEmma, French, Hindi, Polish, Russian, Spanish, Thai)

"""

langFilePrefix = {}
langFilePrefix['cmn'] = 'cmn-gsd'
langFilePrefix['eng'] = 'eng-ewt'
langFilePrefix['emma'] = 'eng-emma'
langFilePrefix['fra'] = 'fra-gsd'
langFilePrefix['hin'] = 'hin-hdtb'
langFilePrefix['pol'] = 'pol-pdb'
langFilePrefix['rus'] = 'rus-syntagrus'
langFilePrefix['spa'] = 'spa-ancora'
langFilePrefix['tha'] = 'tha-pud'

def underscoreSpace(x):
    return re.sub(' ','_',x)

def syllabic(c):
    return c in ['a','æ','ã','â','à','ä','ā','å','ą','ậ',
                 'e','ẽ','è','ë','ễ','з',
                 'i','ĩ','î','ï','ĭ',
                 'o','õ','़','ॅ','ɔ','ò','ô','ö','œ','ø',
                 'u','û','ù','ü','ū',
                 'ɤ',
                 'ə'
                 ]

diacritics = ['ː', "'", ' ̩', ' ̤', 'ʰ', ' ̃', ' ̥', ' ̩', ' ̃', '_', ' ̤', ' ̯', '、']

# some diacritics mark tones too, but these are sometimes not next to vowel,
#   so we treat them as distinct symbols
tones = ['「', '」', '『', '』']

def analyze(lang):
    with open('%s-words.txt' % langFilePrefix[lang], 'r') as file:
        langwords = file.read().replace('\n', ' ')

    with open('%s-ipa.txt' % langFilePrefix[lang], 'r') as file:
        langipa = file.read().replace('\n', ' ')

    ipaSymbols = {}
    for i,x in enumerate(langipa):
        if (i+1)<len(langipa) and langipa[i+1] in diacritics:
            x = x+langipa[i+1]
        if x in ipaSymbols.keys():
            ipaSymbols[x] += 1
        elif not(x in diacritics):
            ipaSymbols[x] = 1
    
    ipaSymbolsCounts = list(ipaSymbols.items())
    ipaSymbolsCounts.sort(key = lambda x:(-x[1],x[0]))
    
    print('\nipa vocabulary size =',len(ipaSymbolsCounts))
    print('\nipa vocabulary (from most to least frequent =\n')
    for pair in ipaSymbolsCounts:
        (x, cnt) = pair
        print('  %s  %d' % (underscoreSpace(x), cnt))
    
    ipaBigrams = {}
    for x in ipaSymbolsCounts:
        for y in ipaSymbolsCounts:
            ipaBigrams[(x[0],y[0])] = 0
    
    prev = ' '
    for i,x in enumerate(langipa):
        if (i+1)<len(langipa) and langipa[i+1] in diacritics:
            x = x+langipa[i+1]
        if x in ipaBigrams.keys():
            ipaBigrams[(prev,x)] += 1
        elif not(x in diacritics):
            ipaBigrams[(prev,x)] += 1
            prev = x 
    ipaBigrams[(prev,' ')] += 1 # count bigram of last character
    
    ipaBigrams = list(ipaBigrams.items())
    ipaBigrams.sort(key=lambda e:(-e[1],e[0])) # sort by most frequent first
    
    print('\n# of bigrams =',len(ipaBigrams))
    print('\n# of zeros =',len([x for x in ipaBigrams if x[1] == 0]))
    print('\nmost common bigrams:')
    for i in ipaBigrams[:20]:
        (x,y) = i[0]
        a = underscoreSpace(x)
        b = underscoreSpace(y)
        cnt = i[1]
        print('    %s %s    %d' % (a,b,cnt) )
    
    # a couple of graphs to show frequency distribution

    ipaBigrams0 = ipaBigrams[:20]
    y = [i[1] for i in ipaBigrams0]
    x = range(len(y))
    plt.plot(x,y)
    plt.title('frequency of top 20 bigrams, in decreasing order')
    labels = [('%s%s' % (underscoreSpace(i[0][0]), underscoreSpace(i[0][1]))) for i in ipaBigrams0]
    plt.xticks(range(len(labels)), labels, rotation=90)
    plt.savefig('%s-freqTop20bigrams.png' % langFilePrefix[lang])
    plt.show()

    ipaBigrams = [x for x in ipaBigrams if x[1] != 0]
    y = [i[1] for i in ipaBigrams]
    x = range(len(y))
    plt.plot(x,y)
    #plt.xscale('log')
    plt.yscale('log')
    plt.title('frequency of bigrams of all %d bigrams, in decreasing order' % len(ipaBigrams))
    plt.savefig('%s-freq%dbigrams.png' % (langFilePrefix[lang],len(ipaBigrams)))
    plt.show()

    print('\nipa:')
    syll,nonsyll = (0,0)
    for c in langipa:
        if syllabic(c):
            syll += 1
        elif c != ' ' and not(c in diacritics) and not(c in tones):
            nonsyll += 1
    print('%d syll, %d non-syll, so %.2f%% syll' % (syll, nonsyll, (100.*(syll/(syll+nonsyll)))))

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print(USAGE)
    analyze(sys.argv[1])
