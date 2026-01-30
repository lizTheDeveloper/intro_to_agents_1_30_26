# Course Design for Agent Memory (Unit4)

**Unit4 Objectives:**
1. Implement persistent memory using SQLite
2. Store/retrieve agent state across sessions
3. Build memory indexing and querying
4. Create recursive memory patterns
5. Handle database connection management

## Code Architecture

1. **Database Setup**:
```sql
CREATE TABLE memory (
  id INTEGER PRIMARY KEY,
  session_id TEXT,
  key TEXT,
  value TEXT,
  created_at TIMESTAMP
)
```

2. **Memory Manager**:
```python
import sqlite3
from datetime import datetime


class MemoryAgent:
    """Manages persistent memory through SQLite"""

    def __init__(self):
        self.conn = sqlite3.connect('agent_memory.db')

    def connect(self):
        return self.conn.cursor()

    def save_state(self, session_id, key, value):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO memory (session_id, key, value, created_at)"
            "VALUES (?, ?, ?, ?)",
            (session_id, key, value, datetime.now())
        )
        self.conn.commit()

    def get_last_state(self, session_id, key):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT value FROM memory"
            "WHERE session_id = ? AND key = ?"
            "ORDER BY created_at DESC LIMIT 1",
            (session_id, key)
        )
        result = cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()