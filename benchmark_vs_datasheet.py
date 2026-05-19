"""Benchmark vs datasheet - STM32F446ZE.

Colle des lignes au format cle=valeur, par exemple:
firCyclesSum=987654
firBlocks=80
sampleRateHz=16000
AUDIO_BLOCK_SIZE=128
SystemCoreClock=168000000

Valeurs datasheet integrees:
- Frequence max CPU: 180 MHz
- Performance: 225 DMIPS, soit 1.25 DMIPS/MHz
"""

import sys

DATASHEET = {
    "cpu_max_hz": 180_000_000,
    "dmips": 225,
    "dmips_per_mhz": 1.25,
}

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
    sample_rate = data.get("sampleRateHz")

    fir_cycles_sum = data.get("firCyclesSum")
    fir_blocks = data.get("firBlocks")

    cycles_avg = None
    if fir_cycles_sum is not None and fir_blocks:
        cycles_avg = fir_cycles_sum / (fir_blocks * block_size)

    cycles_budget = None
    if sample_rate:
        cycles_budget = sys_clk / sample_rate

    cpu_load = None
    if cycles_avg is not None and cycles_budget:
        cpu_load = (cycles_avg / cycles_budget) * 100.0

    print("\n=== Benchmark vs Datasheet (STM32F446ZE) ===")
    print(f"SystemCoreClock: {sys_clk} Hz")
    if sample_rate is not None:
        print(f"sampleRateHz: {sample_rate} Hz")
    print(f"CPU max (datasheet): {DATASHEET['cpu_max_hz']} Hz")
    print(f"Perf datasheet: {DATASHEET['dmips']} DMIPS ({DATASHEET['dmips_per_mhz']} DMIPS/MHz)")

    if cycles_avg is not None:
        print(f"cycles_moyens: {cycles_avg:.2f} cycles/ech")
    if cycles_budget is not None:
        print(f"cycles_budget: {cycles_budget:.2f} cycles/ech")
    if cpu_load is not None:
        print(f"charge_cpu: {cpu_load:.2f} %")

    if cpu_load is not None:
        if cpu_load < 100.0:
            print("Conclusion: le FIR tient en temps reel (charge < 100%).")
        else:
            print("Conclusion: le FIR ne tient pas en temps reel (charge >= 100%).")

    print("\nNote: les DMIPS donnent un niveau de perf global. La comparaison la plus utile ici est le budget de cycles par echantillon.")


if __name__ == "__main__":
    main()
