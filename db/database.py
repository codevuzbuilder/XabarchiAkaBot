import aiosqlite
from datetime import datetime

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
  user_id INTEGER PRIMARY KEY,
  button_color INTEGER DEFAULT 0,
  account_api TEXT,
  kassa_api TEXT,
  autopay INTEGER DEFAULT 0,
  is_partner INTEGER DEFAULT 0,
  created_at TEXT
);
CREATE TABLE IF NOT EXISTS archives(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER, chat_id INTEGER, chat_title TEXT,
  kind TEXT, file_id TEXT, keyword TEXT, created_at TEXT
);
CREATE TABLE IF NOT EXISTS labels(
  user_id INTEGER, key TEXT, label TEXT, PRIMARY KEY(user_id,key)
);
CREATE TABLE IF NOT EXISTS channels(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  chat_id TEXT, title TEXT, link TEXT
);
CREATE TABLE IF NOT EXISTS partner_bots(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  owner_id INTEGER, token TEXT, username TEXT, created_at TEXT
);
"""

def now():
    return datetime.utcnow().isoformat(timespec="seconds")

class DB:
    def __init__(self, path):
        self.path = path
        self.c: aiosqlite.Connection | None = None

    async def connect(self):
        self.c = await aiosqlite.connect(self.path)
        self.c.row_factory = aiosqlite.Row
        await self.c.executescript(SCHEMA)
        await self.c.commit()

    async def _exec(self, sql, params=()):
        await self.c.execute(sql, params)
        await self.c.commit()

    async def ensure_user(self, uid):
        await self._exec(
            "INSERT OR IGNORE INTO users(user_id, created_at) VALUES(?,?)",
            (uid, now()),
        )

    async def get_user(self, uid):
        cur = await self.c.execute("SELECT * FROM users WHERE user_id=?", (uid,))
        return await cur.fetchone()

    async def set_user(self, uid, **fields):
        keys = ", ".join(f"{k}=?" for k in fields)
        vals = list(fields.values()) + [uid]
        await self._exec(f"UPDATE users SET {keys} WHERE user_id=?", vals)

    async def get_label(self, uid, key, default):
        cur = await self.c.execute(
            "SELECT label FROM labels WHERE user_id=? AND key=?", (uid, key)
        )
        row = await cur.fetchone()
        return row["label"] if row else default

    async def set_label(self, uid, key, label):
        await self._exec(
            "INSERT INTO labels(user_id,key,label) VALUES(?,?,?) "
            "ON CONFLICT(user_id,key) DO UPDATE SET label=excluded.label",
            (uid, key, label),
        )

    async def add_archive(self, uid, chat_id, chat_title, kind, file_id, keyword):
        await self._exec(
            "INSERT INTO archives(user_id,chat_id,chat_title,kind,file_id,keyword,created_at)"
            " VALUES(?,?,?,?,?,?,?)",
            (uid, chat_id, chat_title, kind, file_id, keyword, now()),
        )

    async def list_archives(self, uid, chat_id=None):
        if chat_id is None:
            cur = await self.c.execute(
                "SELECT * FROM archives WHERE user_id=? ORDER BY id DESC", (uid,)
            )
        else:
            cur = await self.c.execute(
                "SELECT * FROM archives WHERE user_id=? AND chat_id=? ORDER BY id DESC",
                (uid, chat_id),
            )
        return await cur.fetchall()

    async def chats_of(self, uid):
        cur = await self.c.execute(
            "SELECT chat_id, chat_title, COUNT(*) n FROM archives "
            "WHERE user_id=? GROUP BY chat_id", (uid,)
        )
        return await cur.fetchall()

    async def search(self, uid, keyword):
        cur = await self.c.execute(
            "SELECT * FROM archives WHERE user_id=? AND keyword LIKE ?",
            (uid, f"%{keyword}%"),
        )
        return await cur.fetchall()

    async def add_channel(self, chat_id, title, link):
        await self._exec(
            "INSERT INTO channels(chat_id,title,link) VALUES(?,?,?)",
            (chat_id, title, link),
        )

    async def list_channels(self):
        cur = await self.c.execute("SELECT * FROM channels")
        return await cur.fetchall()

    async def add_partner_bot(self, owner_id, token, username):
        await self._exec(
            "INSERT INTO partner_bots(owner_id,token,username,created_at) VALUES(?,?,?,?)",
            (owner_id, token, username, now()),
        )

    async def list_partner_bots(self, owner_id):
        cur = await self.c.execute(
            "SELECT * FROM partner_bots WHERE owner_id=?", (owner_id,)
        )
        return await cur.fetchall()