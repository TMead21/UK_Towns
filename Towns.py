from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from geopy import distance

# The base class which our objects will be defined on.
Base = declarative_base()

class Town(Base):
    __tablename__ = 'uk_towns'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    county = Column(String)
    country = Column(String)
    grid_reference = Column(String)
    easting = Column(Integer)
    northing = Column(Integer)
    latitude = Column(Numeric(8, 5))
    longitude = Column(Numeric(8, 5))
    elevation = Column(Integer)
    postcode_sector = Column(String)
    local_government_area = Column(String)
    nuts_region = Column(String)
    type = Column(String)


    # Lets us print out a user object conveniently.
    def __repr__(self):
       return "<town(id = '%s', name = '%s', grid_reference='%s', postcode_sector='%s', \
        City'%s', latitude'%s', longitude'%s')>" % (
                               self.id, self.name, self.grid_reference, self.postcode_sector, \
                               self.county, self.latitude, self.longitude)


    def get_engine(self, db):
        engine = create_engine(db)
        return engine

    def get_session(self, engine):
        # Creates a new session to the database by using the engine we described.
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def get_town_by_id(self, session, id):
        # Now let's query the user that has the e-mail address ed@google.com
        # SQLAlchemy will construct a JOIN query automatically.
        town_by_id = session.query(Town) \
            .filter(Town.id == id) \
            .first()
        return town_by_id

    def find_list_of_town_by_initial_charas(self, session, initial_chara):
        #s.query(Employee).filter(Employee.name.startswith("C")).one().name
        list_of_town = session.query(Town) \
            .filter(Town.name.startswith(initial_chara)) \
            .all()
        #return ('Aldersley', 'Aldridge', 'All Saints', 'Allesley', 'Allesley Green', 'Alum Rock')
        return list_of_town

    def calculate_distance(self, coords_1, coords_2):
        #coords_1 = (52.2296756, 21.0122287)
        #coords_2 = (52.406374, 16.9251681)
        # amend the calculate both kilometres and miles
        return (distance.distance(coords_1, coords_2).km, distance.distance(coords_1, coords_2).miles)

    def read_all_town_in_DB(self, session):
        return session.query(Town).all()

    def obtain_town_details_for_specified_group(self, session, all_town_in_arc):
        this_town = Town()
        towns_details = []
        for town in all_town_in_arc:
            town_id = town.ending_town_id
            town_detail = this_town.get_town_by_id(session, town_id)
            towns_details.append([town_detail.id,town_detail.name,town_detail.latitude,town_detail.longitude])
        return towns_details


if __name__ == '__main__':
    # Create UK_Town object
    this_town = Town()
