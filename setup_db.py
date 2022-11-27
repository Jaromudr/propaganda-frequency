from sqlalchemy import create_engine
from models import Base

engine = create_engine(f"sqlite:///data/tchannels_narratives.db")
Base.metadata.create_all(engine)