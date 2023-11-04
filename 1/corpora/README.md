# 1 Supplemental: Building some IPA corpora

## 1.1. Jane Austen's *Emma*

The [Gutenberg version of Emma](https://www.gutenberg.org/ebooks/158)
is available as part of the [NLTK](https://www.nltk.org/) 
[corpora](https://www.nltk.org/howto/corpus.html).

NLTK also parses the novel into sentences for us.

```
> pip install nltk
> python -m nltk.downloader gutenberg
```

## 1.2 UD corpora
Sentences are collected from Version 2.12 of the
[Universal Dependencies](https://universaldependencies.org/) corpora,
available [here](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5150).

Unpack ud-treebanks-v2.12.tgz in this directory:

```
> wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-5150/ud-treebanks-v2.12.tgz
> tar xvzf ud-treebanks-v2.12.tgz
> rm ud-treebanks-v2.12.tgz
```

Probably, more recent versions of the UD treebanks will work just as well.

We use the python package piconll to access the treebank files.

```
> pip install piconll
```

Files in this directory show how corpora were prepared in these languages,
all of which are also handled by Epitran (described just below).

* cmn Mandarin
* eng English
* fra French
* hin Hindi
* pol Polish
* rus Russian
* spa Spanish
* tha Thai

For each corpus *, several formats are saved:

* `*-words.txt` has 1 sentence per line, removing punctuation except possessive 's

* `*-ipa.txt` has ipa transcriptions of the same lines

* `*-ipaSpaced.txt` puts spaces between the ipa characters

## 1.3 IPA transcription
[Epitran](https://github.com/dmort27/epitran), presented by
[Mortensen, Dalmia & Littell (2018)](https://aclanthology.org/L18-1429/),
was used to obtain IPA transcriptions.

Installation instructions are provided on the 
[epitran](https://github.com/dmort27/epitran) website, including
the instructions about getting Flite for English transcriptions, and
getting the Chinese dictionary.

Of course, ongoing research aims to improve the accuracy of epitran-like
tools and to extend them to more languages. See e.g.
[Hasegawa&al 2020](https://link.springer.com/chapter/10.1007/978-3-030-59430-5_1),
[Yu&al 2020](https://ieeexplore.ieee.org/abstract/document/9054696),
[Li&al 2020](https://ojs.aaai.org/index.php/AAAI/article/view/6341),
[Li&al 2021](https://www.cs.cmu.edu/~awb/papers/li21f_interspeech.pdf),
[Li&al 2022](https://aclanthology.org/2022.findings-acl.166/),
[Manohar&al 2022](https://ieeexplore.ieee.org/abstract/document/9877808),
[Salesky&al 2020](https://arxiv.org/abs/2005.13962),
[Ahn&al 2022](https://aclanthology.org/2022.lrec-1.566/),
[Cao&al 2023](https://www.mdpi.com/2076-3417/13/16/9408)
