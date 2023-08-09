from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form, Request
from starlette.datastructures import FormData
from typing import Annotated

from deployment.libs.models.model import get_model
from deployment.libs.utils.config import Config

app = FastAPI(title = "latexocr api")
config = Config()
model = None


@app.on_event("startup")
async def load_model():
    global model
    if model is None:
        model = get_model(config)


# Route 1: Test if things working
@app.get("/")
def root():
    return {
        "message": "Hello"
    }

# Route 2: Take the image from the user and load it to the model
@app.post('/predict/')
async def predict(#sampling_type: Annotated[str,Form()],
                temperature: Annotated[float, Form()],
                search_type: Annotated[str,Form()],
                beam_width: Annotated[int,Form()],
                file: UploadFile = File(...)) -> list :
    """
    Predict the latext code from an image file

    Args:
        img (UploadFile): Image to predict from. Default: File(...).
    
    Returns:
        result (str): Latex prediction of the input image.
    """
    global model
#    config.sampling = sampling_type
    config.search_method = search_type
    config.temperature = temperature
    config.beam_width = beam_width
    model = get_model(config)
    image = Image.open(file.file)
    result = model(image)
    return result



    





