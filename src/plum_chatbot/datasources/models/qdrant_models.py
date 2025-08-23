from re import sub
from pydantic import BaseModel, Field


class QdrantDocumentMetadata(BaseModel):
    source: str = Field(..., description="Source file path of the document")
    title: str = Field(..., description="Title of the document")
    images: dict[int, str] = Field(
        ..., description="Mapping of image indices to their file paths"
    )


class QdrantDocument(BaseModel):
    id: str = Field(
        ...,
        description="Unique identifier for the document",
    )
    content: str = Field(..., description="The main content of the document")
    metadata: QdrantDocumentMetadata = Field(
        ...,
        description="Metadata associated with the document, including source and images",
    )

    def substitute_images(self) -> str:
        """
        Reconstruct the content by replacing image references with actual image paths.
        """

        def replace_with_image(match):
            idx = int(match.group(1))
            return f"![Image]({self.metadata.images[idx]})"

        return sub(r"!\[Image\]\((\d+)\)", replace_with_image, self.content)
