from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select
from typing import List
import random
try:
    from models import Blacklist, Draw, Participant
except ImportError:
    from app.models import Blacklist, Draw, Participant
app = FastAPI()


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield 

@app.post("/participants", response_model=Participant)
def add_participant(participant: Participant):
    with Session(engine) as session:
        session.add(participant)
        session.commit()
        session.refresh(participant)
        return participant


@app.post("/participants/{participant_id}/blacklist/{blocked_id}")
def add_to_blacklist(participant_id: int, blocked_id: int):
    with Session(engine) as session:
        blacklist_entry = Blacklist(participant_id=participant_id, blocked_id=blocked_id)
        session.add(blacklist_entry)
        session.commit()
        return {"message": "Added to blacklist"}


@app.get("/draw")
def perform_draw():
    with Session(engine) as session:
        participants = session.exec(select(Participant)).all()
        if len(participants) < 2:
            raise HTTPException(status_code=400, detail="Not enough participants")

        names = [p.name for p in participants]
        ids = {p.name: p.id for p in participants}
        blacklist_map = {p.name: set() for p in participants}

        for bl in session.exec(select(Blacklist)).all():
            giver = session.get(Participant, bl.participant_id).name
            receiver = session.get(Participant, bl.blocked_id).name
            blacklist_map[giver].add(receiver)

        for _ in range(100):  # try 100 times max
            shuffled = names[:]
            random.shuffle(shuffled)
            valid = True
            for giver, receiver in zip(names, shuffled):
                if giver == receiver or receiver in blacklist_map[giver]:
                    valid = False
                    break
            if valid:
                break
        else:
            raise HTTPException(status_code=400, detail="No valid draw found")

        draws = []
        for giver, receiver in zip(names, shuffled):
            draw = Draw(giver=giver, receiver=receiver)
            session.add(draw)
            draws.append({"giver": giver, "receiver": receiver})

        session.commit()
        return draws


@app.get("/draws", response_model=List[Draw])
def get_last_draws():
    with Session(engine) as session:
        results = session.exec(select(Draw).order_by(Draw.created_at.desc()).limit(5)).all()
        return results
