"""Finite FormalJudge-style atomic-fact composition toy; not an LLM benchmark."""
import argparse, hashlib, json, pathlib

def evaluate(case):
    # Source toy example: budget plus conditional flight/hotel-date rule.
    facts = {"flying": case["flying"], "within_budget": case["cost"] <= case["budget"],
             "hotel_on_arrival": case["hotel_start"] >= case["arrival_day"]}
    # Deterministic composition of extracted atomic facts (source §Formal-of-Thought).
    compliant = facts["within_budget"] and ((not facts["flying"]) or facts["hotel_on_arrival"])
    violated = []
    if not facts["within_budget"]: violated.append("budget")
    if facts["flying"] and not facts["hotel_on_arrival"]: violated.append("flight_implies_hotel_on_arrival")
    return facts, compliant, violated

def main(out):
    out=pathlib.Path(out); out.mkdir(parents=True,exist_ok=True)
    cases=[
      {"id":"source_style_conditional_violation","flying":True,"cost":750,"budget":800,"arrival_day":5,"hotel_start":4,"expected":False},
      {"id":"compliant_flight","flying":True,"cost":750,"budget":800,"arrival_day":5,"hotel_start":5,"expected":True},
      {"id":"budget_control","flying":False,"cost":900,"budget":800,"arrival_day":5,"hotel_start":4,"expected":False},
    ]
    rows=[]
    for c in cases:
      facts, verdict, violations=evaluate(c); assert verdict==c['expected']
      rows.append({**c,"atomic_facts":facts,"formal_verdict":"PASS" if verdict else "BLOCK","violations":violations})
    raw={"method":"finite propositional composition of source-style atomic facts","cases":rows}
    (out/'raw.json').write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
    summary={"verdict":"toy","n_cases":3,"accuracy_against_constructed_labels":1.0,"source_case_detected":rows[0]['formal_verdict']=="BLOCK","scope":"Deterministic finite logical-composition toy preserving the source conditional trip constraint; no LLM semantic extraction, Dafny/Z3, Claude judge, or benchmark accuracy."}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    protocol={"source_locations":"example_paper.tex lines 349-355 (trip conditional); 364-390 (atomic facts/composition)","controls":["compliant flight","budget violation"],"metric":"exact agreement with three constructed propositional labels","compute":"local CPU"}
    (out/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2,sort_keys=True)+'\n')
    files=['raw.json','summary.json','PROTOCOL.json']; (out/'SHA256SUMS').write_text(''.join(hashlib.sha256((out/f).read_bytes()).hexdigest()+'  '+f+'\n' for f in files))
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--out',default='outputs/claim1_symbolic_trip_toy'); main(p.parse_args().out)
