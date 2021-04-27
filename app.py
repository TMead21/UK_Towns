from flask import Flask, render_template
from flask import flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Towns import Town
from UK_Town_Distance import Town_Distances
from operator import attrgetter
from Form import LoginForm1, LoginForm2, LoginForm3, LoginForm4
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


def get_session():
    db = 'sqlite:///C:\\Users\\timwi\\Documents\\work\\other sql\\uk_towns.db'
    engine = create_engine(db)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@app.route('/', methods=['GET', 'POST'])
def parameters():
    session = get_session()
    towns = session.query(Town).all()
    # https://docs.python.org/3/howto/sorting.html
    townsSorted = sorted(towns, key=attrgetter('name'))
    choicesCentre = []
    for town in townsSorted:
        townDetails = (town.id, town.name)
        choicesCentre.append(townDetails)
    # choicesCentre = [(1, "town One"), (2, "town Two"), (3, "town Three")]
    form1 = LoginForm1(choicesCentre)
    choicesMin = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    form2 = LoginForm2(choicesMin)
    choicesMax = [(1, 1), (5, 5), (10, 10), (15, 15), (20, 20)]
    form3 = LoginForm3(choicesMax)
    choicesNumber = [(5, 5), (10, 10), (15, 15), (20, 20), (1300, 1300)]
    form4 = LoginForm4(choicesNumber)
    # TODO: validation (to ensure that something was entered) is not working
    if form1.validate_on_submit():
        # flash('City parameters for towns {}'.format(
        #     form1.searchCentre.data))
        # flash('City parameters for minimum {}'.format(
        #     form2.minimum.data))
        # flash('City parameters for maximum {}'.format(
        #     form3.maximum.data))
        # flash('City parameters for town Number {}'.format(
        #     form4.townNumber.data))
        this_distance = Town_Distances()
        all_towns_in_arc = \
            this_distance.obtain_towns_within_specified_arc_miles_to_max_number\
                (session, form1.searchCentre.data,
                 form2.minimum.data, form3.maximum.data, form4.townNumber.data)
        this_town = Town()
        towns_details = this_town.obtain_town_details_for_specified_group(session, all_towns_in_arc)
        alltowns = []
        allNames = []
        for town in towns_details:
            allNames.append(town[1])
            latLong = [float(town[3]), float(town[2])]
            alltowns.append(latLong)
        #return redirect('/')
        # To centre the towns html pass the lat/long of the selected town
        #   So first obtain the lat/long
        selected_town = this_town.get_town_by_id(session, form1.searchCentre.data)
        return render_template("Towns.html", towns=alltowns, names=allNames, selected_town=selected_town)
    return render_template('parameters.html', title='Enter Parameters', form1=form1, form2=form2, form3=form3,
                           form4=form4)


if __name__ == '__main__':
    app.run(debug=True)
