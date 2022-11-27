from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import (
    Channel, Post
)

from narratives import (
    is_discrediting_the_authorities,
    is_humiliation_of_culture_narrative,
    is_external_influence_narrative,
    is_military_actions_narrative
)

engine = create_engine(f"sqlite:///data/tchannels_narratives.db")

print ('')
print ('> Analyzing narratives')
print ('> ...')

with Session(engine) as session:
    for post in tqdm(session.query(Post).all()):
        if post.message:
            post.discrediting_the_authorities_narrative = is_discrediting_the_authorities(post.message)
            post.humiliation_of_culture_narrative = is_humiliation_of_culture_narrative(post.message)
            post.external_influence_narrative = is_external_influence_narrative(post.message)
            post.military_actions_narrative = is_military_actions_narrative(post.message)

    session.commit()
