from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Towns import Town
from UK_Town_Distance import Town_Distances
from jinja2 import Template

def get_session():
    db = 'sqlite:///C:\\Users\\timwi\\Documents\\work\\other sql\\uk_towns.db'
    engine = create_engine(db)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def test_find_town_by_id():  #working
    session = get_session()
    this_town = Town()
    test_town = this_town.get_town_by_id(session, 44)
    print(test_town)
    assert test_town.name == 'Abbots Leigh'

def test_find_list_of_towns_by_initial_charas(): #working
    session = get_session()
    this_town = Town()
    list_of_towns = this_town.find_list_of_town_by_initial_charas(session, 'Anw')
    town_1 = list_of_towns[0]
    town_2 = list_of_towns[1]
    assert (town_1.name, town_2.name)  == ('Anwick', 'Anwoth')

def test_calculate_distance(): #working
    this_town = Town()
    coords_1 = (51.18291, -0.63098)
    coords_2 = (51.00283, -2.41825)
    distance = this_town.calculate_distance(coords_1, coords_2)
    assert distance == (126.8008447085739, 78.7903920532676)

def test_read_all_towns_in_DB(): #working
    session = get_session()
    this_town = Town()
    all_towns = this_town.read_all_town_in_DB(session)
    assert len(all_towns) == 1799
    
def test_obtain_towns_within_specified_arc_miles(): #working
    session = get_session()
    this_distance = Town_Distances()
    all_towns_in_arc = this_distance.obtain_towns_within_specified_arc_miles(session, 2, 5, 50)
    assert len(all_towns_in_arc) == 172
    # The following assert will fail becouse  all_towns_in_arc is the array of the 348 towns
    # rather then just the number 348, so the question is how could this array be stored and
    # then the results in all_towns_in_arc be checked against it ?
    # assert all_towns_in_arc == 348

def test_obtain_towns_within_specified_arc_miles_to_max_number(): #working
    session = get_session()
    this_distance = Town_Distances()
    all_towns_in_arc = this_distance.obtain_towns_within_specified_arc_miles_to_max_number(session, 2, 5, 100, 5)
    assert len(all_towns_in_arc) == 5

def test_obtain_town_details_for_specified_group(): #working
    session = get_session()
    this_distance = Town_Distances()
    all_towns_in_arc = this_distance.obtain_towns_within_specified_arc_miles(session, 2, 5, 100)
    this_town = Town()
    towns_details = this_town.obtain_town_details_for_specified_group(session, all_towns_in_arc)
    town_1 = towns_details[0]
    town_2 = towns_details[1]
    town_3 = towns_details[2]
    assert (town_1[1], town_2[1], town_3[1])  == ("Aaron's Hill", 'Abberley', 'Abberton')


def test_array_creation(): #working
    towns2 = [
        [1, [-73.897156, 40.94465]],
        [2, [-74, 40.71]]
    ]
    #assert (towns2[0][0] == 1)
    assert (towns2[0][1], towns2[1][1] == [-73.897156, 40.94465], [-74, 40.71])

def test_conversion_of_text_to_number(): #working
    string1 = '126.8008447085739'
    string2 = '78.7903920532676'
    float1 = float(string1)
    float2 = float(string2)
    assert (float1,float2) == (126.8008447085739, 78.7903920532676)

# WARNING - this test generates the distance between the town with ID of 1
#           and all of the other towns, in the nyc_town_distances table
#           so do NOT run it unless you are re-creating the database and need to test this feature
# def test_generate_one_town_to_town_distance_row():
#     session = get_session()
#     this_distance = town_Distances()
#     all_other_distances = this_distance.create_one_towns_distances(session, 1)
#     assert all_other_distances == 1639


# WARNING - this test generates the distances (between all of the towns )
#           in the nyc_town_distances table, and the last time is was run
#           it took 1:45:44 to complete
#           So do NOT run it unless you are re-creating the database
# def test_generate_all_town_to_town_distance_rows():
#     session = get_session()
#     this_distance =town_Distances()
#     all_other_distances = this_distance.create_all_towns_distances(session)
#     assert all_other_distances == 2687960
