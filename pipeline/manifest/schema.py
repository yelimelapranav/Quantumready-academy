"""Pydantic models mirroring docs/manifest-schema.md. Every pipeline stage that
touches a lesson record should import LessonManifestEntry from here rather than
passing raw dicts around, so a schema change is a one-file edit.
"""
from pydantic import BaseModel, Field


class QuizQuestion(BaseModel):
    question: str
    choices: list[str]
    answer_index: int


class LessonManifestEntry(BaseModel):
    slug: str
    order_index: int
    title: str
    transcript: str
    cloudflare_video_id: str | None = None
    duration_seconds: int | None = None
    quiz: list[QuizQuestion] = Field(default_factory=list)


class Manifest(BaseModel):
    lessons: list[LessonManifestEntry]
