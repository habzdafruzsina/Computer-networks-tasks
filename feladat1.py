import sys
import subprocess
import platform
from datetime import date
from subprocess import PIPE
import json

file = open(sys.argv[1],'r')

list = [];
list2 = [];


#fájl beolvas
for line in file:
    list.append(line)
    
file.close()



for i in range(0,10,1):
	list2.append(list[i].rstrip('\n').split(',')[1])
    
for i in range(len(list),len(list)-10,-1):
	list2.append(list[i-1].rstrip('\n').split(',')[1])
    
#print(list2)




traceroute = {
	"date": date.today().strftime("%Y%m%d"),
	"system": platform.system().lower(),
	"traces": []
}

pingfile = {
	"date": date.today().strftime("%Y%m%d"),
	"system": platform.system().lower(),
	"pings": []
}



if platform.system().lower() == "windows":

	for i in range(0,20,1):
		p1 = subprocess.Popen(["tracert", '-h', '30', list2[i]], shell=True, stdout=subprocess.PIPE)
		#print(p1.communicate())
		trace = {
			"target": list2[i],
			"output": p1.communicate()[0].decode()
		}
		traceroute["traces"].append(trace)
		#print(json.dumps(traceroute))
		
		p2 = subprocess.Popen(["ping", '-n', '10', list2[i]], stdout=subprocess.PIPE)
		#print(p2.communicate())
		ping = {
			"target": list2[i],
			"output": p2.communicate()[0].decode()
		}
		pingfile["pings"].append(ping)
		#print(pingfile["pings"])
		
else:

	for i in range(0,20,1):
		p1 = subprocess.Popen(["traceroute", '-h', '30', list2[i]], shell=True, stdout=subprocess.PIPE)
		#print(p1.communicate())
		trace = {
			"target": list2[i],
			"output": p1.communicate()[0].decode()
		}
		traceroute["traces"].append(trace)
		
		p2 = subprocess.Popen(["ping", '-c', '10', list2[i]], stdout=subprocess.PIPE)
		#print(p2.communicate())
		ping = {
			"target": list2[i],
			"output": p2.communicate()[0].decode()
		}
		pingfile["pings"].append(ping)


with open("traceroute.json", "w") as f1:
	json.dump(traceroute, f1)

with open("ping.json", "w") as f2:
	json.dump(pingfile, f2)

#with open('traceroute.json', 'w') as f1:
    #f1.write(p1.communicate)
#f1.close()
#with open('ping.json', 'w') as f2:
    #f2.write(p2.communicate)
#f2.close()    
