#Création du fichier .json

import json

data_test = {
 	 	 'gender' : '',
 	 	 'name' : '',
 	 	 'capacity' : 1,
 	 	 'results' : {},
 	 	 'standards' : {},

}

print (data_test)

out_file = open("test.json", 'w')

json.dump(data_test, out_file, indent=5)

#Remplissage du fichier .json

data_test['gender'] = 'male'
data_test['name'] = 'Tom'
data_test['capacity'] = 1
results = {
 	 'Francais' : 13,
 	 'Anglais' : 19, 
 	 'Maths' : 7
}

standards = {
 'Physique' : 0.4,
 'Histoire' : 0.7, 
 'Chimie' : 0.1
}

data_test['results']= results
data_test['standards'] = standards

print (data_test)

#Enregistrement dans le fichier

out_file = open("test.json", 'w')
json.dump(data_test, out_file, indent=5)

#Ouverture du fichier en Python

in_file = open("test.json","r")

#Importation des données

gender = data_test['gender']
name = data_test['name']
capacity = data_test['capacity']

print (gender, name)