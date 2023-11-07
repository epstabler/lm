import sys, re
import matplotlib.pylab as plt

USAGE = """
   python CORPUS-ANALYZE.py x

where x is one of the language file prefixes
listed just below, reports some simple statistics
on the corpus x-y named by x, and writes those
statistics to x-y-stats.txt

For example,

   python CORPUS-ANALYZE.py eng

reads eng-ewt-ipa.txt and
writes stats to eng-ewt-stats.txt

Note that some platforms/editors provide strange
print/screen representations for some of these
characters.
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

def syllabic(c):
    return c in ['a','æ','ã','â','à','ä','ā','å','ą','ậ','á','ɑ','ả', 'ạ', 'ă',
                 'e','ẽ','è','ë','ễ','з','é', 'ɛ', 'ε', 'е', 'ё', '³',
                 'i','ĩ','î','ï','ĭ','ɪ','ı','ī','í','ɨ',
                 'o','õ','़','ॅ','ɔ','ò','ô','ö','œ','ø', 
                 'u','û','ù','ü','ū','ʊ','ʌ','ш', 'ũ', 
                 'ɤ', 'ə'
                 ]

# diacritics
diacritics = ['ː', "'", ' ̩', ' ̤', 'ʰ', ' ̃', ' ̥', ' ̩', ' ̃', '_', ' ̤', ' ̯', '、', '̄',
              '‧', '°', ':', '·', '-', '`', '°', '‧', '^', '|', 'т', '̨', '̧', '̆', '̃', '̥',
              '̤', 'ʲ', '̇', '̀',
              ]

# some diacritics mark tones too, but these are sometimes not next to vowel,
#   so we treat them as distinct symbols
tones = ['「', '」', '『', '』']

# these are output by epitran, but should not count as phonemes
junk = ['~', '・', '─', ',', '.', 
        '曧', '袥', '/', '卧', '坮', '撘', '彝', '鱂', '痹', '\u200b', '$',
        '脱', '鍝', '洒', '櫾',
        'N', 'W', 'C', 'Z', 'X', 'K', 'ō', 'Y', 'S',
        'D', 'G', 'H', 'J', 'R', 'L', 'O', 'E', 'M', 'F', 'U', 'V', 'I'
        '宿', '芦', '慎', '호', '大', '楽', '園', 'ن', 'د', '伎', '火', 'ǩ', 'ك',
        'п', 'ч', '箭', 'ʿ', '上', '성', 'л', '則', '部', 'ا', 
        '胡', '²', '̀', '征', 'ج', '介', '义', '乙', '̉', '粉', '田', '±', '中', '†',
        '济', '̈', 'م', '安', '藩', '̛', '号', 'њ', 'ش', '̂', '′', '长', '—', 'ر',
        '강', '四', '玄', '临', 'о', '́', '規', 'ъ', '町', '−', 'д', 'џ', 'ل', 'º', 
        '井', 'љ', '宮', '宿', 'ذ', '\u200d', 'ऑ', '<', '>', '͡',
        ]

def underscoreSpace(x):
    return re.sub(' ','_',x)

def analyze(lang):
    with open('%s-ipa.txt' % langFilePrefix[lang], 'r') as file:
        langipa = file.read().replace('\n', ' ')

    w = open('%s-stats.txt' % langFilePrefix[lang], 'w')

    ipaSymbols = {}
    for i,x in enumerate(langipa):
        if (i+1)<len(langipa) and langipa[i+1] in diacritics:
            x = x+langipa[i+1]
        if x in ipaSymbols.keys():
            ipaSymbols[x] += 1
        elif not(x in diacritics) and not(x in junk) and not(x in tones):
            ipaSymbols[x] = 1
    
    ipaSymbolsCounts = list(ipaSymbols.items())
    ipaSymbolsCounts.sort(key = lambda x:(-x[1],x[0]))
    
    for o in [w,sys.stdout]:
        o.write('ipa corpus size: %d characters\n' % len([x for x in langipa if x != ' ']))
        o.write('ipa vocabulary size = %d\n' % len(ipaSymbolsCounts))
        o.write('ipa vocabulary (most frequent first) = %s\n' % str(ipaSymbolsCounts))
    
    syll,nonsyll = (0,0)
    syllInThisFile = set([])
    nonsyllInThisFile = set([])
    junkInThisFile = set([])
    for c in langipa:
        if c in junk:
            junkInThisFile.add(c)

        if syllabic(c):
            syllInThisFile.add(c)
            syll += 1

        elif not(c in [' ','\n','\t']) and \
             not(c in diacritics) and \
             not(c in tones) and \
             not(c in junk):
            nonsyllInThisFile.add(c)
            nonsyll += 1

    for o in [w,sys.stdout]:
        o.write('ipa syll = %s\n' % str(syllInThisFile))
        o.write('ipa non-syll = %s\n' % str(nonsyllInThisFile))
        o.write('junk = %s\n' % str(junkInThisFile))
        o.write('occurrences: %d syll, %d non-syll, so %.2f%% syll\n' % (syll, nonsyll, (100.*(syll/(syll+nonsyll)))))

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
        elif not(x in diacritics) and not(x in junk) and not(x in tones):
            ipaBigrams[(prev,x)] += 1
            prev = x 
    ipaBigrams[(prev,' ')] += 1 # count bigram of last character
    
    ipaBigrams = list(ipaBigrams.items())
    ipaBigrams.sort(key=lambda e:(-e[1],e[0])) # sort by most frequent first
    
    n = 10
    for o in [w,sys.stdout]:
        o.write('# of bigrams = %d\n' % len(ipaBigrams))
        o.write('# of zeros = %d\n' % len([x for x in ipaBigrams if x[1] == 0]))
        o.write('%d most common bigrams: %s\n' % (n, str(ipaBigrams[:n])))
    
    w.close()
    sys.exit(0) # comment this line if you want to draw the graphs

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

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print(USAGE)
    analyze(sys.argv[1])
