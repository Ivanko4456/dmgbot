import json
import os.path
import discord
from discord.ext import commands

with open("config.json", "r") as cfgfile:
	cfg = json.load(cfgfile)
	

class DMGbot(commands.Bot):
	
	def __init__(self):
		super().__init__(command_prefix='', intents=discord.Intents.default())
		
		self._dmgs: dict[str, int]
		
		# creating dmg.json if it doesn't exist
		if not os.path.exists('dmg.json'):
			with open('dmg.json', 'w') as file:
				file.write('{}')
				
		@self.tree.command(name=cfg["add_damage_command_name"], description=cfg["add_damage_command_description"])
		async def add_dmg_func(interaction, dmg: str):
			self._dmgs = self.parse_file()
			na = interaction.user.nick if interaction.user.nick is not None else interaction.user.name
			dm = self.normalizer(dmg)
			if na in self._dmgs:
				if int(self._dmgs[na]) < dm:
					
					with open("dmg.json", "r") as jsonFile:
						data = json.load(jsonFile)
					data[na] = dm
					with open("dmg.json", "w") as jsonFile:
						json.dump(data, jsonFile)
					
					return await interaction.response.send_message(f'✅{na}: {self.denormalizer(dm)}')
				else:
					return await interaction.response.send_message\
							(f'❌Предыдущая запись больше: {na}: {self.denormalizer(self._dmgs[na])}')
			
			with open("dmg.json", "r") as jsonFile:
				data = json.load(jsonFile)
			data[na] = dm
			with open("dmg.json", "w") as jsonFile:
				json.dump(data, jsonFile)
			
			return await interaction.response.send_message(f'✅{na}: {self.denormalizer(dm)}')
		
		@self.tree.command(name=cfg["get_gamage_command_name"], description=cfg["get_gamage_command_description"])
		async def get_dmg_func(interaction):
			self._dmgs = self.parse_file()
			if len(self._dmgs):
				peops = []
				for name in self._dmgs:
					peops.append((name, self._dmgs[name]))
				peops.sort(key=lambda p: int(p[1]), reverse=True)
				msg = ''
				for pe in peops:
					msg += pe[0] + '\t' + self.denormalizer(pe[1]) + '\n'
				await interaction.response.send_message(msg)
			else:
				await interaction.response.send_message('Список пуст')
		
		@self.event
		async def on_ready():
			synced = await self.tree.sync()
			print(f"Synced {len(synced)} command{'s' if len(synced) > 1 else ''}.")
			print(f"{self.user} is ready and online!")
	
	@staticmethod
	def normalizer(dmg: str) -> int:
		""" Damage converter
			:param dmg: Damage with letter (e.g., 123.56M)
			:return: Damage without letter (e.g., 123560000)
		"""
		
		if any([let in dmg for let in ['m', 'M', 'м', 'М', 'K', 'k', 'к', 'К']]):
			count = float(dmg[:-1])
			letter = dmg[-1]
			if letter in ['m', 'M', 'м', 'М']:
				count *= 1000000
			elif letter in ['K', 'k', 'к', 'К']:
				count *= 1000
			return int(count)
		else:
			return int(dmg)
	
	@staticmethod
	def denormalizer(dmg: int) -> str:
		""" Damage converter
			:param dmg: Damage without letter (e.g., 123560000)
			:return: Damage with letter (e.g., 123.56M)
		"""
		
		dmg = str(dmg)
		if 7 > len(dmg) > 3:
			dmg = str(float(dmg) / 1000) + 'K'
		elif len(dmg) > 6:
			dmg = str(float(dmg) / 1000000) + 'M'
		return dmg
	
	@staticmethod
	def parse_file() -> dict[str, int]:
		"""Read damage from dmg.json into {"name": damage} dict"""
		
		with open("dmg.json", "r") as jsonFile:
			data = json.load(jsonFile)
		return data
