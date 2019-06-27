import os
import shutil

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

