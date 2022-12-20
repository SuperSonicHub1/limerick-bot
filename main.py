import os
from difflib import SequenceMatcher, Match
import discord
from dotenv import load_dotenv
load_dotenv()
from dp.phonemizer import Phonemizer

BOT_TOKEN = os.getenv("BOT_TOKEN")

phonemizer = Phonemizer.from_checkpoint('en_us_cmudict_ipa_forward.pt')

def phonemize(content: str) -> str:
	return '\n'.join([phonemizer(line, lang='en_us') for line in content.replace('.', '').replace(',', '').splitlines()])

def rhymes(first_word: str, second_word: str, match: Match) -> bool:
	return match.size != 0 and first_word[match.a:] == second_word[match.b:]

def is_limerick(content: str):
	phonemized = phonemize(content)
	last_words = [line.split(' ')[-1] for line in phonemized.splitlines()]

	# limerick structure: AABBA

	# AA**A
	first_a_second_a_match = SequenceMatcher(None, last_words[0], last_words[1]).find_longest_match()
	first_a_second_a = rhymes(last_words[0], last_words[1], first_a_second_a_match)

	first_a_third_a_match = SequenceMatcher(None, last_words[0], last_words[4]).find_longest_match()
	first_a_third_a = rhymes(last_words[0], last_words[4], first_a_third_a_match)

	aaa = first_a_second_a and first_a_third_a

	# **BB*
	bb_match = SequenceMatcher(None, last_words[2], last_words[3]).find_longest_match()
	# Match exists and ends of words are the same
	bb = rhymes(last_words[2], last_words[3], bb_match)
	return aaa and bb

class LimerickBot(discord.Client):
	async def on_ready(self):
		print(f'Logged on as {self.user}!')

	async def on_message(self, message: discord.Message):
		channel = message.channel
		author = message.author
		content = message.content

		if author == client.user: return
		if channel.name != 'spam': return

		await channel.send(str(is_limerick(content)))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


client = LimerickBot(intents=intents)
client.run(BOT_TOKEN)
