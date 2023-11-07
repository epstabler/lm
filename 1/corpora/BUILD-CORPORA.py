import sys, re, nltk, pyconll, epitran

EPI_PATH = "/Users/es/.local/src/epitran/"
CEDICT_PATH = EPI_PATH + "cedict_1_0_ts_utf-8_mdbg.txt"

USAGE = """
This code reads specified files from selected nltk- and ud-treebanks,
translates them to ipa, and writes out the results in various formats.

Use:

   python BUILD-CORPORA.py <LANGUAGE1> ... <LANGUAGEn>

where each LANGUAGEi is one of these:

   cmn eng fra hin pol rus spa tha

(those are: Mandarin, English, French, Hindi, Polish, Russian, Spanish, Thai)

Alternatively:

   python BUILD-CORPORA.py all

builds corpora for all 8 languages.

These languages chosen because also covered fairly well by epitran. 
It is easy to extend this script to use additional corpora.

On laptops and other small computers, building these corpora takes some time,
  esp. for the larger ones like eng and cmn ... time for a coffee break.
"""

def cors(lang):
    """ corpora paths for ud + names for nltk """
    if lang == 'cmn':    
        return ['ud-treebanks-v2.12/UD_Chinese-GSD/zh_gsd-ud-train.conllu']
    elif lang == 'eng':
        return ['ud-treebanks-v2.12/UD_English-EWT/en_ewt-ud-train.conllu', 'emma']
    elif lang == 'fra':
        return ['ud-treebanks-v2.12/UD_French-GSD/fr_gsd-ud-train.conllu']
    elif lang == 'hin':
        return ['ud-treebanks-v2.12/UD_Hindi-HDTB/hi_hdtb-ud-train.conllu']
    elif lang == 'pol':
        return ['ud-treebanks-v2.12/UD_Polish-PDB/pl_pdb-ud-train.conllu']
    elif lang == 'rus':
        return ['ud-treebanks-v2.12/UD_Russian-SynTagRus/ru_syntagrus-ud-train.conllu']
    elif lang == 'spa':
        return ['ud-treebanks-v2.12/UD_Spanish-AnCora/es_ancora-ud-train.conllu']
    elif lang == 'tha':
        return ['ud-treebanks-v2.12/UD_Thai-PUD/th_pud-ud-test.conllu']
    else:
        raise ValueError('uds lang name error')

def ep(lang):
    """ epitran models """
    if lang == 'cmn':
        return epitran.Epitran('cmn-Hant', cedict_file=CEDICT_PATH)
    elif lang == 'eng':
        return epitran.Epitran('eng-Latn')
    elif lang == 'fra':
        return epitran.Epitran('fra-Latn')
    elif lang == 'hin':
        return epitran.Epitran('hin-Deva')
    elif lang == 'pol':
        return epitran.Epitran('pol-Latn')
    elif lang == 'rus':
        return epitran.Epitran('rus-Cyrl')
    elif lang == 'spa':
        return epitran.Epitran('spa-Latn')
    elif lang == 'tha':
        return epitran.Epitran('tha-Thai')
    else:
        raise ValueError('Epitran model name error')

def udName(lang, cor):
    """ create simple language-corpus prefix for names of created files """
    if cor == 'emma':                   # nltk corpus
        return 'eng-emma'
    else:                               # UD corpus
        pathParts = cor.split('/')
        udf = pathParts[-1].split('-')
        udfParts = udf[0].split('_')
        if len(udfParts) > 1:
            return '-'.join([lang,udfParts[1]])
        else:
            raise ValueError('UD corpus name format error: %s' % cor)

VERBOSE = False

