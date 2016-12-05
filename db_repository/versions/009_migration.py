from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
article = Table('article', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('link', String(length=250)),
    Column('title', String(length=140)),
    Column('source', String(length=50)),
    Column('reader', String),
)

impressions = Table('impressions', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('thoughts', String(length=500)),
    Column('title', String(length=140)),
    Column('category', String(length=50)),
    Column('source', String(length=50)),
    Column('writer', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['article'].columns['reader'].create()
    post_meta.tables['impressions'].columns['writer'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['article'].columns['reader'].drop()
    post_meta.tables['impressions'].columns['writer'].drop()
