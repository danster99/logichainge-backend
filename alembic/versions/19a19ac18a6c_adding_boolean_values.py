"""adding boolean values

Revision ID: 19a19ac18a6c
Revises: 9b28a1c8dc26
Create Date: 2022-07-04 09:54:18.181467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19a19ac18a6c'
down_revision = '9b28a1c8dc26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transport_file', sa.Column('multi_trip', sa.Boolean(), server_default='False', nullable=True))
    op.add_column('transport_file', sa.Column('multi_activity', sa.Boolean(), server_default='False', nullable=True))
    op.add_column('transport_file', sa.Column('date_deviation', sa.Boolean(), server_default='False', nullable=True))
    op.add_column('transport_file', sa.Column('urgency', sa.Boolean(), server_default='False', nullable=True))
    op.add_column('transport_file', sa.Column('late_booking', sa.Boolean(), server_default='False', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transport_file', 'late_booking')
    op.drop_column('transport_file', 'urgency')
    op.drop_column('transport_file', 'date_deviation')
    op.drop_column('transport_file', 'multi_activity')
    op.drop_column('transport_file', 'multi_trip')
    # ### end Alembic commands ###
