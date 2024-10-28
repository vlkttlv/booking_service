"""create tables

Revision ID: d552054c0e92
Revises:
Create Date: 2024-10-26 14:07:38.424461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd552054c0e92'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String()),
        sa.Column('hashed_password', sa.String()),
        sa.Column('role', sa.String(), nullable=True, default='user'),
    )

    # Создаем таблицу hotels
    op.create_table(
        'hotels',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('services', sa.ARRAY(sa.String())),
        sa.Column('rooms_quantity', sa.Integer(), nullable=False),
    )

    # Создаем таблицу hotels_images
    op.create_table(
        'hotels_images',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('hotel_id', sa.Integer(), sa.ForeignKey(
            'hotels.id'), nullable=False),
        sa.Column('image_id', sa.Integer()),
    )

    # Создаем таблицу rooms
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('hotel_id', sa.Integer(), sa.ForeignKey(
            'hotels.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('services', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False),
    )

    # Создаем таблицу rooms_images
    op.create_table(
        'rooms_images',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('room_id', sa.Integer(), sa.ForeignKey(
            'rooms.id'), nullable=False),
        sa.Column('image_id', sa.Integer(), nullable=False),
    )

    # Создаем таблицу bookings
    op.create_table(
        'bookings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('room_id', sa.Integer(), sa.ForeignKey('rooms.id')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('date_from', sa.Date(), nullable=False),
        sa.Column('date_to', sa.Date(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('total_cost', sa.Integer(), sa.Computed(
            '(date_to - date_from) * price', )),
        sa.Column('total_days', sa.Integer(),
                  sa.Computed('date_to - date_from', )),
        sa.Column('payment_status', sa.String(), default="not paid"),
    )
    # Создаем таблицу payments
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('booking_id', sa.Integer(), sa.ForeignKey('bookings.id')),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('date_to', sa.Date(), nullable=False),
        sa.Column('status', sa.String()),
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###