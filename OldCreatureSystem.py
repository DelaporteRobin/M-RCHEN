self.prompt_check_for_creature = """
Dans cette situation que tu as généré : 
[%s]
Est ce qu'une créature intervient (qu'elle soit belliqueuse ou passive 
envers le joueur)?

- TU NE DOIS NOTIFIER QUE LES CREATURES QUE LE JOUEUR VOIT DIRECTEMENT
AVEC LESQUELLES IL A UNE VRAIE INTERRACTION!
- TU NE DOIS PAS CREER UNE NOUVELLE CREATURE SI ELLE NE CCORRESPOND QU'A
UN BRUIT ENTENDU PAR LE JOUEUR

Voici la liste des dernières actions menées par le joueur:
"""%(self.current_situation)
			for situation in self.memory_dictionnary["ShortMemory"]:
				self.prompt_check_for_creature += "\n - %s"%situation

			self.prompt_check_for_creature += """
Génère un dictionnaire pour répondre à ces deux questions:

{
	'creatureDetected':True / False,
	'creatureExists':True / False,
	'creatureChanged':True / False,
	'creatureOldName':False / str(),
	'creatureNewName':str()
}

- creatureDetected correspond à 'est ce qu'une créature ennemi du joueur intervient dans la situation'
- creatureExists correspond à 'est ce que cette créature est déjà intervenu auparavant dans l'histoire'
- creatureChanged correspond à est ce que le nom de la créature a changé entre les situations précédentes et la situation actuelle?
- creatureOldName correspond donc à l'ancien nom de cette créature (dans la liste des créatures)
- creatureNewName correspond donc au nouveau nom de cette créature mentionné dans la situation actuelle

Voici la liste des dernières actions du joueur pour savoir si cette créature existait déjà avant, et si elle a changé de forme
"""
			while True:	
				try:
					self.creature_exists_dictionnary = ast.literal_eval(self.prompt_function(self.system_general_python_rules, self.prompt_check_for_creature, "CHECK_FOR_CREATURE"))
				except Exception as e:
					print(colored(e, "red"))
				else:
					print(self.creature_exists_dictionnary)
					break





			#CREATE THE CREATURE
			#ADD IT TO THE DICTIONNARY
			if (self.creature_exists_dictionnary["creatureDetected"]==True) and (self.creature_exists_dictionnary["creatureExists"]==False):

				#create creature stats
				#add creature stats to the dictionnary
				self.prompt_create_creature = """
Dans cette situation une nouvelle créature est apparu
[%s]

créé un dictionnaire de cette forme

{
	'creatureName':'name',
	'creatureLifePoint':int(),
	'creatureStatut':'alive',
}

- récupère le nom de la créature en vérifiant que ce nom de créature n'est pas déjà utilisé dans le dictionnaire des créatures
- donne à la créature un nom qui est au plus proche du nom mentionné dans le texte ci-dessus
- attribue un nombre de point de vie à cette créature (nombre entier)
"""%(self.current_situation)
				if len(self.memory_dictionnary["CreatureDictionnary"].keys()) != 0:
					self.prompt_create_creature += """

Voici la liste des créatures déjà existantes:
%s
"""%list(self.memory_dictionnary["CreatureDictionnary"].keys())		
					
				while True:
					try:
						self.new_creature_dictionnary = ast.literal_eval(self.prompt_function(self.system_general_python_rules, self.prompt_create_creature, "CREATE_CREATURE"))		
					except Exception as e:
						print(colored(e, "red"))
					else:


						#update the creature dictionnary
						creature_dictionnary = self.memory_dictionnary["CreatureDictionnary"]
						creature_dictionnary[self.new_creature_dictionnary["creatureName"]] = self.new_creature_dictionnary
						self.memory_dictionnary["CreatureDictionnary"] = creature_dictionnary
						self.save_game_function()

						print(colored("NEW CREATURE ADDED\n%s"%creature_dictionnary, "green"))
						break

						"""
						self.memory_dictionnary["CreatureDictionnary"][self.new_creature_dictionnary["creatureName"]] = self.new_creature_dictionnary
						self.memory_dictionnary["CreatureDictionnary"] = self.creature_dictionnary
						self.save_game_function()
						print(colored("NEW CREATURE ADDED\n%s"%self.new_creature_dictionnary, "green"))
						break
						"""




	

			#LOAD THE CREATURE
			if (self.creature_exists_dictionnary["creatureDetected"]==True) and (self.creature_exists_dictionnary["creatureExists"]==True):

				self.prompt_load_creature = """
Dans cette situation une nouvelle créature est apparue
[%s]

Cette créature est déjà mentionnée dans le dictionnaire de créature
retourne une variable str() donnant le nom de la créature mentionnée

Voici la liste des créatures
%s
"""%(self.current_situation, list(self.memory_dictionnary["CreatureDictionnary"].keys()))

				self.creature_name = self.prompt_function(self.system_general_python_rules, self.prompt_load_creature, "LOAD_CREATURE")
				print(self.creature_name)