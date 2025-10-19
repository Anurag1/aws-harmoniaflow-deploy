import json, os, re, boto3, requests
from requests_aws4auth import AWS4Auth
s=boto3.Session(); c=s.get_credentials(); region=s.region_name or "us-east-1"
auth=AWS4Auth(c.access_key,c.secret_key,region,"neptune-db",session_token=c.token)
NEPTUNE_ENDPOINT=os.environ.get("NEPTUNE_ENDPOINT")

def parse_nl_to_gremlin(q):
    t=q.lower()
    if "related" in t or "depends" in t:
        w=re.findall(r"(\w+)",t)
        if len(w)>=2: return f"g.V('{w[0]}').outE('depends_on').inV().hasId('{w[-1]}').path()"
    if "datasets" in t: return "g.V().hasLabel('dataset').values('id')"
    if "rules" in t: return "g.V().hasLabel('rule').values('id')"
    if "influence" in t:
        m=re.findall(r"influence\s+(\w+)",t)
        if m: return f"g.V('{m[0]}').inE('depends_on').outV().path()"
    return "g.V().limit(5)"

def lambda_handler(event, context):
    q=event.get("query","")
    if not q: return {"error":"No query provided"}
    if not NEPTUNE_ENDPOINT: return {"error":"Missing NEPTUNE_ENDPOINT"}
    gq=parse_nl_to_gremlin(q)
    payload=json.dumps({"gremlin":gq})
    r=requests.post(f"https://{NEPTUNE_ENDPOINT}:8182/gremlin",data=payload,auth=auth,
                    headers={"Content-Type":"application/json"})
    try: data=r.json()
    except: data={"raw":r.text}
    return {"query":q,"gremlin":gq,"response":data}
