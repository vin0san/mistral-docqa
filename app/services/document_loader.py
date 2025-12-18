from fastapi import UploadFile, HTTPException


class DocumentLoader:
    @staticmethod
    async def load(file: UploadFile) -> str:
        if not file.filename.endswith((".txt", ".md")):
            raise HTTPException(400, "Only .txt or .md files supported")

        content = (await file.read()).decode("utf-8").strip()

        if not content:
            raise HTTPException(400, "Document is empty")

        return content
