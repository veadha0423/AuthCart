from fastapi import FastAPI

import database
import models
from routes import router

app = FastAPI(title="AuthCart API")

models.Base.metadata.create_all(bind=database.engine)

app.include_router(router)