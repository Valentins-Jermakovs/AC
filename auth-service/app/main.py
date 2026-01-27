# demonstrējuma programma autentifikācijas pakalpojumam

# lai palaist šo programmu, instalē nepieciešamas atkarības virtuālajā vidē
# un izpildi komandu [fastapi dev main.py]

from fastapi import FastAPI

app = FastAPI()

# Vienkāršs saknes maršruts - tests
@app.get("/")
async def root():
    return {"message": "Hello World"}