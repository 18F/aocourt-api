from fastapi import APIRouter, Depends
from starlette.requests import Request
from sqlalchemy.orm import Session
from ariadne.asgi import GraphQL
from app.data.database import get_db
from app.entities import User
from app.api.dependency import get_current_user
from . import schema

graphql_app = GraphQL(schema, debug=False)
graphQL_router = APIRouter()


@graphQL_router.get("/")
async def graphiql(request: Request):
    return await graphql_app.render_playground(request=request)


@graphQL_router.post("/")
async def graphql_post(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    request.state.db = db
    request.state.user = user
    return await graphql_app.graphql_http_server(request=request)
