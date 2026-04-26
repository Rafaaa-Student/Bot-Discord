import sqlite3
import os
from datetime import date

# Path ke database
DB_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(DB_DIR, 'books.db')

def get_db_connection():
    """Create and return database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with books table, conversation history table, AI usage tracking table, and indexes"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            harga TEXT,
            deskripsi TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create conversation history table for AI memory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create AI usage tracking table (The Guard System)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_usage (
            user_id TEXT PRIMARY KEY,
            daily_count INTEGER DEFAULT 0,
            last_ask_date TEXT DEFAULT NULL
        )
    ''')
    
    # Create indexes for faster search
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_judul ON books(judul)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_deskripsi ON books(deskripsi)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversation_user ON conversations(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversation_created ON conversations(created_at)')
    
    conn.commit()
    conn.close()

def add_book(judul, harga, deskripsi, url):
    """Add a new book to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (judul, harga, deskripsi, url)
        VALUES (?, ?, ?, ?)
    ''', (judul, harga, deskripsi, url))
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return book_id

def get_books(limit=None, offset=0):
    """Get books from database with optional limit and offset"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute('SELECT * FROM books ORDER BY id DESC LIMIT ? OFFSET ?', (limit, offset))
    else:
        cursor.execute('SELECT * FROM books ORDER BY id DESC')
    
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return books

def search_books(keyword):
    """Search books by judul or deskripsi (case-insensitive)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    search_term = f'%{keyword}%'
    cursor.execute('''
        SELECT * FROM books 
        WHERE LOWER(judul) LIKE LOWER(?) 
           OR LOWER(deskripsi) LIKE LOWER(?)
        ORDER BY id DESC
    ''', (search_term, search_term))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results

def get_book_count():
    """Get total number of books in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM books')
    count = cursor.fetchone()['count']
    conn.close()
    return count

def book_exists(judul):
    """Check if a book with given judul already exists"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM books WHERE judul = ?', (judul,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_random_book():
    """Get a random book from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books ORDER BY RANDOM() LIMIT 1')
    book = cursor.fetchone()
    conn.close()
    return dict(book) if book else None

# ==================== CONVERSATION MEMORY FUNCTIONS ====================
def save_conversation(user_id, role, content):
    """Save a conversation message to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (user_id, role, content)
        VALUES (?, ?, ?)
    ''', (user_id, role, content))
    conn.commit()
    conn.close()

def get_conversation_history(user_id, limit=10):
    """Get conversation history for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role, content, created_at 
        FROM conversations 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (user_id, limit))
    history = [dict(row) for row in cursor.fetchall()]
    conn.close()
    # Reverse to get chronological order
    return history[::-1]

def clear_conversation(user_id):
    """Clear conversation history for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM conversations WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

# ==================== AI USAGE TRACKING FUNCTIONS (The Guard System) ====================
def get_ai_usage(user_id):
    """Get AI usage data for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT daily_count, last_ask_date FROM ai_usage WHERE user_id = ?', (str(user_id),))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {'daily_count': result['daily_count'], 'last_ask_date': result['last_ask_date']}
    return {'daily_count': 0, 'last_ask_date': None}

def check_ai_limit(user_id, admin_id, daily_limit=25):
    """Check if user has reached daily AI limit. Returns (can_use, remaining, message)"""
    # Admin bypass
    if str(user_id) == str(admin_id):
        return True, float('inf'), "Admin - unlimited access"
    
    usage = get_ai_usage(user_id)
    today = str(date.today())
    
    # Reset count if it's a new day
    if usage['last_ask_date'] != today:
        reset_ai_count(user_id)
        return True, daily_limit, f"New day! Reset to {daily_limit} uses"
    
    remaining = daily_limit - usage['daily_count']
    if remaining <= 0:
        return False, 0, f"Daily limit reached ({daily_limit} uses). Try again tomorrow!"
    
    return True, remaining, f"{remaining} uses remaining today"

def increment_ai_count(user_id):
    """Increment AI usage count for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = str(date.today())
    
    # Check if user exists
    cursor.execute('SELECT daily_count FROM ai_usage WHERE user_id = ?', (str(user_id),))
    result = cursor.fetchone()
    
    if result:
        # Check if it's a new day
        cursor.execute('SELECT last_ask_date FROM ai_usage WHERE user_id = ?', (str(user_id),))
        last_date = cursor.fetchone()['last_ask_date']
        
        if last_date != today:
            # Reset for new day
            cursor.execute('UPDATE ai_usage SET daily_count = 1, last_ask_date = ? WHERE user_id = ?', (today, str(user_id)))
        else:
            # Increment
            cursor.execute('UPDATE ai_usage SET daily_count = daily_count + 1 WHERE user_id = ?', (str(user_id),))
    else:
        # Create new entry
        cursor.execute('INSERT INTO ai_usage (user_id, daily_count, last_ask_date) VALUES (?, 1, ?)', (str(user_id), today))
    
    conn.commit()
    conn.close()

def reset_ai_count(user_id):
    """Reset AI usage count for a user (called on new day)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = str(date.today())
    cursor.execute('UPDATE ai_usage SET daily_count = 0, last_ask_date = ? WHERE user_id = ?', (today, str(user_id)))
    conn.commit()
    conn.close()

def get_remaining_uses(user_id, admin_id, daily_limit=25):
    """Get remaining AI uses for a user"""
    can_use, remaining, message = check_ai_limit(user_id, admin_id, daily_limit)
    return remaining if can_use else 0

# Initialize database on import
if __name__ != '__main__':
    init_db()
