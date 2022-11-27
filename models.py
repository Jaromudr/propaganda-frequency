from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import Integer, Text, String, Boolean, DateTime

Base = declarative_base()

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    posts = relationship("Post", back_populates="channel")

    def __repr__(self):
        return f"<Channel {self.username}>"

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), index=True)
    channel = relationship("Channel", back_populates="posts")

    message = Column(Text, nullable=True)
    posted_at = Column(DateTime)

    discrediting_the_authorities_narrative = Column(Boolean)
    humiliation_of_culture_narrative = Column(Boolean)
    external_influence_narrative = Column(Boolean)
    military_actions_narrative = Column(Boolean)
    betrayal_of_partners_narrative = Column(Boolean)
    internal_conflict_narrative = Column(Boolean)
    historical_dependence_narrative = Column(Boolean)
    war_is_secret_duty_narrative = Column(Boolean)
    illegimate_government_narrative = Column(Boolean)
