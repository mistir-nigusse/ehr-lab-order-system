from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'results',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('orders.orders.id', ondelete='CASCADE'), nullable=False),
        sa.Column('test_code', sa.String(length=64), nullable=False),
        sa.Column('value', sa.String(length=255), nullable=True),
        sa.Column('units', sa.String(length=64), nullable=True),
        sa.Column('ref_range', sa.String(length=128), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('resulted_at', sa.DateTime(), nullable=True),
        sa.Column('received_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('digest', sa.String(length=64), nullable=False),
        sa.UniqueConstraint('order_id', 'digest', name='uq_results_order_digest'),
        schema='labs',
    )
    op.create_index('ix_labs_results_order', 'results', ['order_id'], unique=False, schema='labs')


def downgrade() -> None:
    op.drop_index('ix_labs_results_order', table_name='results', schema='labs')
    op.drop_table('results', schema='labs')

