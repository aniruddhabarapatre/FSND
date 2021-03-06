from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy

import datetime

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

def q1_all_puppies_asc_order():
    """Query all of the puppies and return the results in ascending alphabetical order"""
    results = session.query(Puppy.name).order_by(Puppy.name.asc()).all()
    for puppy in results:
        print puppy[0]

def q2_all_puppies_less_than_6months():
    """Query all of the puppies that are less than 6 months old organized by the youngest first"""
    today = datetime.date.today()
    sixMonths = today - datetime.timedelta(days = 180)
    results = session.query(Puppy.name, Puppy.dateOfBirth).filter(Puppy.dateOfBirth >= sixMonths).order_by(Puppy.dateOfBirth.desc())

    for puppy in results:
        print "{name}: {dob}".format(name=puppy[0], dob=puppy[1])


def q3_all_puppies_by_weight():
    """Query all puppies by ascending weight"""
    results = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()
    for puppy in results:
        print puppy[0], puppy[1]

def q4_all_puppies_by_shelter():
    """Query all puppies grouped by the shelter in which they are staying"""
    results = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    for puppy in results:
        print puppy[0].name, puppy[1]

q1_all_puppies_asc_order()
q2_all_puppies_less_than_6months()
q3_all_puppies_by_weight()
q4_all_puppies_by_shelter()
