"""manual patient_user table

Revision ID: ca167bcce4c8
Revises: 
Create Date: 2025-06-03 05:45:29.085409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca167bcce4c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'patient_user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=120), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patient.id'), nullable=False, unique=True),
        sa.Column('is_verified', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_table('patient_user')
