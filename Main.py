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


import time
import sys
import colorama
import os 
import pyfiglet









class MARCHEN_Terminal_Application(MARCHEN_CommonFunctions):


	def __init__(self):
		print(colored("Hello world", "green"))



		self.model_prompt_dictionnary = {}
		self.mj_data_dictionnary = {}

		self.character_test_dictionnary = {
			"Name": "Robin",
			"Age": 23,
			"Class":"Wizard",
			"Weapon": [
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
		self.global_context = self.prompt_function(self.model_prompt_dictionnary["promptGlobalContext"])
		#print(self.story)




		character_prompt = self.model_prompt_dictionnary["promptCharacterContext"]

		character_prompt+= "\nThis is the story you wrote about the universe the player will live in:\n [%s]"%self.global_context
		character_prompt+= "\n\nThese are informations and statistics about the player:\n"
		for key, value in self.character_test_dictionnary.items():
			character_prompt += "%s : %s"%(key, value)


		self.character_context = self.prompt_function(character_prompt, True)

		print(self.character_context)











MARCHEN_Terminal_Application()



