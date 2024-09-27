from textual.app import App, ComposeResult
from textual.widgets import Markdown, MarkdownViewer, DataTable,TextArea, RadioSet, RadioButton, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.validation import Function, Number
from textual.screen import Screen, ModalScreen
from textual import events
from textual.containers import ScrollableContainer, Grid, Horizontal, Vertical, Container, VerticalScroll
from textual import on, work

from termcolor import *
from datetime import datetime
from groq import Groq


from data.M_CommonFunctions import MARCHEN_CommonFunctions


import ast
import time
import sys
import colorama
import os 
import pyfiglet







colorama.init()




class MARCHEN_Terminal_Application(MARCHEN_CommonFunctions):


	def __init__(self):
		print(colored("Hello world", "green"))



		self.model_prompt_dictionnary = {}
		self.mj_data_dictionnary = {}

		self.short_memory = []
		self.global_memory = []

		self.character_test_dictionnary = {
			"Name": "Robin",
			"Age": 23,
			"Class":"Wizard",
			"Inventory": [
				"Magic stick",
				"Spell book",
			],
			"Attack":6,
			"Defense":3,
			"Dexterity":4,
			"Eloquence":7,
			"Agility":5,
		}


		self.load_model_prompt_function()


		#generate the global story
		self.global_context = self.prompt_function(None, self.model_prompt_dictionnary["promptGlobalContext"], False)
		#print(self.story)




		character_prompt = self.model_prompt_dictionnary["promptCharacterContext"]

		character_prompt+= "\nThis is the story you wrote about the universe the player will live in:\n [%s]"%self.global_context
		character_prompt+= "\n\nThese are informations and statistics about the player:\n"
		for key, value in self.character_test_dictionnary.items():
			character_prompt += "%s : %s"%(key, value)


		for i in range(5):
			try:
				self.character_context = self.prompt_function(self.character_test_dictionnary, character_prompt, True)
				self.character_context.replace("'", '"')


				#print("%s\n\n\n\n"%self.character_context)
				#try to convert the character context into a dictionnary to start the adventure
				answer_dictionnary = ast.literal_eval(self.character_context)
			except Exception as e:
				self.display_error_function("Error while generating!\n%s"%e)
			else:
				break

		for key, value in answer_dictionnary.items():
			self.display_notification_function(key)
			print(value)

		


		

		#GLOBAL STORY LOOP
		for i in range(10):
			player_choice = input("...")
			if player_choice == "p":
				exit()

			#print(answer_dictionnary["option"], type(answer_dictionnary["option"]))
			new_prompt = """
suite à cette situation : [%s]

Le joueur a fait le choix de l'option : %s

Génère la suite de l'histoire
"""%(answer_dictionnary["context"], answer_dictionnary["option"][int(player_choice)-1])
			print(new_prompt)


			#generate again if syntax error
			for y in range(5):
				try:
					answer = self.prompt_function(self.character_test_dictionnary, new_prompt, True, self.short_memory)
					answer.replace("'", '"')
					answer_dictionnary = ast.literal_eval(answer)
				except Exception as e:
					self.display_error_function("error\n%s"%e)
					continue
				else:
					self.display_notification_function("OUTPUT")
					

					self.display_title_function(answer_dictionnary["context"])
					for i in range(len(answer_dictionnary["option"])):
						print(colored(i+1, "cyan"), answer_dictionnary["option"][i])



					self.short_memory.append(answer_dictionnary["context"])
					self.display_notification_function("VALUE APPENDED")
					if len(self.short_memory) > 10:
						self.display_notification_function("VALUE POPED")
						self.short_memory.pop(0)




					break




			#print(answer_dictionnary)

			
			


			














MARCHEN_Terminal_Application()



