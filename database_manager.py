# codesnap/database_manager.py

import sqlite3
import os

DB_FILE = os.path.join("database", "snippets.db")
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Initializes and upgrades the database schema if necessary."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            language TEXT NOT NULL,
            tags TEXT,
            code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # --- NEW: Safely add the is_favorite column if it doesn't exist ---
    cursor.execute("PRAGMA table_info(snippets)")
    columns = [column['name'] for column in cursor.fetchall()]
    if 'is_favorite' not in columns:
        print("Upgrading database: Adding 'is_favorite' column...")
        cursor.execute("ALTER TABLE snippets ADD COLUMN is_favorite INTEGER DEFAULT 0")
    
    conn.commit()
    conn.close()
    print("Database initialized and up-to-date.")


# --- NEW: Function to toggle the favorite status of a snippet ---
def toggle_favorite_status(snippet_id):
    conn = get_db_connection()
    # First, get the current status
    current_status = conn.execute(
        "SELECT is_favorite FROM snippets WHERE id = ?", (snippet_id,)
    ).fetchone()['is_favorite']
    
    # Flip the status (0 becomes 1, 1 becomes 0)
    new_status = 1 - current_status
    
    conn.execute(
        "UPDATE snippets SET is_favorite = ? WHERE id = ?",
        (new_status, snippet_id)
    )
    conn.commit()
    conn.close()
    return new_status

def get_all_snippets():
    conn = get_db_connection()
    snippets = conn.execute("SELECT id, title, language, tags, is_favorite FROM snippets ORDER BY title ASC").fetchall()
    conn.close()
    return snippets

# --- NEW: Function to get only favorite snippets ---
def get_favorite_snippets():
    conn = get_db_connection()
    snippets = conn.execute("SELECT id, title, language, tags, is_favorite FROM snippets WHERE is_favorite = 1 ORDER BY title ASC").fetchall()
    conn.close()
    return snippets

def get_snippet_by_id(snippet_id):
    conn = get_db_connection()
    snippet = conn.execute("SELECT * FROM snippets WHERE id = ?", (snippet_id,)).fetchone()
    conn.close()
    return snippet

# --- Other functions (add, update, delete, search) remain largely the same ---

def add_snippet(title, language, tags, code):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO snippets (title, language, tags, code) VALUES (?, ?, ?, ?)",
        (title, language, tags, code)
    )
    conn.commit()
    conn.close()
    
def update_snippet(snippet_id, title, language, tags, code):
    conn = get_db_connection()
    conn.execute(
        "UPDATE snippets SET title = ?, language = ?, tags = ?, code = ? WHERE id = ?",
        (title, language, tags, code, snippet_id)
    )
    conn.commit()
    conn.close()

def delete_snippet(snippet_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
    conn.commit()
    conn.close()

def search_snippets(query, favorites_only=False):
    conn = get_db_connection()
    search_term = f"%{query}%"
    
    base_query = "SELECT id, title, language, tags, is_favorite FROM snippets WHERE (title LIKE ? OR tags LIKE ? OR language LIKE ?)"
    params = [search_term, search_term, search_term]

    if favorites_only:
        base_query += " AND is_favorite = 1"
        
    base_query += " ORDER BY title ASC"

    snippets = conn.execute(base_query, params).fetchall()
    conn.close()
    return snippets