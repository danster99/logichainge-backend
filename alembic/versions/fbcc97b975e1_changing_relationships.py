"""changing relationship

Revision ID: fbcc97b975e1
Revises: 27b92a99e3e5
Create Date: 2022-04-20 17:22:38.843901

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fbcc97b975e1'
down_revision = '27b92a99e3e5'
branch_labels = None
depends_on = None


def upgrade():
    print("Changing activity and goods relationship to be one to many")
    op.drop_column('transport_file', 'activity_reference')
    op.drop_column('activity', 'goods_id')
    op.add_column('activity', sa.Column('transport_file_id', sa.Integer, nullable=False))
    op.create_foreign_key(
        'fk_activity_transport_file',
        source_table='activity',
        referent_table='transport_file',
        local_cols=['transport_file_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    op.add_column('goods',  sa.Column('activity_id', sa.Integer, nullable=False))
    op.create_foreign_key(
        'fk_goods_activity',
        source_table='goods',
        referent_table='activity',
        local_cols=['activity_id'],
        remote_cols=['activity_reference'],
        ondelete='CASCADE'
    )
    
    
def downgrade():
    return 'Not implemented yet'
