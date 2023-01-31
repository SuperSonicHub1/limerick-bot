from dp.phonemizer import Phonemizer
import readline
from itertools import chain
from syllabify import Pronunciation

phonemizer = Phonemizer.from_checkpoint('en_us_cmudict_ipa_forward.pt')

def syllable_is_stressed(syllable: str) -> bool:
	"""
	From https://www.poetryfoundation.org/learn/glossary-terms/foot:
	A foot usually contains one stressed syllable and at least one unstressed syllable.
	From https://en.wikipedia.org/wiki/Foot_(prosody)#Classical_meter:
	"stressed" = stressed/long syllable, "short" = unstressed/short syllable 
	"""

	# Does the vowel contain a stress or enlongation?
	return 'ˈ' in syllable or  'ˌ' in syllable or 'ː' in syllable
	# The almost-inverse of this would be
	# Does the vowel contain a shortening? (doesn't handled cases where vowel has no modifications)
	# return 'ˑ' in syllable or '̆' in syllable

def metric_feet(syllables: List[str]) -> int:
  stresses = [syllable_is_stressed(syllable) for syllable in syllable]
  return len(list(filter(bool, stresses)))

def trimeter(syllables: List[str]) -> bool:
  return metric_feet(syllables) % 3 == 0

while True:
	text = input("> ")
	phonemized = [f'/{word}/' for word in phonemizer(text, lang='en_us').split(' ')]
	syllables = list(chain.from_iterable(Pronunciation(word).syllables for word in phonemized))
	print(*syllables, sep='\t')
	print(*[str(syllable_is_stressed(syllable)) for syllable in syllables], sep='\t')
