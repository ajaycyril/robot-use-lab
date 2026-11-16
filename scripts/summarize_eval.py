"""Summarize genuine PEAR JSONL output without treating absent/partial runs as benchmarks."""
import argparse, json, statistics
from collections import defaultdict
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("records",type=Path)
p.add_argument("--expected",type=int,default=80)
a=p.parse_args()
groups=defaultdict(list); uids=set()
for line in a.records.read_text().splitlines():
    if not line.strip(): continue
    r=json.loads(line)
    uid=r["uid"]
    if uid in uids: raise ValueError(f"Duplicate trajectory UID: {uid}")
    uids.add(uid)
    score=r["score"]
    if not isinstance(score,(int,float)) or score not in (0,1):
        raise ValueError("Expected binary success score; do not silently label partial credit as success")
    groups[str(r["data_source"])].append(r)
n=sum(map(len,groups.values()))
if not n: raise ValueError("No completed trajectories")
result={"status":"complete" if n==a.expected else "partial_or_unexpected_count",
        "episodes":n,"expected":a.expected,
        "warning":"Perturbation groups are taken from upstream data_source. Do not infer per-episode pairing from UID alone.",
        "by_group":{k:{"n":len(v),"success_percent":100*statistics.mean(x["score"] for x in v),
                       "mean_rounds":statistics.mean(x["num_turns"] for x in v)} for k,v in sorted(groups.items())}}
print(json.dumps(result,indent=2))

