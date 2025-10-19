import json,subprocess
p=open("sample_payload.json").read()
r=subprocess.run(["python3","../lambda/reasoning_handler.py"],input=p.encode(),capture_output=True)
print(r.stdout.decode())
