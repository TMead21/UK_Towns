from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from Towns import Town

# The base class which our objects will be defined on.
Base = declarative_base()


class Town_Distances(Base):
    __tablename__ = 'uk_town_distances'

    # Every SQLAlchemy table should have a primary key named 'id'
    id = Column(Integer, primary_key=True)

    # starting_town_id needs to be an Index - how is this coded?
    starting_town_id = Column(Integer, index=True)
    ending_town_id = Column(Integer)
    kilometres = Column(Integer)
    miles = Column(Integer)
    #drive_time = Column(Time)

    def __init__(self, starting_town_id=None, ending_town_id=None, kilometres=None, miles=None):
        self.starting_town_id = starting_town_id
        self.ending_town_id = ending_town_id
        self.kilometres = kilometres
        self.miles = miles

    # Lets us print out a user object conveniently.
    def __repr__(self):
        return "<uk_town_Distances(id = '%s', starting_town_id='%s', ending_town_id='%s', \
        kilometres'%s', miles'%s')>" % (
            self.id, self.starting_town_id, self.ending_town_id, \
            self.kilometres, self.miles)

    def get_engine(self, db):
        engine = create_engine(db)
        return engine

    def get_session(self, engine):
        # Creates a new session to the database by using the engine we described.
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def create_one_towns_distances(self, session, town_id):
        # do rows already exist for the requested town in town_distances?
        #   if so, error "rows already exist in town_distances"
        #   if not:-
        #       obtain lat/long for requested town
        this_town = Town()
        starting_town = this_town.get_town_by_id(session, town_id)
        starting_town_co_ords = (starting_town.latitude, starting_town.longitude)
        #
        #       read thro' the towns table and for each one that is not the requested town
        list_of_towns = session.query(Town) \
            .filter(Town.id != town_id) \
            .all()
        # read thro' list_of_towns
        town_distances = Town_Distances()
        for other_town in list_of_towns:
            end_town_co_ords = (other_town.latitude, other_town.longitude)
            # calculate the distance in kilometres and miles
            distance = this_town.calculate_distance(starting_town_co_ords, end_town_co_ords)
            # write a row to the town_distances table
            # me = User('admin', 'admin@example.com')
            town_distances = Town_Distances(town_id, other_town.id, distance[0], distance[1])
            #town_distances.insert().values((town_id, other_town.id, distance[0], distance[1]))
            session.add(town_distances)
        session.commit()
        return len(list_of_towns)

    def create_all_towns_distances(self, session):
        this_town = Town()
        list_of_all_towns = this_town.read_all_towns_in_DB(session)
        town_distances = Town_Distances()
        rows_created = 0
        for town in list_of_all_towns:
            rows_created = rows_created + town_distances.create_one_towns_distances(session, town.id)
        return rows_created

    def read_town_to_town_distance_rows(self, session, id):
        town_by_id = session.query(Town_Distances) \
            .filter(Town_Distances.starting_town_id == id) \
            .all()
        return town_by_id

    def obtain_towns_within_specified_arc_miles(self, session, town_id, min_miles, max_miles):
        town_by_id = session.query(Town_Distances) \
            .filter( \
            Town_Distances.starting_town_id == town_id, \
            Town_Distances.miles >= min_miles, \
            Town_Distances.miles <= max_miles \
            ) \
            .all()
        return town_by_id

    def obtain_towns_within_specified_arc_miles_to_max_number(self, session, town_id, min_miles, max_miles, max):
        town_by_id = session.query(Town_Distances) \
            .filter( \
            Town_Distances.starting_town_id == town_id, \
            Town_Distances.miles >= min_miles, \
            Town_Distances.miles <= max_miles \
            ) \
            .limit(max).all()
        return town_by_id

if __name__ == '__main__':
    # Create town_Distances object
    this_town = Town_Distances()

    # Get engine
    db = 'sqlite:///C:\\Users\\timwi\\Documents\\work\\other sql\\uk_towns.db'
    # echo=True
    engine = this_town.get_engine(db)
    # Create all tables by issuing CREATE TABLE commands to the DB.
    Base.metadata.create_all(engine)