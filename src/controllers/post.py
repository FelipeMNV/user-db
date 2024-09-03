from flask import Blueprint, request
from src.app import Post, db
from http import HTTPStatus
from sqlalchemy import inspect

bp = Blueprint("post", __name__, url_prefix="/posts")


def _create_post():
    data = request.json
    post = Post(
        title=data["Title"],
        body=data["Body"],
        user_id=data["user_id"],
    )
    db.session.add(post)
    db.session.commit()


@bp.route("/", methods=["GET"])
def _list_post():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()

    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id,
            "created": post.created,
        }
        for post in posts
    ]


@bp.route("/", methods=["POST"])
def list_or_create_post():
    if request.method == "POST":
        _create_post()
        return {"message": "Post created"}, HTTPStatus.CREATED
    else:
        return {"posts": _list_post()}


@bp.route("/<int:post_id>")
def get_post(post_id):
    post = db.get_or_404(Post, post_id)
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "user_id": post.user_id,
        "created": post.created,
    }


@bp.route("/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "user_id": post.user_id,
        "created": post.created,
    }


@bp.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return {
        "message": f"Post ID: {post.id} Title: {post.title} deleted!"
    }, HTTPStatus.OK
