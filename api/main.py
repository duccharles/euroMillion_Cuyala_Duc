from fastapi import FastAPI
from api.predict import predict
from api.model import model
from api.model.retrain import retrain

app = FastAPI()
app.include_router(
    predict.router,
    tags=["predict"]
)
app.include_router(
    model.router,
    tags=["model"]
)
app.include_router(
    retrain.router,
    tags=["retrain"]
)