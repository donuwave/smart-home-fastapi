from api_v1.firebase.repository import FirebaseRepository


async def get_firebase_repository() -> FirebaseRepository:
    return FirebaseRepository()
