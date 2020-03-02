import sys
from lingpy import *
from collections import defaultdict
#from pyclts.transcriptionsystem import TranscriptionSystem
from pyclts import CLTS

clts = CLTS(sys.argv[1])

bipa = clts.transcriptionsystem('bipa')

data = csv2list('characters.tsv')

reps = {
        "P": "P/⁵⁵",
        "R¹": "R¹/²¹⁴",
        "S": "S/³⁵",
        "tʂʰu": "ʈʂʰ u",
        "P²": "P²/⁵⁵",
        "R²": "R²/²¹⁴",
        "eːŋ": "eː ŋ",
        "iauː": "i/j auː",
        "uaiː": "u/w aiː",
        "S²": "S²/³⁵",
        'E': 'ᴇ/ɛ',
        'Q': 'Q/⁵¹',
        'R³': 'R³/²¹⁴',
        "a:": "aː",
        "a:i": "aːi",
        "a:u": "aːu",
        "ai": "ai",
        "au": "au",
        "aʊ": "aʊ",
        "aːʔ": "aː ʔ",
        "e": "e",
        "ei": "ei",
        "eu": "eu",
        #"eːŋ": "eːŋ",
        "i": "i",
        "ia": "i/j a",
        "iai": "i/j ai",
        "iau": "i/j au",
        "ie": "i/j e",
        "ieu": "i/j eu",
        "ii": "i/j i",
        "io": "i/j o",
        "iou": "i/j ou",
        "iu": "i/j u",
        "iæ": "i/j æ",
        "iø": "i/j ø",
        "iøy": "i/j øy",
        "iɑ": "i/j ɑ",
        "iɑu": "i/j ɑu",
        "iɒ": "i/j ɒ",
        "iɔ": "i/j ɔ",
        "iɔi": "i/j ɔi",
        "iɔu": "i/j ɔu",
        "iə": "i/j ə",
        "iəu": "i/j əu",
        "iɛ": "i/j ɛ",
        "iɛu": "i/j ɛu",
        "iɤ": "i/j ɤ",
        "iɤu": "i/j ɤu",
        "iɤɯ": "i/j ɤɯ",
        "iɪ": "i/j ɪ",
        "iɯ": "i/j ɯ",
        "iʊ": "i/j ʊ",
        "iːʔ": "iː ʔ",
        "o": "o",
        "oi": "oi",
        "ou": "ou",
        "u": "u",
        "ua":   "u/w a",
        "ua:":  "u/w a:",
        "ua:i": "u/w a:i",
        "uai":  "u/w ai",
        "uau":  "u/w au",
        "ue":   "u/w e",
        "uei":  "u/w ei",
        "ui":   "u/w i",
        "uo":   "u/w o",
        "uu":   "u/w u",
        "uui":  "u/w ui",
        "uø":   "u/w ø",
        "uɑ":   "u/w ɑ",
        "uɒ":   "u/w ɒ",
        "uɔ":   "u/w ɔ",
        "uə":   "u/w ə",
        "uəi":  "u/w əi",
        "uɛ":   "u/w ɛ",
        "uɛu":  "u/w ɛu",
        "uɤ":   "u/w ɤ",
        "uɪ":   "u/w ɪ",
        "y":  "y",
        "ya": "y/ɥ a",
        "yai":"y/ɥ ai",
        "ye": "y/ɥ e",
        "yei":"y/ɥ ei",
        "yi": "y/ɥ i",
        "yo": "y/ɥ o",
        "yu": "y/ɥ u",
        "yø": "y/ɥ ø",
        "yɔ": "y/ɥ ɔ",
        "yə": "y/ɥ ə",
        "yɛ": "y/ɥ ɛ",
        "yɤ": "y/ɥ ɤ",
        "yɪ": "y/ɥ ɪ",
        "æ": "æ",
        "ø": "ø",
        "øy": "øy",
        "œ": "œ",
        "œy": "œy",
        "ɑ": "ɑ",
        "ɑu": "ɑu",
        "ɒ": "ɒ",
        "ɔ": "ɔ",
        "ɔi": "ɔi",
        "ɔu": "ɔu",
        "ə": "ə",
        "əi": "əi",
        "əu": "əu",
        "ɚ": "ɚ/ə",
        "ɛ": "ɛ",
        "ɛu": "ɛu",
        "ɜ": "ɜ",
        "ɤ": "ɤ",
        "ɤu": "ɤu",
        "ɤɯ": "ɤɯ",
        "ɪ": "ɪ",
        "ɯ": "ɯ",
        "ɵ": "ɵ",
        "ɵy": "ɵy",
        "ɿ": "ɿ",
        "ʅ": "ʅ",
        "ʊ": "ʊ",
        }

vows = defaultdict(int)
bips = defaultdict(int)
D = {0: ['doculect', 'concept', 'value', 'form', 'tokens']}
for i, line in enumerate(data[1:]):

    tokens = line[4].split()
    vowel = False
    ntk = []
    cls = tokens2class(tokens, 'cv')
    for c, t in zip(cls, tokens):
        if c.lower() == 'v':
            if not vowel:
                vowel = True
                ntk += [t]
            else:
                ntk[-1]+= t
        else:
            if vowel:
                vows[ntk[-1]] += 1
                vowel = False
            ntk += [t]
    print(' '.join(ntk))


    tokens = ' '.join([reps.get(x, x) for x in ntk]).split()
    for j, t in enumerate(tokens):
        s = bipa[t]
        if s.type == 'unknownsound':
            bips[t] += 1
        else:
            if '/' in t:
                pre = t.split('/')[0]+'/'
            else:
                pre = ''
            tokens[j] = pre+s.s

    D[i+1] = [line[2], line[0], line[3], line[3],
            tokens]
input()
for bip in bips:
    print('"'+bip+'": "'+bip+'",')
wl = Wordlist(D)
wl.output('tsv', filename='wordlist', ignore='all', prettify=False)
