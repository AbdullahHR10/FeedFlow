"""Pagination for post-related views."""
from rest_framework.pagination import CursorPagination


class PostCursorPagination(CursorPagination):
    """Cursor-based pagination for posts."""
    page_size = 10
    ordering = "-created_at"
