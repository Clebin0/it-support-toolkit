from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from support_toolkit import collect,recommendations

app=FastAPI(title="IT Support Toolkit",version="2.0.0")

@app.get("/",response_class=HTMLResponse)
def home():
    with open("frontend.html","r",encoding="utf-8") as f: return f.read()

@app.get("/health")
def health(): return {"status":"ok","version":"2.0.0"}

@app.get("/diagnostic")
def diagnostic():
    data=collect()
    data["recommendations"]=recommendations(data)
    return data
