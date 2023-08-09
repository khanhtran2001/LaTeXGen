from pathlib import Path
from PIL import Image

import sys
sys.path.append("deployment")

from deployment.libs.models.model import get_model
from deployment.libs.utils.config import Config
from deployment.libs.utils.transforms import DeployTransform

TEST_DIR = Path(__file__).resolve().parents[1]
TEST_IMAGES_DIR = TEST_DIR / "test_images"
TEST_IMAGE = TEST_IMAGES_DIR / "0000000.png"

def test_onnx_model():
    config = Config()
    model = get_model(config)
    img =  Image.open("C:/Users/PC/Downloads/latex100k/test/0035207.png")
    result = model(img)
    for r in result[0]:
        print(r)
    return result[0][2][0]

print(test_onnx_model())