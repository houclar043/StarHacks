
import csv
from dataclasses import dataclass
import plotly.graph_objects as go


@dataclass
class Person:
    """
    A data type representing a specific person who took the anxiety survey.

    Attributes:
        - age_group: the age group the person belongs to
        - anxiety_score: the generalized anxiety severity score of this person
        - before_distancing: the person's mental health compared to before physical distancing
        - concern_canada: the person's concern about the impact of COVID-19 on Canadian
          population's health
        - concern_social: the person's concern about the impact of COVID-19 on maintaining
          social ties
        - perceived: the person's perceived mental health
        - financial: how COVID-19 impacts the person's ability to meet financial
          obligations or essential needs


    Representation invariants:
        - 1 <= age_group <= 6
        - 0.0 <= anxiety_score <= 21.0
        - 1.0 <= before_distancing <= 9.0
        - 1.0 <= concern_canada <= 9.0
        - 1.0 <= concern_social <= 9.0
        - 0.0 <= perceived <= 9.0
        - 1.0 <= financial <= 9.0
    """
    age_group: int
    anxiety_score: float
    before_distancing: float
    concern_canada: float
    concern_social: float
    perceived: float
    financial: float


def load_data(filename: str) -> list[Person]:
    """
    Return a list that contains the dataclass Person.
    The data in filename is in a csv format with 43 columns. We have chosen 7 specific columns to
    use as the instance attributes for Person.
    """
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # skip the header
        data = [process_row(row) for row in reader]

    return data


def process_row(row: list[str]) -> Person:
    """
    Convert a row of anxiety survey data to Person object.
    """
    p = Person(age_group=int(row[31]), anxiety_score=float(row[28]),
               before_distancing=float(row[3]),
               concern_canada=float(row[18]), concern_social=float(row[22]),
               perceived=float(row[2]),
               financial=float(row[37]))
    p.financial = abs(p.financial - 6)

    return p


def calculate_avg(attr: str, age_group: list) -> float:
    """
    Return a float representing the average for the attribute of the age group.
    """
    count = 0
    length = len(age_group)
    attr_avg_variable = attr + '_avg'
    not_stated = globals()[attr_avg_variable][0][2]

    for person in age_group:
        a = getattr(person, attr)
        if a == not_stated:
            length -= 1
        else:
            count += a

    return count / length


def formula(age_group: dict) -> list[float]:
    """
    Return a list of 6 float variables that each represent
    the overall anxiety score of each age group.

    We created a formula that uses all attributes in Person (except age_group) and calculates
    their overall anxiety score.

    The formula is as follows:
    anxiety_score * 30% + before_distancing * 20% + concern_canada * 10% + concern_social * 10%
    + perceived * 10% + financial * 20%
    """
    percentage = [0.3, 0.2, 0.1, 0.1, 0.1, 0.2]
    # r is the list of the range of answers (ie. anxiety score is 0-21)
    r = [22, 5, 5, 4, 5, 5]
    y_values = []
    for i in range(1, 7):
        for j in range(0, 6):
            # Divide the group's attribute average by the attribute's corresponding range and
            # multiply by its corresponding percentage
            age_group[i][j] = (age_group[i][j] / r[j]) * percentage[j]
        s = sum(age_group[i])
        y_values.append(s)

    return y_values


# Global Variables:

# Age group lists:
age_groups = []
first_age = []
second_age = []
third_age = []
fourth_age = []
fifth_age = []
sixth_age = []

# Attribute average lists:
anxiety_score_avg = []
before_distancing_avg = []
concern_canada_avg = []
concern_social_avg = []
perceived_avg = []
financial_avg = []


def arrange(person: Person) -> None:
    """
    Organize person into its specific age group list.
    """
    if person.age_group == 1:
        first_age.append(person)
    elif person.age_group == 2:
        second_age.append(person)
    elif person.age_group == 3:
        third_age.append(person)
    elif person.age_group == 4:
        fourth_age.append(person)
    elif person.age_group == 5:
        fifth_age.append(person)
    else:
        sixth_age.append(person)


