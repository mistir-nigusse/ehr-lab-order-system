from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('orders', sa.Column('lab_code', sa.String(length=64), nullable=True), schema='orders')
    op.create_index('ix_orders_lab_code', 'orders', ['lab_code'], unique=False, schema='orders')


def downgrade() -> None:
    op.drop_index('ix_orders_lab_code', table_name='orders', schema='orders')
    op.drop_column('orders', 'lab_code', schema='orders')

