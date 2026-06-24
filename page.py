from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal
from enum import Enum

from pydantic import BaseModel, EmailStr, HttpUrl, Field, field_validator


# ── Auth ───────────────────────────────────────────────────────────────────────


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    display_name: str | None
    avatar_url: str | None
    role: str
    created_at: datetime
    github_id: str | None

    model_config = {"from_attributes": True}


# ── Repository ─────────────────────────────────────────────────────────────────


class RepoIngestRequest(BaseModel):
    github_url: HttpUrl
    branch: str = "main"
    github_access_token: str | None = None


class RepoOut(BaseModel):
    id: uuid.UUID
    github_url: str
    full_name: str
    branch: str
    description: str | None
    status: str
    total_files: int
    total_functions: int
    total_classes: int
    indexed_chunks: int
    created_at: datetime
    updated_at: datetime
    progress: int

    model_config = {"from_attributes": True}


class RepoStatusOut(BaseModel):
    id: uuid.UUID
    status: str
    celery_task_id: str | None
    error_message: str | None
    total_files: int
    indexed_chunks: int
    progress: int
    model_config = {"from_attributes": True}


class FileTreeNode(BaseModel):
    name: str
    path: str
    type: Literal["file", "dir"]
    size: int | None = None
    children: list[FileTreeNode] | None = None

    model_config = {"from_attributes": True}


class RepoIngestResponse(BaseModel):
    repo: RepoOut
    tree: list[FileTreeNode]


class FileOut(BaseModel):
    id: uuid.UUID
    path: str
    language: str | None
    file_size: int

    model_config = {"from_attributes": True}


class FileContentOut(BaseModel):
    path: str
    content: str
    language: str | None


class RepoMetricsOut(BaseModel):
    total_files: int
    total_functions: int
    total_classes: int
    total_chunks: int
    languages: dict[str, int]


# ── Chat ───────────────────────────────────────────────────────────────────────


# ── Chat — request bodies ──────────────────────────────────────────────────────

class ChatSessionCreate(BaseModel):
    repository_id: uuid.UUID
    title: str | None = None

class ChatRequest(BaseModel):
    """Body for POST .../messages  (sync) and POST .../stream (SSE)."""
    question: str = Field(..., min_length=1, max_length=4000)
    # Optional overrides — frontend can leave these unset
    top_k: int = Field(default=8, ge=1, le=20,
                       description="Number of code chunks to retrieve from Qdrant")
    language_filter: str | None = Field(
        default=None,
        description="Only search chunks of this language, e.g. 'python'")
    include_graph: bool = Field(
        default=True,
        description="Whether to enrich context with Neo4j relationships")
    

class ChatHistory(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class RepoChatBootstrap(BaseModel):
    session_id: uuid.UUID
    messages: list[ChatHistory]

class 
