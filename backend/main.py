# incl_path
from . import crud
from . import models
from . import schemas
from . import database
from . import routers
from . import deps

from fastapi import Depends, FastAPI

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# include all routes
app.include_router(
    routers.router,
    dependencies=[Depends(deps.get_db)],
    responses={404: {"description": "Not found"}},
)

# streamlit run backend/frontend/test.py
# uvicorn backend.main:app --reload