def run_example(filename: str) -> None:
    """
    Run an example to display graphs based on the data in filename.

    To call this function:
        - Make sure you see that the 'anxiety_survey_canada_2020' folder is in the same directory
          as this file
        - Use an argument for filename like: 'anxiety_survey_canada_2020'
    """
    result = load_data(filename)

    attributes = ['anxiety_score', 'before_distancing',
                  'concern_canada', 'concern_social', 'perceived', 'financial']

    age_groups.extend([first_age, second_age, third_age, fourth_age, fifth_age, sixth_age])

    # The first element of each list is a tuple containing 3 integers
    # The first integer: the lowest number people can pick for questions about specific attributes
    # The second integer: the highest number people can pick for questions about specific attributes
    # The last integer: the number that indicates the person did not respond to this question
    anxiety_score_avg.insert(0, (0, 21, 99))
    before_distancing_avg.insert(0, (1, 5, 9))
    concern_canada_avg.insert(0, (1, 5, 9))
    concern_social_avg.insert(0, (1, 4, 9))
    perceived_avg.insert(0, (1, 5, 9))
    financial_avg.insert(0, (1, 5, 9))

    list_avg = []

    # Append all lists for the attribute average lists onto list_avg
    for attribute in attributes:
        attribute = attribute + '_avg'
        list_avg.append(globals()[attribute])

    for person in result:
        arrange(person)

    for attribute in attributes:
        for group in age_groups:
            avg = calculate_avg(attribute, group)
            attr_avg_variable = attribute + '_avg'
            globals()[attr_avg_variable].append(avg)

    list_without_formula = []
    group_to_attributes = {}
    for i in range(1, 7):
        for e in list_avg:
            list_without_formula.append(e[i])
            group_to_attributes[i] = list_without_formula
        list_without_formula = []

    plot_data(group_to_attributes, attributes)


