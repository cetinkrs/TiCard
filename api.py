from fastapi import FastAPI
from motor import TiCardMotoru

app = FastAPI()
motor = TiCardMotoru()

@app.get("/")
def ana_sayfa():
    return {"mesaj": "TiCard API çalışıyor"}

@app.get("/desteler")
def desteleri_getir():
    return motor.deste_listesi_getir()