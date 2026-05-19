= Oral - Projet DSP (STM32F446ZE)

== 1 - Contexte et objectif
- Microcontroleur: STM32F446ZE (Cortex-M4 + DSP + FPU)
- Chaine temps reel: ADC -> DMA -> FIR Q15 -> DMA -> DAC
- Objectif: filtrer un signal micro en temps reel

== 2 - Architecture DSP
- ADC sur PA0, DAC sur PA4
- Timer declenche l'echantillonnage
- DMA en buffer circulaire (ADC et DAC)
- Traitement bloc par bloc: 128 echantillons

== 3 - Definitions simples
- Benchmark: mesure du temps de calcul (ici en cycles CPU)
- Cycle CPU: un tic du processeur
- Temps reel: le bloc doit etre traite avant l'arrivee du suivant

== 4 - Mesures brutes (debug)

- firCyclesLast = 9962 cycles
- firCyclesPerSample = 77 cycles/ech
- firCyclesMin = 9916 cycles
- firCyclesMax = 10230 cycles
- firCyclesSum = 14,116,551 cycles
- firBlocks = 1417 blocs

== 5 - Calculs benchmark
- Frequence CPU: 168 MHz
- Frequence echantillonnage: 8000 Hz
- Cycles moyens / echantillon:
  $14,116,551 / (1417 * 128) = 77.86 c y c l e s/e c h$
- Budget cycles / echantillon:
  $168,000,000 / 8000 = 21,000 c y c l e s/e c h$
- Charge CPU FIR:
  $(77.86 / 21,000) * 100 = 0.37%$
- Temps par bloc (dernier):
  $(9962 / 168,000,000) * 1,000,000 = 59.30 u s$

== 6 - Conclusion temps reel
- Le FIR tient largement en temps reel
- Charge CPU tres faible (~0.37%)
- Grande marge pour d'autres traitements

== 7 - Comparaison datasheet
- Frequence max CPU: 180 MHz
- Performance globale: 225 DMIPS (1.25 DMIPS/MHz)
- Comparaison utile: budget cycles par echantillon
- 21,000 cycles/ech disponibles vs 77.86 utilises

== 8 - Specs utiles (datasheet)
- ADC: 12 bits, 2.4 MSPS (jusqu'a 7.2 MSPS en triple interleaved)
- DAC: 2 x 12 bits
- DMA: 16 streams, FIFO, burst
- DSP instructions + FPU simple precision

== 9 - Precision ADC (extrait)
- ENOB a 18 MHz: typ 10.4 bits
- ENOB a 36 MHz: typ 10.8 bits
- SNR: 64 a 68 dB selon f_ADC

== 10 - Points pour l'oral
- Explique que le benchmark mesure des cycles CPU
- Montre que la charge est largement sous le budget
- Relie DMA + buffer circulaire a la stabilite temps reel
- Appuie la comparaison avec les chiffres datasheet
