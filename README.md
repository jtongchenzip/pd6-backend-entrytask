# Entry Task - My Blog
## How to Start Service

### Set up
1. git clone project
    ```
    git clone https://github.com/jtongchenzip/pd6-backend-entrytask.git
    ```
2. change directory to `pd6-backend-entrytask`
    ```
    cd pd6-backend-entrytask
    ```

3. create conda environment  
    ```
    conda create --name my-blog python=3.8
    ```
    ```
    conda activate my-blog
    ```
    ```
    pip install -r requirements.txt
    ```

### Edit necessary files
1. copy `.env.example` and rename the file name to `.env`
2. copy `docker-compose.yaml.example` and rename the file name to `docker-compose.yaml`
3. edit `.env` and `docker-compose.yaml` to fit your environment

### Create Database
1. In your directory, run `docker-compose up -d`
2. If the database doesn't create table automatically, run  
    ```
    docker exec -it test_postgres psql -u test_user -w test_db -f docker-entrypoint-initdb.d/schema.sql
    ```
   You could check the database through psql or dbeaver

### Start backend service
1. Run service  
    ```
    uvicorn main:app --reload
    ```
2. Go to `localhost:8000/docs` to find your APIs


## DB Schema and API Designs

### DB Schema
1. table: `post`

    | post          |                   |
    | ------------- | ----------------- |
    | id            | int (primary key) |
    | title         | varchar           |
    | content       | varchar           |

2. table: `comment`

    | comment  |                   |
    | -------- | ----------------- |
    | id       | int (primary key) |
    | post_id  | int               |
    | content  | varchar           |

### API
1. API for post

    |             | Method | EndPoint          | Error Response                               |
    | ----------- | ------ | ----------------- | -------------------------------------------- |
    | Browse post | GET    | `/post`           |                                              |
    | Read post   | GET    | `/post/{post_id}` | `HTTP_404_NOT_FOUND`                         |
    | Edit post   | PATCH  | `/post/{post_id}` | `HTTP_404_NOT_FOUND`                         |
    | Add post    | POST   | `/post`           |                                              | 
    | Delete post | DELETE | `/post/{post_id}` | `HTTP_404_NOT_FOUND`                         |

    |             | Input                                        | Output                      |
    | ----------- | -------------------------------------------- | --------------------------- |
    | Browse post |                                              | `List[PostResponse]`        |
    | Read post   | `post_id: int`                               | `PostResponse`              | 
    | Edit post   | `post_id: int`, `title: str`, `content: str` | `post {post_id} is updated` | 
    | Add post    |                                              | `post {post_id} is added`   |
    | Delete post | `post_id:int`                                | `post {post_id} is deleted` | 

2. API for comment

    |                | Method | EndPoint                  | Error Response                     |
    | -------------- | ------ | ------------------------- | ---------------------------------- |
    | Browse comment | GET    | `/post/{post_id}/comment` |                                    |
    | Read comment   | GET    | `/comment/{comment_id}`   | `HTTP_404_NOT_FOUND`               |
    | Edit comment   | PATCH  | `/comment/{comment_id}`   | `HTTP_404_NOT_FOUND`               |
    | Add comment    | POST   | `/post/{post_id}/comment` |                                    | 
    | Delete comment | DELETE | `/comment/{comment_id}`   | `HTTP_404_NOT_FOUND`               |

    |                | Input                             | Output                            |
    | -------------- | --------------------------------- | --------------------------------- |
    | Browse comment | `post_id: int`                    | `List[CommentResponse]`           |
    | Read comment   | `comment_id: int`                 | `CommentResponse`                 | 
    | Edit comment   | `comment_id: int`, `content: str` | `comment {comment_id} is updated` | 
    | Add comment    | `post_id:int`                     | `comment {comment_id} is added`   |
    | Delete comment | `comment_id:int`                  | `comment {comment_id} is deleted` | 

3. Response Model
- PostResponse
    ```
    class PostResponse(BaseModel):
        id: int
        title: str
        content: str
    ```
- CommentResponse
    ```
    class CommentResponse(BaseModel):
        id: int
        post_id: int
        content: str
    ```

