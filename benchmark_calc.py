"""Benchmark FIR - Calcul simple a partir des valeurs debug.

Colle des lignes au format cle=valeur, par exemple:
firCyclesLast=12345
firCyclesPerSample=96
firCyclesMin=12000
firCyclesMax=13000
firCyclesSum=987654
firBlocks=80
sampleRateHz=16000
AUDIO_BLOCK_SIZE=128
SystemCoreClock=168000000

Tu peux laisser des cles manquantes; le script calcule ce qu'il peut.
"""

import sys

DEFAULTS = {
    "AUDIO_BLOCK_SIZE": 128,
    "SystemCoreClock": 168_000_000,
}


def parse_kv(text):
    data = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().replace("_", "")
        try:
            if "." in value:
                data[key] = float(value)
            else:
                data[key] = int(value)
        except ValueError:
            pass
    return data


def main():
    print("Colle tes valeurs (cle=valeur). Termine par une ligne vide, puis Entrer:")
    lines = []
    while True:
        line = sys.stdin.readline()
        if not line or line.strip() == "":
            break
        lines.append(line)

    data = DEFAULTS.copy()
    data.update(parse_kv("".join(lines)))

    block_size = int(data.get("AUDIO_BLOCK_SIZE", 128))
    sys_clk = int(data.get("SystemCoreClock", 168_000_000))

    fir_cycles_last = data.get("firCyclesLast")
    fir_cycles_per_sample = data.get("firCyclesPerSample")
    fir_cycles_min = data.get("firCyclesMin")
    fir_cycles_max = data.get("firCyclesMax")
    fir_cycles_sum = data.get("firCyclesSum")
    fir_blocks = data.get("firBlocks")
    sample_rate = data.get("sampleRateHz")

    cycles_avg = None
    if fir_cycles_sum is not None and fir_blocks:
        cycles_avg = fir_cycles_sum / (fir_blocks * block_size)

    usec_per_block = None
    if fir_cycles_last is not None and sys_clk:
        usec_per_block = (fir_cycles_last * 1_000_000) / sys_clk

    print("\n=== Benchmark FIR ===")
    print(f"SystemCoreClock: {sys_clk} Hz")
    print(f"AUDIO_BLOCK_SIZE: {block_size}")
    if sample_rate is not None:
        print(f"sampleRateHz: {sample_rate} Hz")
    if fir_cycles_last is not None:
        print(f"firCyclesLast: {fir_cycles_last} cycles")
    if fir_cycles_per_sample is not None:
        print(f"firCyclesPerSample: {fir_cycles_per_sample} cycles/ech")
    if cycles_avg is not None:
        print(f"cycles_moyens: {cycles_avg:.2f} cycles/ech")
    if usec_per_block is not None:
        print(f"temps_bloc (dernier): {usec_per_block:.2f} us")
    if fir_cycles_min is not None:
        print(f"firCyclesMin: {fir_cycles_min} cycles")
    if fir_cycles_max is not None:
        print(f"firCyclesMax: {fir_cycles_max} cycles")

    print("\nSi une valeur n'apparait pas, verifie que tu l'as collee.")


if __name__ == "__main__":
    main()
