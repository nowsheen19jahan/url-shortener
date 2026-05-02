from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
import random
import string

from app.db.database import engine, Base, get_db
from app.models.url import URL
from app.schemas.url import URLCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Helper Function for Regeneration of short code in case of duplicate
def generate_unique_short_code(db: Session):
    while True:

        short_code = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=6
            )
        )

        existing_code = db.query(URL).filter(
            URL.short_code == short_code
        ).first()

        if not existing_code:
            return short_code



@app.get("/")
def home():
    return {"message": "URL Shortener Backend Running"}


@app.post("/shorten")
def create_short_url(
    

    request: URLCreate,
    db: Session = Depends(get_db)
):
    # if the same url is in db , we don't generate new short code, rather ouput the existing code
    #  IDEMPOTENCY
    existing_url = db.query(URL).filter(
    URL.original_url == request.original_url
    ).first()

    if existing_url:
        return {
            "original_url": existing_url.original_url,
            "short_code": existing_url.short_code
        }
    
    short_code = short_code = generate_unique_short_code(db)
    

    new_url = URL(
        original_url=request.original_url,
        short_code=short_code
    )

    db.add(new_url)

    db.commit()

    db.refresh(new_url)

    return {
        "original_url": new_url.original_url,
        "short_code": new_url.short_code
    }

@app.get("/{short_code}")
def redirect_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    url_entry = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if not url_entry:
        return {"error": "Short URL not found"}

    return RedirectResponse(url=url_entry.original_url)