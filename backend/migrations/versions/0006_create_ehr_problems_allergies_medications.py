from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Problems
    op.create_table(
        'problems',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patient.patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('code', sa.String(length=64), nullable=True),
        sa.Column('text', sa.String(length=255), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('onset_date', sa.Date(), nullable=True),
        sa.Column('author', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        schema='ehr',
    )
    op.create_index('ix_ehr_problems_patient', 'problems', ['patient_id'], unique=False, schema='ehr')

    # Allergies
    op.create_table(
        'allergies',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patient.patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('substance_code', sa.String(length=64), nullable=True),
        sa.Column('severity', sa.String(length=32), nullable=True),
        sa.Column('reaction', sa.String(length=128), nullable=True),
        sa.Column('recorded_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('author', sa.String(length=128), nullable=True),
        schema='ehr',
    )
    op.create_index('ix_ehr_allergies_patient', 'allergies', ['patient_id'], unique=False, schema='ehr')

    # Medications
    op.create_table(
        'medications',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patient.patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('rx_code', sa.String(length=64), nullable=True),
        sa.Column('dose', sa.String(length=64), nullable=True),
        sa.Column('route', sa.String(length=64), nullable=True),
        sa.Column('start', sa.Date(), nullable=True),
        sa.Column('end', sa.Date(), nullable=True),
        sa.Column('author', sa.String(length=128), nullable=True),
        schema='ehr',
    )
    op.create_index('ix_ehr_medications_patient', 'medications', ['patient_id'], unique=False, schema='ehr')


def downgrade() -> None:
    op.drop_index('ix_ehr_medications_patient', table_name='medications', schema='ehr')
    op.drop_table('medications', schema='ehr')
    op.drop_index('ix_ehr_allergies_patient', table_name='allergies', schema='ehr')
    op.drop_table('allergies', schema='ehr')
    op.drop_index('ix_ehr_problems_patient', table_name='problems', schema='ehr')
    op.drop_table('problems', schema='ehr')

