from dataclasses import dataclass

@dataclass
class SessionService:

    async def get_session(self, session_id: int):
        pass