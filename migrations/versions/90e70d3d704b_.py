"""empty message

Revision ID: 90e70d3d704b
Revises: 
Create Date: 2019-12-07 17:50:10.425563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90e70d3d704b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_brand_name'), 'brand', ['name'], unique=True)
    op.create_table('motorcycleimage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('cpf', sa.String(length=11), nullable=True),
    sa.Column('rg', sa.String(length=9), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('brandimage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('motorcycle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=255), nullable=False),
    sa.Column('manufactore_year', sa.Integer(), nullable=False),
    sa.Column('model_year', sa.Integer(), nullable=False),
    sa.Column('color', sa.String(length=15), nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_motorcycle_manufactore_year'), 'motorcycle', ['manufactore_year'], unique=False)
    op.create_index(op.f('ix_motorcycle_model_year'), 'motorcycle', ['model_year'], unique=False)
    op.create_table('motorcycle_img_association',
    sa.Column('motorcycle_id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['motorcycleimage.id'], ),
    sa.ForeignKeyConstraint(['motorcycle_id'], ['motorcycle.id'], ),
    sa.PrimaryKeyConstraint('motorcycle_id', 'image_id')
    )
    op.create_table('sale',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('salesperson_id', sa.Integer(), nullable=False),
    sa.Column('motorcycle_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['motorcycle_id'], ['motorcycle.id'], ),
    sa.ForeignKeyConstraint(['salesperson_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sale')
    op.drop_table('motorcycle_img_association')
    op.drop_index(op.f('ix_motorcycle_model_year'), table_name='motorcycle')
    op.drop_index(op.f('ix_motorcycle_manufactore_year'), table_name='motorcycle')
    op.drop_table('motorcycle')
    op.drop_table('brandimage')
    op.drop_table('user')
    op.drop_table('motorcycleimage')
    op.drop_index(op.f('ix_brand_name'), table_name='brand')
    op.drop_table('brand')
    # ### end Alembic commands ###
