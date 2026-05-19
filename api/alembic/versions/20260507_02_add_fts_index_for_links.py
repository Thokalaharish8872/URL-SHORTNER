"""add fts index for links search

Revision ID: 20260507_02
Revises: 20260429_01
Create Date: 2026-05-07 18:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260507_02"
down_revision = "20260429_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add tsvector column for full-text search
    op.add_column(
        "links",
        sa.Column("search_vector", postgresql.TSVECTOR(), nullable=True)
    )
    
    # Create GIN index for fast full-text search
    op.create_index(
        "ix_links_search_vector",
        "links",
        ["search_vector"],
        unique=False,
        postgresql_using="gin"
    )
    
    # Populate the search_vector column
    op.execute("""
        UPDATE links 
        SET search_vector = to_tsvector('english', 
            coalesce(code, '') || ' ' || 
            coalesce(long_url, '') || ' ' || 
            coalesce(array_to_string(tags, ' '), '')
        )
    """)
    
    # Create trigger to keep search_vector updated
    op.execute("""
        CREATE OR REPLACE FUNCTION links_search_vector_update() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := to_tsvector('english',
                coalesce(NEW.code, '') || ' ' ||
                coalesce(NEW.long_url, '') || ' ' ||
                coalesce(array_to_string(NEW.tags, ' '), '')
            );
            RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
    """)
    
    op.execute("""
        CREATE TRIGGER links_search_vector_trigger
        BEFORE INSERT OR UPDATE ON links
        FOR EACH ROW
        EXECUTE FUNCTION links_search_vector_update();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS links_search_vector_trigger ON links")
    op.execute("DROP FUNCTION IF EXISTS links_search_vector_update()")
    op.drop_index("ix_links_search_vector", table_name="links")
    op.drop_column("links", "search_vector")
