import shutil
import csv
import os

#####################################################################################
##### 1ª PARTE: RODA OS SCRIPTS NO SIMULADOR E SALVA AS SAIDAS EM ~/Results 	#####
#####################################################################################
algs = ["FastFourierTransform", "MultMatriz", "QuickSort"]
execsCache = {"CacheAssoc": [1, 2, 4, 8, 16, 32], "CacheSize": [0.5, 1, 2, 4, 8, 16]}
execsCPU = {"IntALU": [1, 2, 3, 4], "LatIntALU": [1, 2, 4, 8]}

try:
	os.system("rm -rf Results")
except:
	pass

# Copia os algoritmos e compila eles com as flags corretas
for alg in algs:
	cp_str = "cp algoritmos/" + alg + ".c ~/gem5/orgb_progs/" + alg + ".c"
	os.system(cp_str)

	exec_str = "gcc ~/gem5/orgb_progs/" + alg + ".c -O0 -lm -lcrypto -static -o ~/gem5/orgb_progs/" + alg
	os.system(exec_str)

for ex in execsCPU:
	# Copia arquivos originais de volta
	os.system("cp caches/basic_caches_fixo.py ~/gem5/orgb_configs/systems/caches/basic_caches.py")
	os.system("cp cpus/MyO3CPU_fixo.py ~/gem5/orgb_configs/systems/cpus/MyO3CPU.py")

	for num in execsCPU[ex]:
		os.system("rm ~/gem5/orgb_configs/systems/cpus/MyO3CPU.py")
		os.system("rm ~/gem5/orgb_configs/systems/cpus/MyO3CPU.pyc")

		src_cpu = "cpus/MyO3CPU_" + ex + "_" + str(num) + ".py"
		dst_cpu = "~/gem5/orgb_configs/systems/cpus/MyO3CPU.py"
		os.system("cp "+ src_cpu + " " + dst_cpu)

		for alg in algs:
			exec_str = "~/gem5/gem5 ~/gem5/orgb_configs/simulate.py run-benchmark -c ~/gem5/orgb_progs/" + alg
			os.system(exec_str)

			# Cria diretório para resultados
			exec_str = "mkdir -p Results/" + alg + "/" + ex
			os.system(exec_str)

			src_result = "m5out/stats.txt"
			dst_result = "Results/" + alg + "/" + ex + "/stats_" + str(num) + ".txt"
			os.system("cp "+ src_result + " " + dst_result)

for ex in execsCache:
	# Copia arquivos originais de volta
	os.system("cp caches/basic_caches_fixo.py ~/gem5/orgb_configs/systems/caches/basic_caches.py")
	os.system("cp cpus/MyO3CPU_fixo.py ~/gem5/orgb_configs/systems/cpus/MyO3CPU.py")

	for num in execsCache[ex]:
		os.system("rm ~/gem5/orgb_configs/systems/caches/basic_caches.py")
		os.system("rm ~/gem5/orgb_configs/systems/caches/basic_caches.pyc")

		src_cache = "caches/basic_caches_" + ex + "_" + str(num) + ".py"
		dst_cache = "~/gem5/orgb_configs/systems/caches/basic_caches.py"
		os.system("cp "+ src_cache + " " + dst_cache)

		for alg in algs:
			exec_str = "~/gem5/gem5 ~/gem5/orgb_configs/simulate.py run-benchmark -c ~/gem5/orgb_progs/" + alg
			os.system(exec_str)

			# Cria diretório para resultados
			exec_str = "mkdir -p Results/" + alg + "/" + ex
			os.system(exec_str)

			src_result = "m5out/stats.txt"
			dst_result = "Results/" + alg + "/" + ex + "/stats_" + str(num) + ".txt"
			os.system("cp "+ src_result + " " + dst_result)


#########################################################################################
##### 2ª PARTE: PROCESSA OS RESULTADOS E GERA UM .csv COM OS PARÂMETROS DEFINIDOS.	#####
#########################################################################################
execs = execsCache.copy()
execs.update(execsCPU)

with open("Results/saida.csv", mode='w', newline='') as saida_file:
	fieldnames = ['algoritmo', 'mudanca', 'exec', 'overall_miss_rate', 'sim_seconds', 'ipc', 'host_seconds', 'overall_accesses', 'overall_misses', 'overall_hits']
	writer = csv.DictWriter(saida_file, fieldnames=fieldnames)
	writer.writeheader()

	for algoritmo in algs:
		for ex in execs: 
			for num in execs[ex]:
				file_name = "Results/" + algoritmo + "/" + ex + "/stats_" + str(num) + ".txt"

				print ("\n" + algoritmo + " -> " + ex + ": "+ str(num))

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

				writer.writerow({'algoritmo': algoritmo, 'mudanca': ex, 'exec': num, 'overall_miss_rate': overall_miss_rate, 'sim_seconds': sim_seconds, 'ipc': ipc, 'host_seconds': host_seconds, 'overall_accesses': overall_accesses, 'overall_misses': overall_misses, 'overall_hits': overall_hits})