from fastapi import FastAPI, HTTPException
from typing import List
from database import database
from schemas import PostResponse, CommentResponse

tags_metadata = [
    { "name": "post", },
    { "name": "comment", },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/post", tags=["post"], response_model=List[PostResponse])
async def browse_post():
    database.cur.execute(f"SELECT id, title, content FROM post")
    rows = database.cur.fetchall()

    return [PostResponse(id=rows[i][0], title=rows[i][1], content=rows[i][2])
            for i in range(len(rows))]

@app.get("/post/{post_id}", tags=["post"], response_model=PostResponse)
async def read_post(post_id: int):
    database.cur.execute(f"SELECT id, title, content FROM post WHERE id= {post_id}")
    row = database.cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="post not found")
    return PostResponse(id=row[0], title=row[1], content=row[2])

@app.patch("/post/{post_id}", tags=["post"])
async def edit_post(post_id: int, title: str, content: str):
    database.cur.execute(f"SELECT id, title, content FROM post WHERE id= {post_id}")
    row = database.cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="post not found")

    database.cur.execute(f"UPDATE post SET title = '{title}', content = '{content}' WHERE id={post_id}")
    database.conn.commit()
    return f"post {post_id} is updated"

@app.post("/post", tags=["post"])
async def add_post():
    database.cur.execute(f"INSERT INTO post (title, content) VALUES ('', '') RETURNING id")
    id, = database.cur.fetchone()
    database.conn.commit()
    return f"post {id} is added"

@app.delete("/post/{post_id}", tags=["post"])
async def delete_post(post_id: int):
    database.cur.execute(f"SELECT id, title, content FROM post WHERE id= {post_id}")
    row = database.cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="post not found")

    database.cur.execute(f"DELETE FROM post WHERE id = {post_id}")
    database.conn.commit()
    return f"post {post_id} is deleted"

@app.get("/post/{post_id}/comment", tags=["comment"], response_model=List[CommentResponse], summary="Browse Comments Under Post")
async def browse_comment(post_id: int):
    database.cur.execute(f"SELECT id, post_id, content FROM comment WHERE post_id = {post_id}")
    rows = database.cur.fetchall()

    return [CommentResponse(id=rows[i][0], post_id=rows[i][1], content=rows[i][2])
            for i in range(len(rows))]

@app.get("/comment/{comment_id}", tags=["comment"], response_model=CommentResponse)
async def read_comment(comment_id: int):
    database.cur.execute(f"SELECT id, post_id, content FROM comment WHERE id= {comment_id}")
    row = database.cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="comment not found")
    return CommentResponse(id=row[0], post_id=row[1], content=row[2])

@app.patch("/comment/{comment_id}", tags=["comment"])
async def edit_comment(comment_id: int, content: str):
    database.cur.execute(f"SELECT id, post_id, content FROM comment WHERE id= {comment_id}")
    row = database.cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="comment not found")

    database.cur.execute(f"UPDATE comment SET content = '{content}' WHERE id={comment_id}")
    database.conn.commit()
    return f"comment {comment_id} is updated"

@app.post("/post/{post_id}/comment", tags=["comment"], summary="Add Comment Under Post")
async def add_comment(post_id: int):
    database.cur.execute(f"SELECT id, title, content FROM post WHERE id= {post_id}")
    row = database.cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="post not found")

    database.cur.execute(f"INSERT INTO comment (post_id ,content) VALUES ({post_id}, '') RETURNING id")
    id, = database.cur.fetchone()
    database.conn.commit()
    return f"comment {id} is added"

@app.delete("/comment/{comment_id}", tags=["comment"])
async def delete_comment(comment_id: int):
    database.cur.execute(f"SELECT id, post_id, content FROM comment WHERE id= {comment_id}")
    row = database.cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="comment not found")

    database.cur.execute(f"DELETE FROM comment WHERE id = {comment_id}")
    database.conn.commit()
    return f"comment {comment_id} is deleted"