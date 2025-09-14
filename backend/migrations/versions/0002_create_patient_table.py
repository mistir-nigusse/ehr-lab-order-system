from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('mrn', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('dob', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('mrn', name='uq_patient_mrn'),
        schema='patient',
    )
    op.create_index('ix_patient_mrn', 'patients', ['mrn'], unique=False, schema='patient')
    op.create_index('ix_patient_name', 'patients', ['name'], unique=False, schema='patient')


def downgrade() -> None:
    op.drop_index('ix_patient_name', table_name='patients', schema='patient')
    op.drop_index('ix_patient_mrn', table_name='patients', schema='patient')
    op.drop_table('patients', schema='patient')

