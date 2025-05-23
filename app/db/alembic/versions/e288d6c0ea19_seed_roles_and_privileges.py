"""Seed Roles and Privileges

Revision ID: e288d6c0ea19
Revises: 5199f5b5d2f6
Create Date: 2025-05-12 09:49:40.946030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e288d6c0ea19'
down_revision: Union[str, None] = '5199f5b5d2f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        INSERT INTO roles (key, name)
        VALUES
            ('admin', 'Administrator'),
            ('customer', 'Customer')
        """
    )
    op.execute(
        """
        INSERT INTO privileges (key, name)
        VALUES
            ('c_n_u', 'Create New User'),
            ('l_a_u', 'List all Users'),
            ('v_a_u', 'View a User'),
            ('v_o_d', 'View Own Details'),
            ('u_a_u', 'Update a User'),
            ('u_o_d', 'Update Own Details'),
            ('d_a_u', 'Delete a User'),
            ('c_n_o', 'Create new Order'),
            ('v_a_o', 'View an Order'),
            ('v_o_o', 'View Own Order'),
            ('u_a_o', 'Update an Order'),
            ('u_o_o', 'Update Own Order'),
            ('d_a_o', 'Delete an Order'),
            ('d_o_o', 'Delete Own Order'),
            ('l_a_o', 'List all Orders'),
            ('l_o_o', 'List Own Orders')
        """
    )
    op.execute(
        """
        INSERT INTO role_privileges (role_id, privilege_id)
        VALUES
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'c_n_u')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'l_a_u')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'v_a_u')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'v_o_d')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'u_a_u')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'u_o_d')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'd_a_u')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'c_n_o')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'v_a_o')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'v_o_o')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'u_a_o')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'u_o_o')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'd_a_o')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'd_o_o')),
            ((SELECT id FROM roles WHERE key = 'admin'), (SELECT id FROM privileges WHERE key = 'l_a_o')),
            ((SELECT id FROM roles WHERE key = 'customer'), (SELECT id FROM privileges WHERE key = 'v_o_d')),
            ((SELECT id FROM roles WHERE key = 'customer'), (SELECT id FROM privileges WHERE key = 'u_o_d')),
            ((SELECT id FROM roles WHERE key = 'customer'), (SELECT id FROM privileges WHERE key = 'c_n_o')),
            ((SELECT id FROM roles WHERE key = 'customer'), (SELECT id FROM privileges WHERE key = 'v_o_o')),
            ((SELECT id FROM roles WHERE key = 'customer'), (SELECT id FROM privileges WHERE key = 'u_o_o')),
            ((SELECT id FROM roles WHERE key = 'customer'), (SELECT id FROM privileges WHERE key = 'd_o_o')),
            ((SELECT id FROM roles WHERE key = 'customer'), (SELECT id FROM privileges WHERE key = 'l_o_o'))
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM role_privileges
        WHERE role_id IN (
            SELECT id FROM roles WHERE key IN ('admin', 'customer')
        )
    """)
    op.execute("""
        DELETE FROM privileges
        WHERE key IN (
            'c_n_u', 'l_a_u', 'v_a_u', 'v_o_d', 'u_a_u', 'u_o_d', 'd_a_u',
            'c_n_o', 'v_a_o', 'v_o_o', 'u_a_o', 'u_o_o',
            'd_a_o', 'd_o_o', 'l_a_o', 'l_o_o'
        )
    """)
    op.execute("""
        DELETE FROM roles
        WHERE key IN ('admin', 'customer')
    """)
