from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tag = Table('tag', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('tag_name', VARCHAR(length=80)),
)

tags = Table('tags', pre_meta,
    Column('tag_id', INTEGER),
    Column('recipe_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tag'].drop()
    pre_meta.tables['tags'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tag'].create()
    pre_meta.tables['tags'].create()
