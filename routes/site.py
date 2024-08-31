from flask import Blueprint, render_template

from db import Session, Dataset, Booking
from domain.search import fetch_dataset, fetch_schedule, fetch_route

site = Blueprint('site', __name__)


@site.route('/')
def home():
    return render_template('index.html')


@site.route('/book/<int:dataset_id>/<int:route_id>/<int:schedule_id>')
def book(dataset_id, route_id, schedule_id):
    dataset = fetch_dataset(dataset_id)

    if not dataset:
        return render_template('invalid_dataset.html')

    route = fetch_route(route_id)
    schedule = fetch_schedule(schedule_id)

    return render_template('book.html', dataset_id=dataset_id, schedule=schedule, route=route)

@site.route('/booking/<int:booking_id>')
def booking(booking_id):
    with Session() as session:
        booking = session.query(Booking).filter(Booking.id == booking_id).first()

        if not booking:
            return render_template('invalid_booking.html')

        return render_template('booking.html', booking=booking)