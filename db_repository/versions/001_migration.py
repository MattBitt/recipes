from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tag = Table('tag', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tag_name', String(length=80)),
)

tags = Table('tags', post_meta,
    Column('tag_id', Integer),
    Column('recipe_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tag'].create()
    post_meta.tables['tags'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tag'].drop()
    post_meta.tables['tags'].drop()
