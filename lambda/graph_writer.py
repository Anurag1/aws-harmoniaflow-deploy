import json, os, boto3, requests
from requests_aws4auth import AWS4Auth
s=boto3.Session(); c=s.get_credentials(); region=s.region_name or "us-east-1"
auth=AWS4Auth(c.access_key,c.secret_key,region,"neptune-db",session_token=c.token)
NEPTUNE_ENDPOINT=os.environ.get("NEPTUNE_ENDPOINT")
def lambda_handler(event, context):
    if not NEPTUNE_ENDPOINT: return {"error":"Missing NEPTUNE_ENDPOINT"}
    g=[]
    data=event.get("data",{}); rules=event.get("rules",{}); results=event.get("results",{})
    for rule,expr in rules.items():
        for var in data.keys():
            g.append(f"g.addV('dataset').property('id','{var}')")
            g.append(f"g.addV('rule').property('id','{rule}')")
            g.append(f"g.addE('depends_on').from(g.V('{rule}')).to(g.V('{var}'))")
        g.append(f"g.addV('result').property('id','{rule}_result').property('value','{results.get(rule)}')")
    payload="\n".join(g)
    r=requests.post(f"https://{NEPTUNE_ENDPOINT}:8182/gremlin",data=payload,auth=auth,
                    headers={"Content-Type":"application/vnd.gremlin-v2.0+json"})
    return {"status":"graph_updated","gremlin_count":len(g),"response":r.text[:200]}
