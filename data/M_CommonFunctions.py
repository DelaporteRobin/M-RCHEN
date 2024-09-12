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


import time
import sys
import colorama
import os 
import pyfiglet
import json
import ast







class MARCHEN_CommonFunctions():

	def display_success_function(self, message):
		print(colored(str(message), "green"))

	def display_error_function(self, message):
		print(colored(str(message), "red"))

	def display_notification_function(self, message):
		print(colored(str(message), "yellow"))

	def display_title_function(self, message):
		print(colored(str(message), "magenta"))




	def load_model_prompt_function(self):
		try:
			with open(os.path.join(os.getcwd(), "data/promptSystem/prompt_Start.json"), "r") as read_file:
				self.model_prompt_dictionnary = json.load(read_file)

		except Exception as e:
			self.display_error_function("Impossible to load prompt dictionnary!\n%s"%e)
			return
		else:
			self.display_success_function("Prompt dictionnary loaded successfully!")





	def prompt_function(self, character_dictionnary, prompt, generate_object=False, context=None):
		self.display_notification_function("Starting generation...")

		


		try:
			client = Groq(
				api_key = os.environ.get("GROQ_API_KEY"),
				)
			if generate_object == False:
				chat_completion = client.chat.completions.create(
					messages = [
						{
							"role":"user",
							"content":prompt.encode("utf-8").decode("utf-8"),
						}
					],
					model = "mixtral-8x7b-32768"
					
				)
			else:
				#self.display_error_function(context)
				if context != None:
					context_history = "\n".join(context)
					prompt = """
Voici un historique des dernières actions menées afin de générer une suite cohérente :
%s

%s
"""%(context_history, prompt)

				#self.display_title_function(prompt)
				#os.system("pause")
				player_item_list = "; ".join(character_dictionnary["Inventory"])
				system_prompt = """
En aucun cas le joueur ne peut utiliser ou avoir en sa possession dans l'histoire
un objet qui ne figure pas dans son inventaire! (sauf si le joueur ramasse un object lors d'une action de l'histoire)

Actuellement, voici l'inventaire du joueur : %s

En réponse à ce prompt, retourne un dictionnaire python de la forme suivante:

{
	'context' : str('la partie ou suite de l'histoire que tu as généré et que tu proposes au joueur'),
	'dilemna' : str('le choix que tu proposes au joueur'),
	'option' : [option1, option2, ..., option 5 max],
}

LES OPTIONS PROPOSEES DOIVENT ETRE COURTE ET SIMPLE A COMPRENDRE
RESPECTE LE PLUS POSSIBLE LA SYNTAXE D'UN DICTIONNAIRE PYTHON
"""%player_item_list
				chat_completion = client.chat.completions.create(
					messages = [
						{
							"role":"system",
							"content": system_prompt,
						},
						{
							"role":"user",
							"content":prompt.encode("utf-8").decode("utf-8"),
						}
					],
					model = "mixtral-8x7b-32768"
				)
		except Exception as e:
			self.display_error_function("Failed to generate\n%s"%e)
		else:
			self.display_success_function("Generation done!")
			return chat_completion.choices[0].message.content