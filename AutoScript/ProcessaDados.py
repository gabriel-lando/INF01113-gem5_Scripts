import csv

algs = ["FastFourierTransform", "MultMatriz", "QuickSort"]
execs = {"CacheAssoc": [1, 2, 4, 8, 16, 32], "CacheSize": [0.5, 1, 2, 4, 8, 16], "IntALU": [1, 2, 3, 4]}

with open("saida.csv", mode='w', newline='') as saida_file:
	fieldnames = ['algoritmo', 'exec', 'change', 'overall_miss_rate', 'sim_seconds', 'ipc', 'host_seconds', 'overall_accesses', 'overall_misses', 'overall_hits']
	writer = csv.DictWriter(saida_file, fieldnames=fieldnames)
	writer.writeheader()

	for algoritmo in algs:
		for ex in execs: 
			for index in execs[ex]:
				file_name = algoritmo + "\\" + ex + "\\stats_" + str(index) + ".txt"

				print ("\n" + algoritmo + " -> " + ex + ": "+ str(index))

				file = open(file_name)

				overall_miss_rate = ""
				sim_seconds = ""
				ipc = ""
				host_seconds = ""
				overall_accesses = ""
				overall_misses = ""
				overall_hits = ""

				for line in file.readlines():
					if line.find("system.cpu.dcache.overall_miss_rate::total") >= 0:
						print ("Overall Miss Rate:      " + line[45:65].strip())
						overall_miss_rate = line[45:65].strip()
					elif line.find("sim_seconds") >= 0:
						print ("# of seconds simulated: " + line[40:58].strip())
						sim_seconds = line[40:58].strip()
					elif line.find("system.cpu.ipc ") >= 0:
						print ("Instructions Per Cycle: " + line[40:58].strip())
						ipc = line[40:58].strip()
					elif line.find("host_seconds ") >= 0:
						print ("RT elapsed on the host: " + line[40:58].strip())
						host_seconds = line[40:58].strip()
					elif line.find("system.cpu.dcache.overall_accesses::total") >= 0:
						print ("Overall Accesses Total: " + line[45:65].strip())
						overall_accesses = line[45:65].strip()
					elif line.find("system.cpu.dcache.overall_misses::total ") >= 0:
						print ("Overall Misses Total:   " + line[45:65].strip())
						overall_misses = line[45:65].strip()
					elif line.find("system.cpu.dcache.overall_hits::total ") >= 0:
						print ("Overall Hits Total:     " + line[45:65].strip())
						overall_hits = line[45:65].strip()

				writer.writerow({'algoritmo': algoritmo, 'exec': ex, 'change': index, 'overall_miss_rate': overall_miss_rate, 'sim_seconds': sim_seconds, 'ipc': ipc, 'host_seconds': host_seconds, 'overall_accesses': overall_accesses, 'overall_misses': overall_misses, 'overall_hits': overall_hits})