from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId

origins = ["*"]

class Blog(BaseModel):
    title:str
    author:str
    content:str
    upvotes:int
    downvotes:int

def blog_helper(blog) -> dict : 
    return {
        "id": str(blog["_id"]),
        "title": blog["title"],
        "author": blog["author"],
        "content": blog["content"],
        "upvotes": blog["upvotes"],
        "downvotes": blog["downvotes"]
    }

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# client = MongoClient("localhost", 27017)
client = MongoClient("mongodb+srv://khalilzemni:f1FTZxKPBi6JJJq7@blog-app.ss8fj.mongodb.net/?retryWrites=true&w=majority")
blogapp_db = client["blogapp"]
blogs_collection = blogapp_db.get_collection("blogs")


@app.get("/")
async def hello():
    return "deployed to horuku :D"

@app.get("/blogs")
async def getAllBlogs() -> dict:
    blogs = []
    for blog in blogs_collection.find():
        blogs.append(blog_helper(blog));
    return blogs;

@app.get("/blogs/{blogId}")
async def getBlogById(blogId: str):
    blog = blogs_collection.find_one({"_id": ObjectId(blogId)})
    return blog_helper(blog)


@app.post("/blogs")
async def postBlog(blog: dict) -> dict:
    to_add = blogs_collection.insert_one(blog);
    print(to_add.inserted_id)
    added_blog = blogs_collection.find_one({"_id":to_add.inserted_id})
    return blog_helper(added_blog)
