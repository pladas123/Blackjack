import json

with open("strategy.csv", "r") as file:
    strategy_hash = json.load(file)
print(strategy_hash['Ace'])


