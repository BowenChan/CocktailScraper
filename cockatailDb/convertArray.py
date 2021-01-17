import json

tempCocktail = {}

with open('cocktail.json') as data_file:    
    data = json.load(data_file)
    for drink in data:
        drinkData = {}
        tempCocktail[drink["name"]] = drink
        tempCocktail[drink["name"]].pop('name', None)
        
with open('convertedCocktailPretty.json', 'w') as outfile:
    json.dump(tempCocktail, outfile, indent=4, sort_keys=True)
    #json.dumps(tempCocktail, outfile, indent=4, sort_keys=True)