def adjustTxt(lang, txt):
    """ minor text adjustments, specialized to each corpus,
         since we're interested in pronunciations...
    """
    SET = False
    if lang == 'cmn':
        # replace punctuation with space:
        for ch in ['一', '。', '？', '：', '，', '；', '》', '《',
                   '\)', '\(', '）', '（', '〔', '〕', '！', '$',
                   '\+', '=', '$', '…', '〈', '〉', '“', '\xad', '£', '…',
                   ]:
            txt = re.sub(ch, ' ', txt)
        # and delete all digits:
        txt = re.sub(r'\d', '', txt)
        return txt.strip()

    elif lang == 'eng' or lang == 'emma':
        txt = re.sub(" ' s ", "'s ", txt)   # keep possessive 's attached, for emma
        # fix some (rare) things that might appear in examples
        txt = re.sub('Dr\.', 'Doctor', txt)
        txt = re.sub('&c', 'etcetera', txt) # epitran does not understand "&c", for emma
        txt = re.sub('Mr\.', 'Mister', txt)
        txt = re.sub('Mrs\.', 'Missus', txt)
        txt = re.sub('Ms\.', 'Miz', txt)
        txt = re.sub('@', ' at ', txt)
        txt = re.sub('.com', ' dot com', txt)
        txt = re.sub('.gov', ' dot gov', txt)
        txt = re.sub('.edu', ' dot E D U', txt)
        txt = re.sub('ldd DOC', '', txt)
        for x in ['CNN','GMT','FDR','IBM','ABC','CBS','FBI','USA','LLC','MTM','FYI',
                  'US','DPA','IP','ICDC','LTTE','IB','TNA','OK','CIA','CFC','VOF','DPA',
                  'ISI','JUI','WMD','CPIPPI','FX','NYMEX','EPI','EBS','EBIC','FERC',
                  'ASAP', 'NXNX', 'CD', 'AM', 'PM', 'GDP', 'CEO', 'GE', 'GM', 'EOL',
                  'IAEA', 'EST', 'EDT', 'PDT', 'PST', 'CST', 'CDT', 'PD', 'GOP', 'BS', 
                  'CPI', 'ROI', 'LOI', 'HR', 'ECT', 'CTV', 'TV', 'AK'
                  ]:
            txt = re.sub(x, ' '.join(x), txt)
        txt = re.sub('%', ' percent', txt)
        # delete punctuation:
        for ch in ['`', ';', ':', ',', '!', '\?', '\(', '\)', '"', "\.", '_', '=', '|',
                   "‘", "’", '“', '”', "\#", '&', '/', '\*', '\+', '$M', '$K', '$', '<', '>', ']',
                   '{', '}', '–',  '—', '…', '\xad', 
                   ]:
            txt = re.sub(ch, '', txt)
        # also delete all digits:
        txt = re.sub(r'\d', '', txt)
        # replace with a single space, to maintain word spacing:
        for ch in ['\-\-', '\-',  " '", "' "]:
            txt = re.sub(ch, ' ', txt)
        txt = re.sub(' +', ' ', txt)
        return txt.strip()

    elif lang == 'fra':
        txt = re.sub('Dr\.', 'Doctor', txt)
        for x in ['UE', 'EEUU', 'USA', 'US', 'CSOB', 'PRI', 'OEA', 'INEM',
                  'CCOO', 'EFE', 'OMC', 'CNE', 'FTU', 'CTU'
                  ]:
            txt = re.sub(x, ' '.join(x), txt)
        txt = re.sub('%', ' percent', txt)
        # delete punctuation:
        for ch in ['`', ';', ':', ',', '!', '\?', '\(', '\)', '"', "\.", '_', '=', '|',
                   "‘", "’", '”', "\#", '&', '/', '\*', '\+', '$', '<', '>', ']', '@', '€',
                   '«', '»', '\{', '}', '▶', '£', 
                   ]:
            txt = re.sub(ch, '', txt)
        # also delete all digits:
        txt = re.sub(r'\d', '', txt)
        # replace with a single space, to maintain word spacing:
        for ch in ['\-\-', '\-',  " '", "' "]:
            txt = re.sub(ch, ' ', txt)
        txt = re.sub(' +', ' ', txt)
        return txt.strip()

    elif lang == 'hin':
        # delete punctuation:
        for ch in ['"', '-', ',', '\.', '…', '\?', '!', ':', '।',
                   '\(', '\)', '<', '>', '/',
                   ]:
            txt = re.sub(ch, '', txt)
        # and delete all digits:
        txt = re.sub(r'\d', '', txt)
        return txt.strip()

    elif lang == 'pol':
        # delete punctuation:
        for ch in ['"', '-', ',', '\.', '…', '\?', '!',
                   ':', '•', '`', '_', '>', '<', '≥', '»', '«', '˝',
                   '&','$', '\+', '@', '\[', '\]', '„',
                   '”', "'", "%", "\(", "\)", ';', '/',
                   '̇ ', '–', '̈ ', '̈ ', '°', '_', '\*', 'μ', '○',
                   '’', '“', 
                   ]: 
            txt = re.sub(ch, '', txt)
        # and delete all digits:
        txt = re.sub(r'\d', '', txt)
        return txt.strip()

    elif lang == 'rus':
        # delete punctuation:
        for ch in ['"', '-', ',', '\.', '…', '\?', '!',
                   ':', '№', '£', '&', '\)', '\(', '\xa0',
                   '%', '=', '@', '\*', '΄', '€', '\+', ';',
                   '/', '$', '~', '<', '>',
                   ]:
            txt = re.sub(ch, '', txt)
        # and delete all digits:
        txt = re.sub(r'\d', '', txt)
        return txt.strip()

    elif lang == 'spa':
        for x in ['UE', 'EEUU', 'USA', 'US', 'CSOB', 'PRI', 'OEA', 'INEM',
                  'CCOO', 'EFE', 'OMC', 'CNE', 'FTU', 'CTU'
                  ]:
            txt = re.sub(x, ' '.join(x), txt)
        txt = re.sub('%', ' percent', txt)
        # delete punctuation:
        for ch in ['`', ';', ':', ',', '!', '¡', '\?', '¿', '\(', '\)', '"', "\.", '_', '=', '|',
                   "‘", "’", '”', "\#", '&', '/', '\*', '\+', '$', '<', '>', ']', '@', '€',
                   '〈', '〉', '‧', '…', 'ª'
                   ]:
            txt = re.sub(ch, '', txt)
        # also delete all digits:
        txt = re.sub(r'\d', '', txt)
        # replace with a single space, to maintain word spacing:
        for ch in ['\-\-', '\-',  " '", "' "]:
            txt = re.sub(ch, ' ', txt)
        txt = re.sub(' +', ' ', txt)
        return txt.strip()

    elif lang == 'tha':
        # delete punctuation:
        for ch in ['"', '-', ',', '\.', '…', '\?', '!', ':', '।', '\(', '\)', '<', '>', '/', '“'
                   ]:
            txt = re.sub(ch, '', txt)
        # and delete all digits:
        txt = re.sub(r'\d', '', txt)
        return txt.strip()

    else:
        raise ValueError('adjustText lang error: %s' % lang)

