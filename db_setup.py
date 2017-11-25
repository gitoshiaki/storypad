import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Boolean, Text, PickleType

from config import DB_URL

engine = sqlalchemy.create_engine(DB_URL, echo=False)

Base = declarative_base()


class Comics(Base):
    __tablename__ = 'comics'

    title_id = Column(Integer, primary_key=True)
    title = Column(Text)
    title_kana = Column(Text)
    artist = Column(PickleType)
    genre_id = Column(Integer)
    magazine_id = Column(Integer)
    theme17 = Column(PickleType)
    theme48 = Column(PickleType)
    score = Column(Float)
    favorite_count = Column(Integer)
    review_count = Column(Integer)
    story = Column(Text)
    start_year = Column(Integer)
    img = Column(Text)
    url = Column(Text)
    recommend = Column(PickleType)


class Genres(Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(Text)


class Magazines(Base):
    __tablename__ = 'magazines'

    magazine_id = Column(Integer, primary_key=True)
    magazine_name = Column(Text)


class Artists(Base):
    __tablename__ = 'artists'

    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(Text)


class ComicArtists(Base):
    __tablename__ = 'comic_artists'

    title_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, primary_key=True)


class ComicTheme17(Base):
    __tablename__ = 'comic_theme17'

    title_id = Column(Integer, primary_key=True)
    theme_id = Column(Integer, primary_key=True)


class Theme17(Base):
    __tablename__ = 'theme17'

    theme_id = Column(Integer, primary_key=True)
    theme_name = Column(Text)


class Theme48(Base):
    __tablename__ = 'theme48'

    theme_id = Column(Integer, primary_key=True)
    theme_name = Column(Text)


class ComicTheme48(Base):
    __tablename__ = 'comic_theme48'

    title_id = Column(Integer, primary_key=True)
    theme_id = Column(Integer, primary_key=True)


class Reviews(Base):
    __tablename__ = 'reviews'

    title_id = Column(Integer, primary_key=True)
    review_headers = Column(PickleType)
    review_contents = Column(PickleType)
    comment_title = Column(Text)
    comment_headers = Column(PickleType)
    comment_contents = Column(PickleType)


class ComicReviewNouns(Base):
    __tablename__ = 'comic_review_nouns'

    title_id = Column(Integer, primary_key=True)
    noun_id = Column(Integer, primary_key=True)
    value = Column(Float)


class ReviewNouns(Base):
    __tablename__ = 'review_nouns'

    noun_id = Column(Integer, primary_key=True)
    noun_name = Column(Text)


class ComicStoryNouns(Base):
    __tablename__ = 'comic_story_nouns'

    title_id = Column(Integer, primary_key=True)
    noun_id = Column(Integer, primary_key=True)
    value = Column(Float)


class StoryNouns(Base):
    __tablename__ = 'story_nouns'

    noun_id = Column(Integer, primary_key=True)
    noun_name = Column(Text)


Base.metadata.create_all(engine)
