from db import Session, Booking


def find_booking(booking_id):
    with Session() as session:
        return session.query(Booking).filter(Booking.id == booking_id).first()


def can_cancel_booking(booking_id):
    booking = find_booking(booking_id)

    # check if a dataset the booking was made with exists,
    # because we can't cancel a booking if the dataset is still available (e.g the last 15)
    return find_booking(booking.dataset_id) is None