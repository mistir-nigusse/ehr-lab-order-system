from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Encounters
    op.create_table(
        'encounters',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patient.patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.String(length=8), nullable=False),  # OUT | ER | IN
        sa.Column('started_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('status', sa.String(length=16), nullable=True),
        schema='ehr',
    )
    op.create_index('ix_ehr_encounters_patient', 'encounters', ['patient_id'], unique=False, schema='ehr')

    # Notes (append-only)
    op.create_table(
        'notes',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patient.patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('encounter_id', sa.Integer(), sa.ForeignKey('ehr.encounters.id', ondelete='CASCADE'), nullable=False),
        sa.Column('author', sa.String(length=128), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        schema='ehr',
    )
    op.create_index('ix_ehr_notes_patient', 'notes', ['patient_id'], unique=False, schema='ehr')
    op.create_index('ix_ehr_notes_encounter', 'notes', ['encounter_id'], unique=False, schema='ehr')


def downgrade() -> None:
    op.drop_index('ix_ehr_notes_encounter', table_name='notes', schema='ehr')
    op.drop_index('ix_ehr_notes_patient', table_name='notes', schema='ehr')
    op.drop_table('notes', schema='ehr')
    op.drop_index('ix_ehr_encounters_patient', table_name='encounters', schema='ehr')
    op.drop_table('encounters', schema='ehr')

