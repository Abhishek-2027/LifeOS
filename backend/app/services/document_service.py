# backend/app/services/document_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document
from app.schemas.document_schema import DocumentCreate


class DocumentService:

    @staticmethod
    async def add_document(db: AsyncSession, user_id: int, data: DocumentCreate):

        document = Document(
            user_id=user_id,
            filename=data.filename,
            content_summary=data.content_summary
        )

        db.add(document)
        await db.commit()
        await db.refresh(document)

        return document