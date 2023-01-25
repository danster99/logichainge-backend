"""Added new child object to transport_file

Revision ID: 67f97ac60733
Revises: fbcc97b975e1
Create Date: 2022-04-21 16:21:14.003613

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '67f97ac60733'
down_revision = 'fbcc97b975e1'
branch_labels = None
depends_on = None


def upgrade():
	op.drop_column(table_name='transport_file', column_name='client')
	op.drop_column(table_name='transport_file', column_name='contact')
	op.drop_column(table_name='transport_file', column_name='department')
	op.drop_column(table_name='transport_file', column_name='employee')
	op.add_column(
		"activity",
		sa.Column(
			'instructions',
			sa.String,
			nullable=True
		))
	
	op.create_table(
		'client',
		sa.Column('id', sa.Integer, nullable=False, autoincrement=True),
		sa.Column('client_identifier', sa.String, autoincrement=False, nullable=False),
		sa.Column('name', sa.String, autoincrement=False, nullable=False),
		sa.Column('transport_file_id', sa.Integer, autoincrement=False, nullable=False),
		sa.PrimaryKeyConstraint('id'),
		sa.ForeignKeyConstraint(
			['transport_file_id'],
			['transport_file.id'],
			ondelete="CASCADE"
		)
	)
	op.create_table(
		'contact',
		sa.Column('id', sa.Integer, nullable=False, autoincrement=True),
		sa.Column('initials', sa.String, autoincrement=False, nullable=True),
		sa.Column('name', sa.String, autoincrement=False, nullable=False),
		sa.Column('surname_prefix', sa.String, autoincrement=False, nullable=True),
		sa.Column('surname', sa.String, autoincrement=False, nullable=False),
		sa.Column('phone', sa.String, autoincrement=False, nullable=True),
		sa.Column('mobile', sa.String, autoincrement=False, nullable=True),
		sa.Column('email', sa.String, autoincrement=False, nullable=False),
		sa.Column('transport_file_id', sa.Integer, autoincrement=False, nullable=False),
		sa.PrimaryKeyConstraint('id'),
		sa.ForeignKeyConstraint(
			['transport_file_id'],
			['transport_file.id'],
			ondelete="CASCADE"
		)
	)
	op.create_table(
		'department',
		sa.Column('id', sa.Integer, nullable=False, autoincrement=True),
		sa.Column('name', sa.String, autoincrement=False, nullable=False),
		sa.Column('transport_file_id', sa.Integer, autoincrement=False, nullable=False),
		sa.PrimaryKeyConstraint('id'),
		sa.ForeignKeyConstraint(
			['transport_file_id'],
			['transport_file.id'],
			ondelete="CASCADE"
		)
	)
	op.create_table(
		'employee',
		sa.Column('id', sa.Integer, nullable=False, autoincrement=True),
		sa.Column('name', sa.String, autoincrement=False, nullable=False),
		sa.Column('transport_file_id', sa.Integer, autoincrement=False, nullable=False),
		sa.PrimaryKeyConstraint('id'),
		sa.ForeignKeyConstraint(
			['transport_file_id'],
			['transport_file.id'],
			ondelete="CASCADE"
		)
	)


def downgrade():
	op.add_column(table_name='transport_file', column=sa.Column('client', sa.String, nullable=False))
	op.add_column(table_name='transport_file', column=sa.Column('contact', sa.String, nullable=False))
	op.add_column(table_name='transport_file', column=sa.Column('department', sa.String, nullable=False))
	op.add_column(table_name='transport_file', column=sa.Column('employee', sa.String, nullable=False))
	op.drop_column(table_name="activity", column_name='instructions')
	
	op.drop_table('client')
	op.drop_table('contact')
	op.drop_table('department')
	op.drop_table('employee')
