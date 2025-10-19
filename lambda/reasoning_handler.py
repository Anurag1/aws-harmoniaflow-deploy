import sympy as sp, json, time
def lambda_handler(event, context):
    data = event.get("data", {}); rules = event.get("rules", {}); results={}
    for n,e in rules.items():
        expr=sp.sympify(e)
        for k,v in data.items(): expr=expr.subs(sp.Symbol(k),sum(v)/len(v))
        results[n]=float(expr.evalf())
    return {"timestamp": time.time(), "results": results}
