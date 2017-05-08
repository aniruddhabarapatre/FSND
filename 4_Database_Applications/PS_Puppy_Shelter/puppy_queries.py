from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def q1_all_puppies_asc_order():
    """Query all of the puppies and return the results in ascending alphabetical order"""
    results = session.query(Puppy.name).order_by(Puppy.name.asc()).all()
    for puppy in results:
        print puppy[0]

q1_all_puppies_asc_order()
