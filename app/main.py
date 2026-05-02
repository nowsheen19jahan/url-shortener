from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
import random
import string

from app.db.database import engine, Base, get_db
from app.models.url import URL
from app.schemas.url import URLCreate
from urllib.parse import urlparse

app = FastAPI()

# Middleware 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def is_valid_url(url: str):
    try:
        result = urlparse(url)

        # must have scheme + domain
        if not result.scheme or not result.netloc:
            return False

        # only allow http/https
        if result.scheme not in ["http", "https"]:
            return False

        # domain must be meaningful
        if len(result.netloc) < 3:
            return False

        return True

    except:
        return False

@app.get("/")
def home():
    return {"message": "URL Shortener Backend Running"}


@app.post("/shorten")
def create_short_url(
    

    request: URLCreate,
    db: Session = Depends(get_db)
):
    if not is_valid_url(request.original_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid URL format"
        )

    # if the same url is in db , we don't generate new short code, rather ouput the existing code
    #  IDEMPOTENCY


    existing_url = db.query(URL).filter(
    URL.original_url == request.original_url
    ).first()

    if existing_url:
        return {
            "original_url": existing_url.original_url,
            "short_code": existing_url.short_code,
            "short_url": f"https://url-shortener-rkyb.onrender.com/{existing_url.short_code}"
        }
    
    short_code = generate_unique_short_code(db)
    

    new_url = URL(
        original_url=request.original_url,
        short_code=short_code
    )

    db.add(new_url)

    db.commit()

    db.refresh(new_url)

    return {
        "original_url": new_url.original_url,
        "short_code": short_code,
        "short_url": f"https://url-shortener-rkyb.onrender.com/{short_code}"
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
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    url_entry.clicks += 1

    db.commit()

    return RedirectResponse(url=url_entry.original_url)