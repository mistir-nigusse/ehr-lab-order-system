from alembic import op
import sqlalchemy as sa

# revision identifiers used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create module schemas if not exist 
    for schema in ('patient', 'ehr', 'orders', 'labs'):
        op.execute(f'CREATE SCHEMA IF NOT EXISTS {schema}')


def downgrade() -> None:
    # Drop schemas
    for schema in ('labs', 'orders', 'ehr', 'patient'):
        op.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE')

