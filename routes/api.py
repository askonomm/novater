from flask import Blueprint, request, render_template

from db import Session, Booking
from domain.search import fetch_dataset, fetch_routes, fetch_route, fetch_schedule

api = Blueprint('api', __name__)


@api.post('/search')
def search():
    # get request data
    data = request.form
    start = data['start'] if 'start' in data else None
    end = data['end'] if 'end' in data else None

    # validate data
    if not start and not end:
        return "Palun sisesta algus- ja lõpp-punkt"

    if not start:
        return "Palun sisesta algus-punkt"

    if not end:
        return "Palun sisesta lõpp-punkt"

    result = fetch_routes(start, end)

    # could not find results for our criteria
    if not result or len(result['items']) == 0:
        return "Ei leidnud ühtegi tulemust"

    # all good, return data
    return render_template('api/results.html', data=result)


@api.post('/book/<int:dataset_id>/<int:route_id>/<int:schedule_id>')
def book(dataset_id, route_id, schedule_id):
    dataset = fetch_dataset(dataset_id)

    if not dataset:
        return render_template('api/invalid_dataset_str.html')

    # validate request data
    data = request.form
    first_name = data['first_name'] if 'first_name' in data else None
    last_name = data['last_name'] if 'last_name' in data else None

    if not first_name or not last_name:
        return "Palun sisesta nii ees- kui ka perekonnanimi"

    # create booking
    route = fetch_route(route_id)
    schedule = fetch_schedule(schedule_id)
    from_name = route['from_name']
    to_name = route['to_name']
    price = schedule['price']
    operator_name = schedule['company_state']

    with Session() as session:
        booking = Booking(
            first_name=first_name,
            last_name=last_name,
            from_name=from_name,
            to_name=to_name,
            start_date=schedule['start_date'],
            start_timezone_type=schedule['start_timezone_type'],
            start_timezone=schedule['start_timezone'],
            end_date=schedule['end_date'],
            end_timezone_type=schedule['end_timezone_type'],
            end_timezone=schedule['end_timezone'],
            price=price,
            operator_name=operator_name
        )

        session.add(booking)
        session.commit()

        return render_template('api/booking.html', booking=booking)
