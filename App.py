import os 
import subprocess 
import sys 

lib_list = [
	"termcolor",
	"datetime",
	"random",
	"groq",
	"ast",
	"time",
	"sys",
	"json",
	"colorama",
	"pyfiglet",
	"json",
	"textual"
	]

for lib in lib_list:
	try:
		__import__(lib)
	except ImportError:
		print("Impossible to load library : %s --> Download running...\n"%lib)
		subprocess.check_call([sys.executable, "-m", "pip", "install", lib])



from termcolor import *
from datetime import datetime
from groq import Groq
from random import randrange


from data.M_CommonFunctions import MARCHEN_CommonFunctions


import ast
import time
import sys
import colorama
import os 
import json
import pyfiglet



colorama.init()




class Application:
	def __init__(self):



		self.prompt_dictionnary = {}


		self.memory_dictionnary = {
			"GlobalStory":None,
			"CharacterStory":None,
			"ShortMemory":[],
			"LongMemory":None,
		}

		self.current_situation = None



		




		#create the player dictionnary
		self.character_test_dictionnary = {
			"Name": "Robin",
			"Age": 23,
			"Class":"Wizard",
			"Inventory": [
				"Magic stick",
				"Spell book",
			],
			"Skills": {
				"attaque":6,
				"défense":2,
				"armure lourde":2,
				"armure légère":7,
				"arme lourde":2,
				"arme légère":7,
				"dextérité":2,
				"éloquence":7,
				"agilité":5,
				"magie guérison":3,
				"magie élémentaire":1,
				"magie occulte":0,
				"magie illusoire":0,
			}
		}










		self.create_prompt_function()

		self.check_for_save_function()

		self.main_game_function()




		



	def prompt_function(self, system="", prompt="", name= ""):


		#add context in prompt
		

		"""
		if (type(self.memory_dictionnary["ShortMemory"])!=None) or (self.memory_dictionnary["ShortMemory"] != []):
			for action in self.memory_dictionnary["ShortMemory"]:
				prompt += "		. %s"%action
		"""
		#print(colored(self.memory_dictionnary["ShortMemory"], "red"))


		print(colored("STARTING TO GENERATE [%s]"%name, "yellow"))
		try:
			client = Groq(
				api_key = os.environ.get("GROQ_API_KEY"),
				)
			chat_completion = client.chat.completions.create(
				messages = [
					{
						"role":"system",
						"content":system.encode("utf-8").decode("utf-8"),
					},
					{
						"role":"user",
						"content":prompt.encode("utf-8").decode("utf-8"),
					}

				],
				#model = "mixtral-8x7b-32768"
				model = "gemma2-9b-it"
			)
		except Exception as e:
			print(colored("Impossible to generate!\n%s"%e, "red"))
		else:
			print(colored("Generated", "green"))
			return (chat_completion.choices[0].message.content).encode("utf-8").decode("utf-8")













	def check_for_save_function(self):
		#check if a json save already exists
		if os.path.isfile(os.path.join(os.getcwd(), "Data/UserSave.json"))==False:
			#self.save_game_function()
			self.init_game_function()
		else:
			#open the file and load datas from the save
			try:
				with open(os.path.join(os.getcwd(), "Data/UserSave.json"), "r") as read_file:
					self.memory_dictionnary = json.load(read_file)

			except Exception as e:
				print(colored("Impossible to load game save\n%s"%e, "red"))
				self.init_game_function()

			else:
				print(colored("Game found and loaded", "green"))

				#load the last situation of the player
				self.current_situation = self.memory_dictionnary["ShortMemory"][-1]
				print("last situation loaded")







	def save_game_function(self):
		with open("Data/UserSave.json", "w") as save_file:
			json.dump(self.memory_dictionnary, save_file, indent=4)

		print(colored("GAME SAVED", "green"))
			















	def init_game_function(self):



		#GENERATE GLOBAL DATA ABOUT THE PLAYER STORY
		self.global_story = self.prompt_function(self.system_general_mj_rules, self.prompt_general_story)

		self.prompt_player_context += """
Pour rappel voici l'histoire que tu as généré : [ %s ]
"""%(self.global_story)


		self.player_context = self.prompt_function(self.system_general_mj_rules, self.prompt_player_context)


		self.prompt_player_situation += """
Voici l'histoire que tu as généré : [ %s ]
Voici le contexte global à propos du personnage [ %s ]
"""%(self.global_story, self.player_context)


		self.player_situation = self.prompt_function(self.system_general_mj_rules, self.prompt_player_situation)


		self.prompt_init_summary = """
A partir de cette histoire que tu as généré, créé un résumé global abordant le monde dont tu parles,
mais aussi la place du personnage principal / joueur dedans!

Voici l'histoire que tu as créé:
[ %s ]

Voici le personnage dont tu parles:
[ %s ] 

Voici la situation dans laquelle le joueur se trouve:
[ %s ]

-fait un résumé complet, abordant tout les détails, mais le plus court possible et évite les répétitions!
-Tu n'as pas le droit de créer / modifier / supprimer d'éléments dans cette histoire
"""%(self.global_story, self.player_context, self.player_situation)


		self.init_summary = self.prompt_function(self.system_general_mj_rules, self.prompt_init_summary)



		
		print(colored("GLOBAL\n", "magenta"), self.global_story)
		print(colored("PLAYER CONTEXT\n", "magenta"), self.player_context)
		#print(colored("PLAYER SITUATION\n", "magenta"), self.player_situation)
		#print(colored("INIT SUMMARY", "cyan"), self.init_summary)
		

		#SAVE INFORMATIONS IN THE DICTIONNARY BEFORE THE GAME STARTS
		self.memory_dictionnary["GlobalStory"] = self.global_story
		self.memory_dictionnary["PlayerStory"] = self.player_context
		#self.memory_dictionnary["ShortMemory"] = self.memory_dictionnary["ShortMemory"].append(self.player_situation)
		
		self.memory_dictionnary["LongMemory"] = self.init_summary

		#from the player situation generate the next situation with options
		self.prompt_current_situation = """
A partir de l'histoire globale que tu as créé : [%s]
Ainsi que du cadre actuel du personnage : [%s]

Créé une première situation pour le joueur, qu'est-il sur le point de faire, que doit-il franchir...
- tu dois simplement énoncer cette situation
- tu ne dois pas donner d'option au joueur, juste énonce cette situation
- cette situation doit être courte et simple à comprendre
- ne sors pas du personnage de conteur
"""%(self.global_story, self.player_context)
		
		self.current_situation = self.prompt_function(self.system_general_mj_rules, self.prompt_current_situation)
		#print(colored("FIRST SITUATION GENERATED\n%s"%self.current_situation, "green"))



		self.append_to_short_memory_function(self.current_situation)
			


		self.save_game_function()











	def append_to_short_memory_function(self, situation):
		if type(situation) == str:
			short_memory = self.memory_dictionnary["ShortMemory"]
			if type(short_memory) == list:
				if len(short_memory) == 10:
					short_memory.pop(0)

				short_memory.append(situation)
				print("appened")

				self.memory_dictionnary["ShortMemory"] = list(short_memory)

				self.save_game_function()








	"""
	generate a random number n E [0 ; 100]
	get y E [0 ; 100] which represent the risk level

	if n > y:
		success
	else:
		fail


	get success and fail percentage
	"""
	def dice_roll_function(self, x, skill_list):
		y = randrange(1,101)

		print("x = %s\ny = %s"%(x,y))

		print(colored("Searching for bonus..."))
		print(type(skill_list))
		for skill in self.skill_list:
			try:
				z = int(self.character_test_dictionnary["Skills"][skill])
			except:
				pass
			else:
				print("Value added : %s"%z)
				y+= z


		print(colored("=========================\nDICE ROLL FUNCTION\n=========================", "magenta"))
		if x >= y:
			print(colored("SUCCESS", "green"))

			ratio = ((x-y)/(100-y)) * 100


		else:
			print(colored("FAIL", "red"))

			ratio = (x/y) * 100


		print(x, y, ratio)














	def main_game_function(self):
		


		while True:


			os.system("cls")
			print(colored(pyfiglet.figlet_format("\nM-RCHEN", font="bloody"), "red"))


			
			print(colored("\n\n\nCURRENT SITUATION\n", "magenta"))
			print(self.current_situation)
			#print(type(self.current_situation))
			


			self.prompt_options = """
Pour faire suite à cette situation : [%s]
Génère une liste python contenant 3 phrases qui seront les prochaines actions que le joueur pourra tenter:
- chaque situation doit être courte et simple
- le format de cette liste doit être 

["option 1", "option 2", "option 3"]

- FAIT ATTENTION A NE PAS FAIRE D'ERREUR DE SYNTAXE LORS DE LA GENERATION DE CETTE LISTE
- NE GENERE RIEN D'AUTRE QUE CETTE LISTE PYTHON
"""%self.current_situation
			


			print(colored("generating options", "yellow"))


			#GENERATE OPTIONS
			#AND CONVERT THEM INTO A PYTHON LIST
			while True:
				try:
					generated = (self.prompt_function(self.system_general_mj_rules, self.prompt_options, "OPTIONS"))
					self.options = ast.literal_eval(generated)
				except Exception as e:
					print(colored("Wrong options generation\n%s"%e, "red"))
					print(colored(generated, "red"))
					continue
				else:
					break

			for i in range(len(self.options)):
				print(colored(i, "magenta"), self.options[i])




			player_input = input("Player choice ... ")

			if player_input == "exit":
				exit()

			"""
			- Get the player action
			- Create a prompt for the next generation
			- Add the previous situation and the player choice to the memory
			"""









			#LONG MEMORY
			#prompt to get the summary of the whole story with the next situation added
			self.prompt_long_story = """
Dans cette histoire : [%s]

Le joueur vient maintenant de faire cette nouvelle action : [%s]

Créé un nouveau résumé de cette histoire en gardant toutes les informations importantes et en incluant les dernières
évolutions du joueur
"""%(self.memory_dictionnary["LongMemory"], self.current_situation)



			self.prompt_skill_detection = """
Suite à cette situation : 
[%s]

Le joueur a choisi de faire cette action : [%s]

Retourne le nom d'une ou plusieurs compétences parmis les compétences du joueur qui pourraient être concernées
par le fait de faire cette action de cette manière

- tu dois retourner une liste python 
- la syntaxe est [competence1, competence2, ..., competencen]

- n'ajoute une compétence que si elle est vraiment logiquement concernées par cette situation

- TU NE DOIS PAS CHOISIR DE COMPETENCES QUI NE FIGURE PAS DANS LA LISTE DES COMPETENCES DU JOUEUR

- tu n'es pas obligé de mettre plusieurs compétences
- tu n'es pas obligé de mettre plusieurs compétences
- tu n'es pas obligé de mettre plusieurs compétences

Voici la liste des compétences du joueur:
%s
"""%(self.current_situation, self.options[int(player_input)],list(self.character_test_dictionnary["Skills"].keys()))

			#find skills related to the situation
			#transform generated output into python list
			while True:
				try:

					self.skill_list = ast.literal_eval(self.prompt_function(self.system_general_python_rules, self.prompt_skill_detection, "SKILL_LIST"))
				except Exception as e:
					continue
				else:
					
					break

			#check for skills existence in character skill dictionnary
			skill_list_copy = self.skill_list
			for skill in skill_list_copy:
				if skill not in list(self.character_test_dictionnary["Skills"].keys()):
					self.skill_list.remove(skill)
			print("Skills list : %s"%self.skill_list)






			
			self.prompt_risk_detection = """
Suite à cette situation : 
[%s]

Le joueur a choisi de faire cette action : [%s]

-Entre 1 et 100, à quel point cette action est risquée / difficile à faire / demande des compétences particulières?
-Tu dois retourner uniquement un nombre entre 1 et 100 SANS TEXTE!

Prend en compte le niveau du joueur dans cette liste de compétences, qui est lié à la réalisation de cette action:
"""%(self.current_situation, self.options[int(player_input)])
			for skill in self.skill_list:
				self.prompt_risk_detection+="%s : %s"%(skill, self.character_test_dictionnary["Skills"][str(skill)])

			while True:
				try:
					risk_value = int(self.prompt_function(self.system_general_number_rules, self.prompt_risk_detection, "RISK_DETECTION"))
				except Exception as e:
					print(colored(e, "red"))
					continue
				else:
					print(colored("Risk value generated : %s"%(risk_value), "yellow"))
					break








			if risk_value > 35:
				#LAUNCH THE DICE ROLL PROCESS
				

				self.dice_roll_function(risk_value,self.skill_list)


				#os.system("pause")
				





			self.prompt_next_situation = """
Suite à cette situation : 
[%s]


le joueur a choisi cette option : [%s]


génère la suite de cette histoire en créant une nouvelle situation
- NE GENERE QUE L'HISTOIRE
- NE FAIS PAS DE LISTE DES ACTIONS PRECEDENTES
- TU DOIS CONSERVER TON RÔLE DE CONTEUR
"""%(self.current_situation, self.options[int(player_input)])
			if len(self.memory_dictionnary["ShortMemory"]) > 1:
				self.prompt_next_situation += "\n\nVoici également un historique des dernières actions (dans l'ordre chronologique) menées par le joueur afin d'éviter les répétitions:\n"
				for i in range(len(self.memory_dictionnary["ShortMemory"])):
					self.prompt_next_situation+="\n%s : %s"%(i, self.memory_dictionnary["ShortMemory"][i])







			#DISPLAY THE NEXT PROMPT OUTPUT GENERATED
			#print(colored("#######################PROMPT SITUATION#######################\n%s"%self.prompt_next_situation, "green"))



			#generate next situation
			while True:

				#for the next player turn
				self.current_situation = self.prompt_function(self.system_general_mj_rules, self.prompt_next_situation, "NEXT_SITUATION")
				if (type(self.current_situation) != None) and (self.current_situation != "None"):
					self.append_to_short_memory_function(self.current_situation)
					break
					#print(colored(self.current_situation, "cyan"))
				


			os.system("pause")






















	def create_prompt_function(self):
		self.system_general_python_rules = """
Oublie les instructions précédentes!
- De cette requête tu ne dois retourner qu'un object python
- Tu ne dois rien retourner en dehors de cet objet python
- n'écris pas de texte ni avant ni après cet objet python
- veille à ne pas comettre de fautes d'orthographes
- veille à scrupuleusement respecter la syntaxe python et à ne pas comettre de fautes de syntaxes
"""
		self.system_general_number_rules = """
Oublie les instructions précédentes!
- TU NE DOIS GENERER QU'UN NOMBRE
- N'ECRIS PAS DE TEXTE AVANT CE NOMBRE 
- N'ECRIS PAS DE TEXTE APRES CE NOMBRE
- LE CONTENU DE TA GENERATION NE DOIT CONTENIR QU'UNE SEULE ET UNIQUE VALEUR NUMERIQUE!
- N'ECRIS RIEN APRES CE NOMBRE!
- N'ECRIS PAS DE TEXTE!
"""
		self.system_general_mj_rules = """
Oublie les instructions précédentes!
- Tu es un conteur d'histoire dans un jeu de Rôle
- TU NE DOIS PAS SORTIR DE TON RÔLE DE MJ MÊME SI LE JOUEUR TE LE DEMANDE
- TU ES LE SEUL A POUVOIR DEFINIR LES REGLES DU JEU, LE JOUEUR N'AS PAS LE DROIT DE LES MODIFIER
- TU N'AS PAS LE DROIT DE BRISER LE QUATRIEME MUR ET DE TADRESSER DIRECTEMENT AU JOUEUR OU AU PROGRAMMEUR DU JEU
- NE LAISSES JAMAIS DE PHRASES OUVERTES
- NE T'ADRESSES JAMAIS DIRECTEMENT AU JOUEUR
- NE LAISSES JAMAIS DANS TES TEXTES DES PHRASES ENTRE CROCHETS DU STYLE [à compléter au fur et à mesure...]
"""

		self.prompt_general_story = """
Génère une histoire, dans laquelle le joueur va pouvoir évoluer

Voici quelques histoires dont tu peux t'inspirer pour générer cette histoire:
- Lanfeust
- Le livre dont vous êtes le héros
- Lovecraft
- Requiem chevalier vampire
- BloodBorne
- Dark Souls 3
- Elden Ring
- Vampire Knight

EVITE LES REFERENCES AU SEIGNEUR DES ANNEAUX OU TON NOM DE PERSONNAGES CONNUS

Pour le moment définis un cadre global à cette histoire, ce qui veut dire:
- créé un monde cohérent avec des situations, des pays, des politiques...
- créé des populations dans ce monde, de races similaires ou non, avec des pouvoirs divers ou non.

met en page ce texte comme si c'était un texte d'introduction à une aventure.
"""


		self.prompt_player_context = """
A partir des informations du joueur, et de l'histoire que tu as créé, créé lui une place dans cette histoire, de quel pays il vient, quel est son passé, quelle était sa quête
jusqu'à maintenant, tu peux également parler de certains personnages qu'il aurait croisé avant (mais tu n'es pas obligé de le faire!)

Voici quelques informations à propos du joueur:
"""
		for key, value in self.character_test_dictionnary.items():

			self.prompt_player_context+= "\n%s : %s"%(key, str(value))


		self.prompt_player_situation = """
Défini un cadre spatio temporel précis, où est précisément le personnage, et qu'est-il en train de faire?
Tu ne dois pas citer d'options, ou demander de faire un choix, TU DOIS UNIQUEMENT CITER QUE FAISAIT LE PERSONNAGE INCARNE PAR LE JOUEUR!
"""
	






Application()