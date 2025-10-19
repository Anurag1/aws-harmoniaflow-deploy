import sympy as sp, time
def lambda_handler(event, context):
    rules=event.get("rules",{}); res=[]
    for e in rules.values():
        try: s=sp.simplify(sp.sympify(e)-sp.sympify(e)); res.append(abs(float(s)) if s.is_number else 0)
        except: res.append(1)
    score=1-sum(res)/(len(res)+1e-6)
    return {"timestamp": time.time(), "equilibrium_score": score}
