# TP2 - Modeles Django : Bibliotheque

A Django library management system built as part of the Django Web course.

## Models

- **Auteur** - Author information (name, first name, birth date)
- **Livre** - Book catalog (title, ISBN, pages, language, resume)
- **Genre** - Book genres (many-to-many with books)
- **Emprunt** - Book loans/borrowing records
- **FicheAuteur** - Optional author profile (biography, website)
- **Emprunteur** - Library members (in `membres` app)

## Setup

```bash
# Create virtual environment
uv venv
.venv\Scripts\activate

# Install dependencies
uv pip install Django

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## Project Structure

- `config/` - Django project settings
- `bibliotheque/` - Library app (books, authors, genres, loans)
- `membres/` - Members app
