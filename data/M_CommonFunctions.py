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







class MARCHEN_CommonFunctions():

	def display_success_function(self, message):
		print(colored(str(message), "green"))

	def display_error_function(self, message):
		print(colored(str(message), "red"))

	def display_notification_function(self, message):
		print(colored(str(message), "yellow"))




	def load_model_prompt_function(self):
		try:
			with open(os.path.join(os.getcwd(), "data/promptSystem/prompt_Start.json"), "r") as read_file:
				self.model_prompt_dictionnary = json.load(read_file)

		except Exception as e:
			self.display_error_function("Impossible to load prompt dictionnary!\n%s"%e)
			return
		else:
			self.display_success_function("Prompt dictionnary loaded successfully!")





	def prompt_function(self, prompt, generate_object=False):
		self.display_notification_function("Starting generation...")



		if generate_object == True:
			prompt += """

"""
		try:
			client = Groq(
				api_key = os.environ.get("GROQ_API_KEY"),
				)
			chat_completion = client.chat.completions.create(
				messages = [
					{
						"role":"user",
						"content":prompt.encode("utf-8").decode("utf-8"),
					}
				],
				model = "mixtral-8x7b-32768"
				
			)
		except Exception as e:
			self.display_error_function("Failed to generate")
		else:
			self.display_success_function("Generation done!")
			return chat_completion.choices[0].message.content