def adjustIPA(ipa):
    """ stylistic adjustments in epitran IPA """
    # represent syllabic r with schwa, as epitran does for syllabic l
    ipa = re.sub('ɹ̩','əɹ',ipa)   # printer -> pɹɪntɹ̩ -> pɹɪntəɹ
    ipa = re.sub('ɻ̩','əɻ',ipa)
    ipa = re.sub('r̩','ər',ipa)
    # remove tie bars
    ipa = re.sub('t͡ʃ','tʃ',ipa)
    ipa = re.sub('t͡s','ts',ipa)
    ipa = re.sub('t͡ɕ','tɕ',ipa)
    ipa = re.sub('ʈ͡ʂ','ʈʂ',ipa)
    ipa = re.sub('t͡ɕ','tɕ',ipa)
    ipa = re.sub('d͡ʒ','dʒ',ipa)
    ipa = re.sub('d͡ʑ','dʑ',ipa)
    ipa = re.sub('d͡z','dz',ipa)
    ipa = re.sub('d͡ʐ','dʐ',ipa)
    ipa = re.sub('d͡s','ds',ipa)
    # adjust epitran representations of some diphthongs
    ipa = re.sub('oj','ɔɪ',ipa)  # boy -> boj -> bɔɪ
    ipa = re.sub('ow','oʊ',ipa)  # home -> howm -> hoʊm
    ipa = re.sub('aw','aʊ',ipa)  # loud -> lawd -> laʊd
    ipa = re.sub('aj','aɪ',ipa)  # lie -> laj -> laɪ
    ipa = re.sub('ej','eɪ',ipa)  # hay -> hej -> heɪ
    return ipa.strip()

def buildCorpus(langs):

    for lang in langs:

        for cor in cors(lang):

            udn = udName(lang, cor)

            print('building %s in various formats...' % udn)
    
            if cor == 'emma':
                corpusListed = nltk.Text(nltk.corpus.gutenberg.sents('austen-emma.txt'))
                corpus = [' '.join(s) for s in corpusListed]
            else:
                corpusListed = pyconll.load_from_file(cor)
                corpus = [sentence.text for sentence in corpusListed]
    
            epi = ep(lang)
        
            ss = open('%s-sentences.txt' % udn, 'w')
        
            ws = open('%s-words.txt' % udn, 'w')
            wsa = open('%s-wordsSpaced.txt' % udn, 'w')
        
            ps = open('%s-ipa.txt' % udn, 'w')
            psa = open('%s-ipaSpaced.txt' % udn, 'w') 
        
            cCnt = 0
    
            for st in corpus:
                # ignore non-content lines
                if not('[' in st) and \
                   not('http' in st) and \
                   not('VOLUME' in st) and \
                   not('CHAPTER' in st):
     
                    ss.write(st)
                    ss.write('\n')
                    if VERBOSE:
                        print('snt =',st)
                    else:
                        cCnt += len(st)
                        sys.stdout.write('\r%d characters processed' % cCnt)
                        sys.stdout.flush()

                    txt = adjustTxt(lang, st)
                    if VERBOSE: print('txt =',txt)
                    ws.write(txt)
                    ws.write('\n')
                    for x in txt:
                        if x != ' ':
                            wsa.write(x)
                            wsa.write(' ')
                        else:
                            wsa.write('_ ')
                    wsa.write('\n')
        
                    ipa = adjustIPA(epi.transliterate(txt))
                    if VERBOSE: print('ipa =',ipa)
                    ps.write(ipa)
                    ps.write('\n')
                    for x in ipa:
                        if x != ' ':
                            psa.write(x)
                            psa.write(' ')
                        else:
                            psa.write('_ ')
                    psa.write('\n')

            sys.stdout.write('\n%s transcription complete\n' % lang)

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print(USAGE)
    elif sys.argv[1:] == ['all']:
        buildCorpus(['cmn', 'eng', 'fra', 'hin', 'pol', 'rus', 'spa', 'tha'])
    else:
        buildCorpus(sys.argv[1:])
