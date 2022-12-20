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

def rhymes(first_word: str, second_word: str) -> bool:
	# Reverse words like in rhyming dictionaries to emphazise matches of endings 
	match = SequenceMatcher(None, first_word[::-1], second_word[::-1]).find_longest_match()

	# Match exists and ends of words are the same
	return match.size != 0 and match.a == 0 and match.b == 0

def is_limerick(content: str):
	phonemized = phonemize(content)
	last_words = [line.split(' ')[-1] for line in phonemized.splitlines()]

	# limerick structure: AABBA

	# AA**A
	first_a_second_a = rhymes(last_words[0], last_words[1])
	first_a_third_a = rhymes(last_words[0], last_words[4])
	aaa = first_a_second_a and first_a_third_a

	# **BB*
	bb_match = SequenceMatcher(None, last_words[2], last_words[3]).find_longest_match()
	bb = rhymes(last_words[2], last_words[3])
	
	return (aaa and bb, (first_a_second_a, first_a_third_a, bb), [line.split(' ')[-1] for line in phonemized.splitlines()])

def bool_to_emoji(truth: bool) -> str:
	return ':white_check_mark:' if truth else ':x:'

def format_lint(section: str, rhymes: bool, pronunciations: list[str]) -> str:
	return f"`{section}`: {bool_to_emoji(rhymes)} ({', '.join(pronunciations)})"

class LimerickBot(discord.Client):
	async def on_ready(self):
		print(f'Logged on as {self.user}!')

	async def on_message(self, message: discord.Message):
		channel = message.channel
		author = message.author
		content = message.content

		if author == client.user: return
		if channel.name != 'spam': return

		limerick, (first_a_second_a, first_a_third_a, bb), last_words = is_limerick(content)
		if limerick:
			msg = "You've got a limerick!"
		else:
			msg = '\n'.join([
				format_lint('AA___', first_a_second_a, last_words[0:2]),
				format_lint('A___A', first_a_third_a, [last_words[0], last_words[4]]),
				format_lint('__BB_', bb, last_words[2:4]),
			])

		await channel.send(msg)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


client = LimerickBot(intents=intents)
client.run(BOT_TOKEN)
