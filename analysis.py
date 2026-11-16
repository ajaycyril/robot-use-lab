"""Reanalyse author-reported PEAR results. Python standard library only."""
import csv, json, math, statistics
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def wilson(k, n, z=1.959963984540054):
    if n <= 0 or not 0 <= k <= n:
        raise ValueError("Require 0 <= successes <= total and total > 0")
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n))/d
    r = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return [100*(c-r), 100*(c+r)]

def mixture(p, original, changed):
    if not 0 <= p <= 1: raise ValueError("Mix must be in [0,1]")
    return (1-p)*original + p*changed

def crossover(a0, a1, b0, b1):
    denominator = (a1-a0)-(b1-b0)
    if denominator == 0: return None
    p = (b0-a0)/denominator
    return p if 0 <= p <= 1 else None

def analyse():
    data = json.loads((ROOT/"data/reported.json").read_text())
    with (ROOT/"data/real_trials.csv").open() as handle:
        rows = list(csv.DictReader(handle))
    for r in rows:
        for k in ["base_success","libero_success","pear_success","pear_rounds","trial"]:
            r[k] = int(r[k])
    assert len(rows) == 30 and len({(r["scene"],r["trial"]) for r in rows}) == 30
    totals = {k:sum(r[k] for r in rows) for k in ["base_success","libero_success","pear_success"]}
    assert list(totals.values()) == [0,7,18], totals
    failures = dict(Counter(r["pear_failure"] for r in rows if not r["pear_success"]))
    assert sum(failures.values()) == 12
    a,b = data["conditions"][:2]
    p = crossover(a["pear"],b["pear"],a["pi05"],b["pi05"])
    trials = {
        "n":len(rows), "successes":totals, "final_success_percent":60,
        "descriptive_wilson_95_percent":wilson(18,30),
        "interval_caveat":"Assumes independent Bernoulli trials; these 30 trials repeat 15 scenes/objects. This is descriptive, not a population guarantee.",
        "final_failures":failures,
        "libero_to_final":{"both_success":sum(r["libero_success"] and r["pear_success"] for r in rows),
                          "new_success":sum(not r["libero_success"] and r["pear_success"] for r in rows),
                          "lost_success":sum(r["libero_success"] and not r["pear_success"] for r in rows)},
        "successful_rounds_median":statistics.median(r["pear_rounds"] for r in rows if r["pear_success"])
    }
    result = {
        "status":"Completed reanalysis of published data; no model inference or training performed.",
        "workload_mix":{"crossover_percent":100*p,"caveat":"Illustrative two-condition weighting of cross-source aggregates; not a deployment threshold or causal experiment.",
                        "at_50_percent":{"pear":mixture(.5,a["pear"],b["pear"]),"pi05":mixture(.5,a["pi05"],b["pi05"])}},
        "real_trials":trials,
        "latency_sensitivity_seconds":{device:{effort:val["tokens"]/speed for effort,val in data["effort"].items() if isinstance(val,dict)} for device,speed in data["decode"].items() if isinstance(speed,(int,float))},
        "latency_caveat":"Arithmetic sensitivity only. BF16 mean reasoning length / NVFP4 decode rate; excludes prefill, vision, movement, networking, and quantization-induced longer reasoning.",
        "full_robodojo":{"micro_percent":100*21/540,"reported_dimension_macro_percent":5.5,"context_exhaustion_percent":100*370/540}
    }
    return result

if __name__ == "__main__":
    result=analyse()
    out=ROOT/"results";out.mkdir(exist_ok=True)
    (out/"analysis.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

