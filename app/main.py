from pathlib import Path
import random

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Card

app = FastAPI(title="Flashcard Vault")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    cards = db.query(Card).order_by(Card.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "cards": cards})


@app.get("/add")
def add_form(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


@app.post("/add")
def add_card(
    word: str = Form(...),
    translation: str = Form(...),
    example: str = Form(""),
    db: Session = Depends(get_db),
):
    card = Card(
        word=word.strip(),
        translation=translation.strip(),
        example=example.strip() if example else None,
    )
    db.add(card)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card:
        db.delete(card)
        db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.get("/quiz")
def quiz(request: Request, db: Session = Depends(get_db)):
    cards = db.query(Card).all()
    if not cards:
        return templates.TemplateResponse(
            "quiz.html",
            {
                "request": request,
                "card": None,
                "result": None,
                "message": "Додай хоча б 1 слово 🙂",
            },
        )

    card = random.choice(cards)
    return templates.TemplateResponse(
        "quiz.html", {"request": request, "card": card, "result": None, "message": None}
    )


@app.post("/quiz")
def quiz_check(
    request: Request,
    card_id: int = Form(...),
    answer: str = Form(...),
    db: Session = Depends(get_db),
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        return RedirectResponse(url="/quiz", status_code=303)

    user = (answer or "").strip().lower()
    correct = card.translation.strip().lower()

    ok = user == correct
    result = {"ok": ok, "user": answer.strip(), "correct": card.translation}

    return templates.TemplateResponse(
        "quiz.html", {"request": request, "card": card, "result": result, "message": None}
    )
