= Rapport DSP (Benchmark FIR)

== Contexte
- Microcontroleur: STM32F446ZE
- Traitement: FIR Q15 (arm_fir_fast_q15)
- Frequence d'echantillonnage: 8000 Hz
- Taille de bloc: 128 echantillons
- Frequence CPU: 168 MHz

== Mesures brutes (debug)
- firCyclesLast = 9962 cycles
- firCyclesPerSample = 77 cycles/ech
- firCyclesMin = 9916 cycles
- firCyclesMax = 10230 cycles
- firCyclesSum = 14,116,551 cycles
- firBlocks = 1417 blocs

== Calculs
- Cycles moyens / echantillon:
  (14,116,551) / (1417 * 128) = 77.86 cycles/ech

- Budget cycles / echantillon:
  168,000,000 / 8000 = 21,000 cycles/ech

- Charge CPU du FIR:
  (77.86 / 21,000) * 100 = 0.37 %

- Temps par bloc (dernier):
  (9962 / 168,000,000) * 1,000,000 = 59.30 us

== Conclusion
Le FIR tient largement en temps reel (charge environ 0.37 %). Le temps par bloc est tres faible par rapport au budget disponible.

== Benchmark vs datasheet
- Frequence max CPU (datasheet): 180 MHz
- Perf globale: 225 DMIPS (1.25 DMIPS/MHz)

La comparaison la plus pertinente pour le temps reel est le budget de cycles par echantillon. Avec 21,000 cycles/ech disponibles et 77.86 cycles/ech utilises, l'execution est largement sous le budget.
