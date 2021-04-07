import json
import sys


def tryToAllocate(demand, j):
	for i in range(0, len(circuits)):
		if(circuits[i][0] == demand["end-points"][0] and circuits[i][len(circuits[i])-1] == demand["end-points"][1]):
			if(examineCircuit(circuits[i], demand) == True): #járható, siker
				allocateCircuit(circuits[i], demand)
				demandCircuit[j] = i;
				return True
			else: #sikertelen
				return False


def examineCircuit(circuit, demand):
	for i in range(0, len(circuit)-1):
		n = seachLink(circuit[i], circuit[i+1])
		if(links[n]["capacity"] < (usedLinks[n]+demand["demand"])):
			return False
	return True
		
		
def allocateCircuit(circuit, demand):
	for i in range(0, len(circuit)-1):
		n = seachLink(circuit[i], circuit[i+1])
		usedLinks[n] = usedLinks[n] + demand["demand"]
	
	
def seachLink(c1, c2):
	for i in range(0, len(links)):
		if((links[i]["points"][0] == c1 or links[i]["points"][0] == c2) and (links[i]["points"][1] == c1 or links[i]["points"][1] == c2)):
			return i
	return -1
	
	
def freeCircuit(demand, j):
	if(demandCircuit[j] != -1):
		for i in range(0, len(circuits[demandCircuit[j]])-1):
			n = seachLink(circuits[demandCircuit[j]][i], circuits[demandCircuit[j]][i+1])
			usedLinks[n] = usedLinks[n] - demand["demand"]
			
		demandCircuit[j] = -1;
	



with open(sys.argv[1], "r") as file:
    jsondata = json.load(file)
	
end_points = jsondata["end-points"]
switches = jsondata["switches"]
links = jsondata["links"]
circuits = jsondata["possible-circuits"]
simulation = jsondata["simulation"]


usedLinks = [0]*len(links)
#usedLinks=[len(links)]
#for i in range(0, len(links)):
#	usedLinks[i] = 0
demandCircuit = [-1]*len(simulation["demands"])
#demandCircuit=[len(simulation["demands"])] #azt tárolja le h melyik demandhoz melyik circuit (sorszám) lett felhasználva
#for i in range(0, len(simulation["demands"])):
#	demandCircuit[i] = -1

line = 1;


for time in range(1, simulation["duration"]):
	for j in range(0, len(simulation["demands"])):  
		if (simulation["demands"][j]["start-time"] == time):
			if(tryToAllocate(simulation["demands"][j], j) == True):
				print(str(line) + ". igény foglalás: " + str(simulation["demands"][j]["end-points"][0]) + "<->" + str(simulation["demands"][j]["end-points"][1]) + " st:" + str(time) + " - sikeres")
				line = line+1
			else:
				print(str(line) + ". igény foglalás: " + str(simulation["demands"][j]["end-points"][0]) + "<->" + str(simulation["demands"][j]["end-points"][1]) + " st:" + str(time) + " - sikertelen")
				line = line+1
		if (simulation["demands"][j]["end-time"] <= time and demandCircuit[j]!=-1):
			freeCircuit(simulation["demands"][j], j)
			print(str(line) + ". igény felszabadítás: " + str(simulation["demands"][j]["end-points"][0]) + "<->" + str(simulation["demands"][j]["end-points"][1]) + " st:" + str(time))
			line = line+1
			
			