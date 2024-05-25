from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'your_revision_id'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('debts', 'debt_id', existing_type=sa.String(), type_=sa.String(length=50))
    op.alter_column('debts', 'name', existing_type=sa.String(), type_=sa.String(length=100))
    op.alter_column('debts', 'government_id', existing_type=sa.String(), type_=sa.String(length=20))
    op.alter_column('debts', 'email', existing_type=sa.String(), type_=sa.String(length=100))

def downgrade():
    op.alter_column('debts', 'debt_id', existing_type=sa.String(length=50), type_=sa.String())
    op.alter_column('debts', 'name', existing_type=sa.String(length=100), type_=sa.String())
    op.alter_column('debts', 'government_id', existing_type=sa.String(length=20), type_=sa.String())
    op.alter_column('debts', 'email', existing_type=sa.String(length=100), type_=sa.String())