import base64
from dataclasses import dataclass

from api_v1.face.schema import FaceForm
from config.broker import connection_broker


@dataclass
class FaceService:
    queue_name = "home_queue"
    queue_name_callback = "callback_home_queue"

    async def create_face(self, face_request: FaceForm):
        contents = await face_request.file.read()
        image_b64 = base64.b64encode(contents).decode("ascii")

        body = {
            "key": "face.create_face",
            "body": {
                "name": face_request.name,
                "file": image_b64,
                "home_id": face_request.home_id
            }
        }

        await connection_broker(queue_name=self.queue_name, queue_name_callback=self.queue_name_callback, body=body)
