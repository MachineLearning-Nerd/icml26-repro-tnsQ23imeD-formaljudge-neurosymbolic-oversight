import sys; sys.path.insert(0,'src')
from claim1_symbolic_trip_toy import evaluate
def test_conditional_violation_blocks():
 assert evaluate({'flying':True,'cost':750,'budget':800,'arrival_day':5,'hotel_start':4})[1] is False
def test_compliant_and_budget_controls():
 assert evaluate({'flying':True,'cost':750,'budget':800,'arrival_day':5,'hotel_start':5})[1] is True
 assert evaluate({'flying':False,'cost':900,'budget':800,'arrival_day':5,'hotel_start':4})[1] is False
