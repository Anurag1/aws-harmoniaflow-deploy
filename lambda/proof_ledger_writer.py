import boto3, json, time, hashlib
dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table('harmonia_proof_ledger')
def lambda_handler(event, context):
    r={"timestamp":str(time.time()),"hash":hashlib.sha256(json.dumps(event).encode()).hexdigest(),"payload":json.dumps(event)}
    table.put_item(Item=r)
    return {"status":"logged","hash":r["hash"]}
