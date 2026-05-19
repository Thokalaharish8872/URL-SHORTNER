"""create links and click_events tables

Revision ID: 20260429_01
Revises:
Create Date: 2026-04-29 14:20:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260429_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("long_url", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.String(length=64)), nullable=True),
    )
    op.create_index("ix_links_code", "links", ["code"], unique=True)
    op.create_index("ix_links_created_by", "links", ["created_by"], unique=False)

    op.create_table(
        "click_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("link_id", sa.Integer(), nullable=False),
        sa.Column("clicked_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("referrer", sa.String(length=512), nullable=True),
        sa.Column("ip_hash", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["link_id"], ["links.id"], ondelete="CASCADE"),
    )
    op.create_index(
        "ix_click_events_link_id_clicked_at",
        "click_events",
        ["link_id", "clicked_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_click_events_link_id_clicked_at", table_name="click_events")
    op.drop_table("click_events")
    op.drop_index("ix_links_created_by", table_name="links")
    op.drop_index("ix_links_code", table_name="links")
    op.drop_table("links")
