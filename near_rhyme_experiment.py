from difflib import SequenceMatcher
from dp.phonemizer import Phonemizer

phonemizer = Phonemizer.from_checkpoint('en_us_cmudict_ipa_forward.pt')

# https://poemanalysis.com/definition/imperfect-rhyme/
# https://en.wikipedia.org/wiki/Perfect_and_imperfect_rhymes#Imperfect_rhyme
near_rhymes = (
	('queen', 'regime'),
	('pay', 'age'),
	('prosperous', 'hostages'),
	('prosperous', 'just'),
	('Love', 'move'),
	('Mom', 'plum'),
	('Bridge', 'fudge'),
	('boil', 'bubble'),
	('sting', 'dog'),
	('mouth', 'out'),
)

print_tab = lambda *args, **kwargs: print(*args, **kwargs, sep='\t')

print_tab('Left', 'Right', 'Ratio')
for left_word, right_word in near_rhymes:
	left_phones = phonemizer(left_word, lang='en_us')
	right_phones = phonemizer(right_word, lang='en_us')
	ratio = SequenceMatcher(None, left_phones, right_phones).ratio()
	print_tab(left_word, right_word)
	print_tab(left_phones, right_phones, ratio)
