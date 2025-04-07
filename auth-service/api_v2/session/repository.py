from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import Session
from .schema import (
    SessionResponse,
    SessionUpdate,
    SessionCreate,
)


@dataclass
class SessionRepository:
    db_session: AsyncSession

    async def get_session_by_id(self, session_id: int) -> Optional[SessionResponse]:
        query = select(Session).where(Session.id == session_id)

        session = await self.db_session.execute(query)
        return session.scalar()

    async def get_session_by_access_token(
        self, access_token: str
    ) -> Optional[SessionResponse]:
        query = select(Session).where(Session.access_token == access_token)

        session = await self.db_session.execute(query)
        return session.scalar()

    async def get_session_by_refresh_token(
        self, refresh_token: str
    ) -> Optional[SessionResponse]:
        query = select(Session).where(Session.refresh_token == refresh_token)

        session = await self.db_session.execute(query)
        return session.scalar()

    async def create_session(self, session: SessionCreate) -> int:
        session = Session(**session.model_dump())
        self.db_session.add(session)
        await self.db_session.commit()
        return session.id

    async def update_session(self, session: SessionUpdate):
        current_session = await self.get_session_by_id(session.session_id)
        update_session = session.model_dump(exclude_unset=True).items()

        for name, value in update_session:
            setattr(current_session, name, value)

        await self.db_session.commit()

    async def delete_session(self, session: SessionResponse):
        await self.db_session.delete(session)
        await self.db_session.commit()
