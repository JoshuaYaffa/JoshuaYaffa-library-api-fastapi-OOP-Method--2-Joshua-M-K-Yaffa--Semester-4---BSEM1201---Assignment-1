from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio

app = FastAPI(title="Limkokwing Library REST API – University Library Resource Manage " \
"Developed by : Joshua M K Yaffa")

# ----------------------------
# Users
# ----------------------------
users = [
    {"id": 1, "name": "Joshua Yaffa"},
    {"id": 2, "name": "Josephine Ashley"},
    {"id": 3, "name": "Phinney Ashley"},
    {"id": 4, "name": "Thomas Ashley"},
    {"id": 5, "name": "Victor Ashley"},
    {"id": 6, "name": "Elizabeth Ashley"},
    {"id": 7, "name": "Elizabeth Lightfoot-Taylor"},
    {"id": 8, "name": "Jestina Ashley"},
    {"id": 9, "name": "Ibrahim Conteh"},
    {"id": 10, "name": "Paul Samura"}
]

# ----------------------------
# Books (30)
# ----------------------------
books = [
    {"id": 1, "title": "Python Basics", "author": "Joshua Yaffa", "category": "Programming", "available": True},
    {"id": 2, "title": "Advanced Python", "author": "Josephine Ashley", "category": "Programming", "available": True},
    {"id": 3, "title": "Data Science Intro", "author": "Phinney Ashley", "category": "Data", "available": True},
    {"id": 4, "title": "Machine Learning", "author": "Thomas Ashley", "category": "AI", "available": True},
    {"id": 5, "title": "AI Fundamentals", "author": "Victor Ashley", "category": "AI", "available": True},
    {"id": 6, "title": "Database Systems", "author": "Elizabeth Ashley", "category": "Database", "available": True},
    {"id": 7, "title": "Web Development", "author": "Elizabeth Lightfoot-Taylor", "category": "Web", "available": True},
    {"id": 8, "title": "Networking Basics", "author": "Jestina Ashley", "category": "Networking", "available": True},
    {"id": 9, "title": "Cyber Security", "author": "Ibrahim Conteh", "category": "Security", "available": True},
    {"id": 10, "title": "Cloud Computing", "author": "Paul Samura", "category": "Cloud", "available": True},
    {"id": 11, "title": "Operating Systems", "author": "Michael Charm", "category": "Systems", "available": True},
    {"id": 12, "title": "Software Engineering", "author": "Pamela Conteh", "category": "Software", "available": True},
    {"id": 13, "title": "Mobile App Dev", "author": "Ngiika Ashley", "category": "Mobile", "available": True},
    {"id": 14, "title": "Algorithms", "author": "Samuel Ashley", "category": "CS", "available": True},
    {"id": 15, "title": "Data Structures", "author": "Hannah Ashley", "category": "CS", "available": True},
    {"id": 16, "title": "Information Systems", "author": "Mediya Kamara", "category": "IS", "available": True},
    {"id": 17, "title": "Digital Literacy", "author": "Isata Yaffa", "category": "Education", "available": True},
    {"id": 18, "title": "ICT in Education", "author": "Maybel Robert", "category": "Education", "available": True},
    {"id": 19, "title": "Business Computing", "author": "Ms Robert", "category": "Business", "available": True},
    {"id": 20, "title": "E-Commerce", "author": "Kadie Yaffa", "category": "Business", "available": True},
    {"id": 21, "title": "Digital Marketing", "author": "Aminata Yaffa", "category": "Marketing", "available": True},
    {"id": 22, "title": "Project Management", "author": "Yusif Yaffa", "category": "Management", "available": True},
    {"id": 23, "title": "Computer Graphics", "author": "Mohamed Yaffa", "category": "Graphics", "available": True},
    {"id": 24, "title": "Game Development", "author": "Amie Yaffa", "category": "Game Dev", "available": True},
    {"id": 25, "title": "Robotics", "author": "Musa Yaffa", "category": "Engineering", "available": True},
    {"id": 26, "title": "Embedded Systems", "author": "Muhammadu Yaffa", "category": "Engineering", "available": True},
    {"id": 27, "title": "Computer Architecture", "author": "Abubakarr Yaffa", "category": "Hardware", "available": True},
    {"id": 28, "title": "IT Support", "author": "Foday Conteh", "category": "Support", "available": True},
    {"id": 29, "title": "Networking Advanced", "author": "Ibrahim Kamara", "category": "Networking", "available": True},
    {"id": 30, "title": "System Administration", "author": "Landi Bassie", "category": "Systems", "available": True}
]

