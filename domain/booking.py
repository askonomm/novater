from db import Session, Booking
from domain.search import fetch_dataset


def find_booking(booking_id):
    with Session() as session:
        return session.query(Booking).filter(Booking.id == booking_id).first()


def can_cancel_booking(booking_id):
    booking = find_booking(booking_id)

    if not booking:
        return False

    # check if a dataset the booking was made with exists,
    # because we can't cancel a booking if the dataset is still available (e.g the last 15)
    return fetch_dataset(booking.dataset_id) is None


def cancel_booking(booking_id):
    with Session() as session:
        booking = session.query(Booking).filter(Booking.id == booking_id).first()

        if not booking:
            return False

        session.delete(booking)
        return True
