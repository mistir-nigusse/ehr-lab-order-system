from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('encounter_id', sa.Integer(), sa.ForeignKey('ehr.encounters.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tests', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(length=16), nullable=False, server_default='ordered'),
        sa.Column('ordered_by', sa.String(length=128), nullable=True),
        sa.Column('placed_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        schema='orders',
    )
    op.create_index('ix_orders_encounter', 'orders', ['encounter_id'], unique=False, schema='orders')


def downgrade() -> None:
    op.drop_index('ix_orders_encounter', table_name='orders', schema='orders')
    op.drop_table('orders', schema='orders')