def plot_data(group_to_formula: dict[int, list[float]], attributes: list[str]) -> None:
    """
    Create a graph for each attribute and for the overall anxiety score across each age group.

    Preconditions:
        - group_to_formula != {}
    """
    # Obtain the first element of each attribute average list and store it in ranges
    ranges = [()] * len(attributes)
    for i in range(len(attributes)):
        attr_avg_variable = attributes[i] + '_avg'
        ranges[i] = globals()[attr_avg_variable].pop(0)

    # x-values of the graphs
    groups = ['15-24', '25-34', '35-44', '45-54', '55-64', '65+']

    x_axis_title = "Age groups"

    # Create the figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=groups, y=formula(group_to_formula), name='Overall Score'))

    fig.add_trace(
        go.Scatter(
            x=groups,
            y=anxiety_score_avg,
            name='Anxiety Score',
            line=dict(color="#CF3333"),
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=groups,
            y=before_distancing_avg,
            name="Before Distancing",
            line=dict(color="#CFCA33"),
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=groups,
            y=concern_canada_avg,
            name="Concern for Canadians",
            line=dict(color="#8BCF33"),
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=groups,
            y=concern_social_avg,
            name="Concern for Social Impact",
            line=dict(color="#33CFCF"),
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=groups,
            y=perceived_avg,
            name="Perceived Mental Health",
            line=dict(color="#334ACF"),
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=groups,
            y=financial_avg,
            name="Financial Impact",
            line=dict(color="#CF33C2"),
        )
    )

    # Configure the starting figure
    fig.update_layout(title='Specific Attributes Across Different Age Groups',
                      xaxis_title=x_axis_title,
                      yaxis_title='Calculated Averages')

    # Configure the buttons and other figures
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="down",
                # Coordinates of the buttons
                x=-0.1,
                y=0.9,
                showactive=True,
                buttons=list(
                    [
                        dict(
                            label="All Graphs",
                            method="update",
                            args=[
                                # True and False values correspond to the order in which we added
                                # each trace (e.g. since we added the trace for Overall Score first,
                                # it corresponds to the first value in the True and False list)
                                {"visible": [True, True, True, True, True, True, True]},
                                {"title.text": "Specific Attributes Across Different Age Groups",
                                 "xaxis.title.text":
                                     x_axis_title,
                                 "yaxis.title.text": "Calculated averages", },
                            ],
                        ),
                        dict(
                            label="Overall Anxiety Score",
                            method="update",
                            args=[
                                {"visible": [True, False, False, False, False, False, False]},
                                {"title.text": "Relationship between Overall Anxiety Score and "
                                               "Different Age Groups",
                                 "xaxis.title.text": x_axis_title,
                                 "yaxis.title.text": "Calculated overall anxiety score "
                                                     "(ranging from 0 to 1)", },
                            ],
                        ),
                        dict(
                            label="Anxiety Level",
                            method="update",
                            args=[
                                {"visible": [False, True, False, False, False, False, False]},
                                {"title.text": "Relationship between Generalized Anxiety Severity "
                                               "Score and Different "
                                               "Age Groups ", "xaxis.title.text": x_axis_title,
                                 "yaxis.title.text": f'Calculated generalized anxiety score average'
                                                     f' 'f'(ranging '
                                                     f'from {ranges[0][0]} '
                                                     f'to {ranges[0][1]})', },
                            ],
                        ),
                        dict(
                            label="Before Distancing",
                            method="update",
                            args=[
                                {"visible": [False, False, True, False, False, False, False]},
                                {"title.text": "Relationship between Mental Health Levels before "
                                               "Distancing and Different Age Groups",
                                 "xaxis.title.text": x_axis_title,
                                 "yaxis.title.text": f'Calculated before distancing score average '
                                                     f'(ranging from {ranges[1][0]} '
                                                     f'to {ranges[1][1]})'},
                            ],
                        ),
                        dict(
                            label="Concern for Canadians",
                            method="update",
                            args=[
                                {"visible": [False, False, False, True, False, False, False]},
                                {"title.text": "Relationship between Concern of Impact of COVID-19 "
                                               "on Canadian Population Health and Different "
                                               "Age Groups", "xaxis.title.text": x_axis_title,
                                 "yaxis.title.text": f'Calculated concern for Canadians score '
                                                     f'average (ranging from {ranges[2][0]} '
                                                     f'to {ranges[2][1]})'},
                            ],
                        ),
                        dict(
                            label="Concern for Impact on Social Life",
                            method="update",
                            args=[
                                {"visible": [False, False, False, False, True, False, False]},
                                {"title.text": "Relationship between Concern of Impact of COVID-19 "
                                               "on Maintaining Social Ties and Different "
                                               "Age Groups", "xaxis.title.text": x_axis_title,
                                 "yaxis.title.text": f'Calculated concern for social impact score '
                                                     f'average (ranging from {ranges[3][0]} '
                                                     f'to {ranges[3][1]})'},
                            ],
                        ),
                        dict(
                            label="Perceived Mental Health",
                            method="update",
                            args=[
                                {"visible": [False, False, False, False, False, True, False]},
                                {"title.text": "Relationship between Perceived Mental Health Level "
                                               "and Different Age Groups",
                                 "xaxis.title.text": x_axis_title,
                                 "yaxis.title.text": f'Calculated perceived mental health score '
                                                     f'average (ranging from {ranges[4][0]} '
                                                     f'to {ranges[4][1]})'},
                            ],
                        ),
                        dict(
                            label="Financial Impact",
                            method="update",
                            args=[
                                {"visible": [False, False, False, False, False, False, True]},
                                {"title.text": "Relationship between Impact of COVID-19 on Person's"
                                               " Ability to Meet Financial Obligations or Essential"
                                               " Needs and Different Age Groups",
                                 "xaxis.title.text": x_axis_title,
                                 "yaxis.title.text": f'Calculated financial impact score average '
                                                     f'(ranging from {ranges[5][0]} '
                                                     f'to {ranges[5][1]})'},
                            ],
                        ),
                    ]
                ),
            )
        ],
    )

    # Show the figure in the browser
    fig.show()


run_example('anxiety_survey_canada_2020.csv')
