import aiosqlite
import json
from datetime import datetime

async def init_db():
    async with aiosqlite.connect('court_cases.db') as db:
        # Create table for search queries
        await db.execute('''
            CREATE TABLE IF NOT EXISTS search_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_type TEXT,
                case_number TEXT,
                year TEXT,
                search_timestamp DATETIME,
                success BOOLEAN
            )
        ''')
        
        # Create table for raw responses
        await db.execute('''
            CREATE TABLE IF NOT EXISTS raw_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER,
                html_content TEXT,
                parsed_data TEXT,
                response_timestamp DATETIME,
                FOREIGN KEY (query_id) REFERENCES search_queries (id)
            )
        ''')
        await db.commit()

async def log_search_query(case_type: str, case_number: str, year: str, success: bool):
    async with aiosqlite.connect('court_cases.db') as db:
        cursor = await db.execute(
            '''INSERT INTO search_queries 
               (case_type, case_number, year, search_timestamp, success)
               VALUES (?, ?, ?, ?, ?)''',
            (case_type, case_number, year, datetime.now(), success)
        )
        await db.commit()
        return cursor.lastrowid

async def log_raw_response(query_id: int, html_content: str, parsed_data: dict):
    async with aiosqlite.connect('court_cases.db') as db:
        await db.execute(
            '''INSERT INTO raw_responses 
               (query_id, html_content, parsed_data, response_timestamp)
               VALUES (?, ?, ?, ?)''',
            (query_id, html_content, json.dumps(parsed_data), datetime.now())
        )
        await db.commit()