borrow_records = []
FINE_PER_DAY = 1000

# ----------------------------
# Models
# ----------------------------
class BorrowRequest(BaseModel):
    user_id: int
    book_id: int

# ----------------------------
# Root
# ----------------------------
@app.get("/")
async def root():
    return {"message": "Library API is running. Go to /docs"}

# ----------------------------
# GET USERS
# ----------------------------
@app.get("/users")
async def get_users():
    return users

# ----------------------------
# GET BOOKS
# ----------------------------
@app.get("/books", response_model=List[dict])
async def get_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    category: Optional[str] = None
):
    await asyncio.sleep(0.2)

    result = books.copy()

    if title:
        result = [b for b in result if title.lower() in b["title"].lower()]
    if author:
        result = [b for b in result if author.lower() in b["author"].lower()]
    if category:
        result = [b for b in result if category.lower() in b["category"].lower()]

    return result

# ----------------------------
# BORROW
# ----------------------------
@app.post("/borrow")
async def borrow_book(request: BorrowRequest):
    await asyncio.sleep(0.5)

    # Check user
    user = next((u for u in users if u["id"] == request.user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check book
    book = next((b for b in books if b["id"] == request.book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book["available"]:
        raise HTTPException(status_code=400, detail="Book not available")

    book["available"] = False

    due_date = datetime.now() + timedelta(days=7)

    borrow_records.append({
        "user_id": request.user_id,
        "book_id": request.book_id,
        "due_date": due_date,
        "returned": False
    })

    return {
        "message": "Book borrowed successfully",
        "due_date": due_date.strftime("%Y-%m-%d")
    }

# ----------------------------
# RETURN
# ----------------------------
@app.post("/return")
async def return_book(request: BorrowRequest):
    await asyncio.sleep(0.5)

    record = next((r for r in borrow_records if r["book_id"] == request.book_id and not r["returned"]), None)

    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    record["returned"] = True

    book = next((b for b in books if b["id"] == request.book_id), None)
    if book:
        book["available"] = True

    return {"message": "Book returned successfully"}

# ----------------------------
# OVERDUE
# ----------------------------
@app.get("/users/{user_id}/overdue")
async def get_overdue_books(user_id: int):
    await asyncio.sleep(0.2)

    overdue_list = []

    for record in borrow_records:
        if record["user_id"] == user_id and not record["returned"]:
            overdue_days = (datetime.now() - record["due_date"]).days

            if overdue_days > 0:
                fine = overdue_days * FINE_PER_DAY
                overdue_list.append({
                    "book_id": record["book_id"],
                    "days_overdue": overdue_days,
                    "fine": fine
                })

    return {"overdue_books": overdue_list}

# ----------------------------
# PUT
# ----------------------------
@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: dict):
    for book in books:
        if book["id"] == book_id:
            book.update(updated_book)
            return {"message": "Book updated", "book": book}

    raise HTTPException(status_code=404, detail="Book not found")

# ----------------------------
# PATCH
# ----------------------------
@app.patch("/books/{book_id}")
async def patch_book(book_id: int, updated_fields: dict):
    for book in books:
        if book["id"] == book_id:
            for key in updated_fields:
                if key in book:
                    book[key] = updated_fields[key]
            return {"message": "Book patched", "book": book}

    raise HTTPException(status_code=404, detail="Book not found")

# ----------------------------
# DELETE
# ----------------------------
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(i)
            return {"message": "Book deleted"}

    raise HTTPException(status_code=404, detail="Book not found")