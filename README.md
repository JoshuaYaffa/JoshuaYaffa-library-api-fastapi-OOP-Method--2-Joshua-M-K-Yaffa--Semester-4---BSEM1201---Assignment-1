# Limkokwing Library REST API

## Description

This project is a RESTful API developed using Python and FastAPI to manage a digital library system. It allows users to search for books, borrow and return them, and track overdue items and fines.

## Features

* Search books by title, author, or category
* Borrow and return books
* Track overdue books and fines
* Manage books (PUT, PATCH, DELETE)
* Multi-user support using asynchronous programming

## Technologies Used

* Python
* FastAPI
* Uvicorn
* Swagger UI

## How to Run

```bash
uvicorn main:app --reload
```

## API Endpoints

* GET /books
* GET /users
* POST /borrow
* POST /return
* GET /users/{user_id}/overdue
* PUT /books/{id}
* PATCH /books/{id}
* DELETE /books/{id}

## SDG Alignment

This project supports Sustainable Development Goal 4 (Quality Education) by improving access to learning resources through digital library services.
