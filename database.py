import sqlite3
from datetime import datetime

# 数据库文件名
DB_FILE = "hr_system.db"

# ==================== 初始化数据库 ====================
def init_database():
    """创建数据库表（如果不存在）"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 创建候选人表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            position TEXT,
            experience TEXT,
            education TEXT,
            status TEXT,
            tags TEXT,
            created_at TEXT
        )
    """)
    
    # 创建文件表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            file_name TEXT NOT NULL,
            file_data BLOB,
            upload_time TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id)
        )
    """)
    
    # 创建备注表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            comment_text TEXT NOT NULL,
            comment_time TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ 数据库初始化成功！")

# ==================== 候选人操作 ====================

def get_all_candidates():
    """获取所有候选人"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM candidates ORDER BY id DESC")
    rows = cursor.fetchall()
    
    candidates = []
    for row in rows:
        candidate = {
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "email": row[3],
            "position": row[4],
            "experience": row[5],
            "education": row[6],
            "status": row[7],
            "tags": row[8].split(",") if row[8] else [],
            "created_at": row[9]
        }
        candidates.append(candidate)
    
    conn.close()
    return candidates

def get_candidate_by_id(candidate_id):
    """根据ID获取候选人"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "email": row[3],
            "position": row[4],
            "experience": row[5],
            "education": row[6],
            "status": row[7],
            "tags": row[8].split(",") if row[8] else [],
            "created_at": row[9]
        }
    return None

def add_candidate(candidate):
    """添加新候选人"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    tags_str = ",".join(candidate["tags"]) if candidate["tags"] else ""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO candidates 
        (name, phone, email, position, experience, education, status, tags, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate["name"],
        candidate["phone"],
        candidate["email"],
        candidate["position"],
        candidate["experience"],
        candidate["education"],
        candidate["status"],
        tags_str,
        created_at
    ))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    candidate["id"] = new_id
    candidate["created_at"] = created_at
    return candidate

def search_candidates(keyword):
    """搜索候选人"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if not keyword:
        return get_all_candidates()
    
    cursor.execute("""
        SELECT * FROM candidates 
        WHERE name LIKE ? OR position LIKE ? OR tags LIKE ?
        ORDER BY id DESC
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    
    rows = cursor.fetchall()
    
    candidates = []
    for row in rows:
        candidate = {
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "email": row[3],
            "position": row[4],
            "experience": row[5],
            "education": row[6],
            "status": row[7],
            "tags": row[8].split(",") if row[8] else [],
            "created_at": row[9]
        }
        candidates.append(candidate)
    
    conn.close()
    return candidates

# ==================== 文件操作 ====================

def save_uploaded_file(candidate_id, file_name, file_data):
    """保存上传的文件"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO files (candidate_id, file_name, file_data, upload_time)
        VALUES (?, ?, ?, ?)
    """, (candidate_id, file_name, file_data, upload_time))
    
    conn.commit()
    conn.close()

def get_candidate_files(candidate_id):
    """获取候选人的所有文件"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, file_name, upload_time 
        FROM files 
        WHERE candidate_id = ?
        ORDER BY upload_time DESC
    """, (candidate_id,))
    
    rows = cursor.fetchall()
    
    files = []
    for row in rows:
        files.append({
            "id": row[0],
            "name": row[1],
            "upload_time": row[2]
        })
    
    conn.close()
    return files

# ==================== 备注操作 ====================

def add_comment(candidate_id, comment_text):
    """添加备注"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    comment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO comments (candidate_id, comment_text, comment_time)
        VALUES (?, ?, ?)
    """, (candidate_id, comment_text, comment_time))
    
    conn.commit()
    conn.close()

def get_comments(candidate_id):
    """获取候选人的所有备注"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT comment_text, comment_time 
        FROM comments 
        WHERE candidate_id = ?
        ORDER BY comment_time DESC
    """, (candidate_id,))
    
    rows = cursor.fetchall()
    
    comments = []
    for row in rows:
        comments.append({
            "text": row[0],
            "time": row[1]
        })
    
    conn.close()
    return comments

# ==================== 初始化示例数据 ====================

def insert_sample_data():
    """插入示例数据（仅在数据库为空时）"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM candidates")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # 插入示例数据
        sample_candidates = [
            ("张三", "13800138000", "zhangsan@example.com", "Java工程师", "5年", "本科", "待沟通", "Java,SpringBoot,MySQL"),
            ("李四", "13900139000", "lisi@example.com", "前端工程师", "3年", "本科", "面试中", "React,Vue,JavaScript"),
            ("王五", "13700137000", "wangwu@example.com", "产品经理", "4年", "硕士", "已入职", "产品设计,数据分析")
        ]
        
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for candidate in sample_candidates:
            cursor.execute("""
                INSERT INTO candidates 
                (name, phone, email, position, experience, education, status, tags, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (*candidate, created_at))
        
        conn.commit()
        print("✅ 示例数据已插入！")
    
    conn.close()
