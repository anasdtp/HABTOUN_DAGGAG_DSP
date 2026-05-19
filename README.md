# Benchmark FIR - Affichage dans STM32CubeIDE

Ce projet mesure le temps d'execution du filtre FIR (fonction `arm_fir_fast_q15`) avec un compteur de cycles CPU. Ce fichier explique comment afficher ces valeurs dans STM32CubeIDE.

## Ce que mesure le benchmark

Les variables suivantes sont mises a jour pendant l'execution:

- `firCyclesLast` : cycles CPU pour un bloc FIR (benchmark brut).
- `firCyclesPerSample` : cycles CPU par echantillon.
- `firUsecPerBlock` : temps d'un bloc FIR en microsecondes.
- `firCyclesMin` / `firCyclesMax` : min / max observes.
- `firCyclesSum` et `firBlocks` : pour calculer la moyenne.
- `sampleRateHz` : frequence d'echantillonnage calculee.
- `firGroupDelaySamples` / `firGroupDelayUs` : latence du FIR.

Explications rapides des termes:
- **Cycle CPU**: un tic du processeur.
- **Bloc**: un paquet d'echantillons traite d'un coup (`AUDIO_BLOCK_SIZE`).
- **Latence**: retard ajoute par l'algorithme (ici le FIR).

## Etapes dans STM32CubeIDE (mode debug)

1. **Compiler en Debug**
   - Selectionne la configuration `Debug` puis build.

2. **Lancer le debug**
   - Clique sur l'icone *bug* (Debug) ou `Run > Debug`.
   - STM32CubeIDE telecharge le code dans la carte et s'arrete a `main()`.

3. **Laisser le programme tourner**
   - Clique sur **Resume** (le bouton vert) pour que le code s'execute en continu.

4. **Afficher les variables dans Watch**
   - Ouvre la vue **Expressions**: `Window > Show View > Expressions`.
   - Clique sur **Add new expression** et ajoute les variables:
     - `firCyclesLast`
     - `firCyclesPerSample`
     - `firUsecPerBlock`
     - `firCyclesMin`
     - `firCyclesMax`
     - `firCyclesSum`
     - `firBlocks`
     - `sampleRateHz`
     - `firGroupDelaySamples`
     - `firGroupDelayUs`

5. **Rafraichir la vue**
   - La vue se met a jour automatiquement quand le CPU s'arrete.
   - Si le CPU tourne en continu, clique sur **Pause** pour figer, regarde les valeurs, puis **Resume**.

## Calcul de la moyenne (a la main)

Pour calculer la moyenne des cycles par echantillon:

```
cycles_moyens = firCyclesSum / (firBlocks * AUDIO_BLOCK_SIZE)
```

Tu peux aussi utiliser `firCyclesPerSample` pour une valeur instantanee.

## Conseils pratiques

- Laisse tourner quelques secondes avant de lire les valeurs (le temps que les moyennes soient stables).
- Si les valeurs restent a zero, verifie que le debug est en cours et que le code tourne bien.

## Depannage rapide

- **Rien ne bouge dans Expressions**: passe en mode **Pause** puis **Resume**.
- **Valeurs a zero**: assure-toi que l'ADC/DAC/DMA demarrent bien et que le code tourne.

## Comparaison benchmark vs datasheet (STM32F446ZE)

Valeurs datasheet (source ST):
- Frequence max CPU: 180 MHz.
- Performance: 225 DMIPS, soit 1.25 DMIPS/MHz.

Lien source (ST):
- https://www.st.com/en/microcontrollers-microprocessors/stm32f446ze.html

Explication rapide des termes:
- **DMIPS**: mesure synthetique de performance CPU (test Dhrystone). Ce n'est pas un temps reel pour ton FIR, mais un repere global.
- **MHz**: millions de cycles par seconde.

### Comment comparer (etape par etape)

1. **Recupere la frequence d'echantillonnage**
   - Valeur deja calculee dans `sampleRateHz`.

2. **Calcule le budget de cycles par echantillon**
   - Formule:

```
cycles_budget = SystemCoreClock / sampleRateHz
```

3. **Mesure les cycles par echantillon**
   - Utilise `firCyclesPerSample` (valeur instantanee).
   - Ou la moyenne:

```
cycles_moyens = firCyclesSum / (firBlocks * AUDIO_BLOCK_SIZE)
```

4. **Calcule la charge CPU du FIR**
   - Formule:

```
charge_cpu_% = (cycles_moyens / cycles_budget) * 100
```

5. **Compare au datasheet**
   - Le datasheet dit que le CPU peut tenir 180 MHz et 225 DMIPS au max.
   - Si ta charge CPU est bien < 100%, ton filtre tient en temps reel.
   - Les DMIPS servent a justifier que le CPU est bien un Cortex-M4 hautes performances, mais la comparaison la plus utile reste le budget de cycles.

### Exemple rapide (a adapter)

Si `SystemCoreClock = 180000000` et `sampleRateHz = 16000`:

```
cycles_budget = 180000000 / 16000 = 11250 cycles/ech
```

Si `cycles_moyens = 900`:

```
charge_cpu_% = (900 / 11250) * 100 = 8%
```

Conclusion: le FIR consomme environ 8% du CPU, donc largement compatible avec le datasheet.
