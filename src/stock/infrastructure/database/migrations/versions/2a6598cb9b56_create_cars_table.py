"""create_cars_table
Revision ID: 2a6598cb9b56
Revises:
Create Date: 2021-12-02 18:22:50.325449
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "2a6598cb9b56"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    schema = op.get_context().version_table_schema
    op.create_table(
        "cars",
        sa.Column("identifier", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("brand", sa.String(), nullable=False),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("registration_number", sa.String(), nullable=False),
        sa.Column("power", sa.Integer(), nullable=True),
        sa.Column("type", sa.Enum("SEDAN", "SUV", "MINIVAN", "ROADSTER", name="cartype"), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("available", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("identifier"),
        schema=schema,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    schema = op.get_context().version_table_schema
    op.drop_table("cars", schema=schema)
    # ### end Alembic commands ###