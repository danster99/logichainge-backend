"""adding attchement object and relationships

Revision ID: 0734f65d6637
Revises: 0bdb913aa547
Create Date: 2022-12-06 15:38:56.499796

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '0734f65d6637'
down_revision = '0bdb913aa547'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'attachment',
		sa.Column(
			'id',
			postgresql.UUID,
			default=uuid.uuid4,
			primary_key=True,
			unique=True
		),
		sa.Column('base_url', sa.String(), nullable=True),
		sa.Column('tr_file_id', sa.Integer(), nullable=False),
		sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
		sa.ForeignKeyConstraint(['tr_file_id'], ['transport_file.id'])
	)
	
	op.create_table(
		'image',
		sa.Column(
			'id',
			postgresql.UUID,
			default=uuid.uuid4,
			primary_key=True,
			unique=True
		),
		sa.Column('path', sa.String(), nullable=True),
		sa.Column('attachment_id', postgresql.UUID, nullable=False),
		sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
		sa.ForeignKeyConstraint(['attachment_id'], ['attachment.id'])
	)


def downgrade():
	op.drop_table('image')
	op.drop_table('attachment')
