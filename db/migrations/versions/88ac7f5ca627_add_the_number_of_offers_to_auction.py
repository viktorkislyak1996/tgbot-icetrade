"""add the number of offers to auction

Revision ID: 88ac7f5ca627
Revises: baf15a1d38f5
Create Date: 2023-10-03 12:27:26.936045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88ac7f5ca627'
down_revision: Union[str, None] = 'baf15a1d38f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auction', sa.Column('offers_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auction', 'offers_number')
    # ### end Alembic commands ###