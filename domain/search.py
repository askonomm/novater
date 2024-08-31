from sqlalchemy.orm import joinedload
from db import Dataset, Route, Schedule, Session
from domain.utils import get_current_time_in_tz


def ensure_only_last_15_datasets(session):
    # fetch all datasets
    datasets = session.query(Dataset).order_by(Dataset.id).all()

    # if we have more than 15 datasets, let's delete the oldest ones
    if len(datasets) > 15:
        for dataset in datasets[15:]:
            session.delete(dataset)

        session.commit()


def fetch_fresh_dataset():
    # fetch data from the API
    # we will just return some dummy data for now
    data = {
        'id': '4b5658be-0cf3-414e-8a99-78d5d82a9dc1',
        'expires': {
            'date': '2024-08-31 23:59:59.000000',
            'timezone_type': 2,
            'timezone': 'Z'
        },
        'routes': [
            {
                'id': '4b5658be-0cf3-414e-8a99-78d5d82a9dc2',
                'from': {
                    'id': '4b5658be-0cf3-414e-8a99-78d5d82a9dc3',
                    'name': 'London'
                },
                'to': {
                    'id': '4b5658be-0cf3-414e-8a99-78d5d82a9dc4',
                    'name': 'Paris'
                },
                'distance': 350,
                'schedule': [
                    {
                        'id': '4b5658be-0cf3-414e-8a99-78d5d82a9dc6',
                        'price': 50,
                        'start': {
                            'date': '2024-08-31 08:00:00.000000',
                            'timezone_type': 3,
                            'timezone': 'Europe/Tallinn'
                        },
                        'end': {
                            'date': '2024-08-31 10:00:00.000000',
                            'timezone_type': 3,
                            'timezone': 'Europe/Tallinn'
                        },
                        'company': {
                            'id': '4b5658be-0cf3-414e-8a99-78d5d82a9dc9',
                            'state': 'NoBus'
                        }
                    }
                ]
            },
            {
                'id': '4b5258be-0cf3-414e-8a99-78d5d82a9dc2',
                'from': {
                    'id': '4b5654e-0cf3-414e-8a99-78d5d82a9dc3',
                    'name': 'Paris'
                },
                'to': {
                    'id': '4b5658b6-0cf3-414e-8a99-78d5d82a9dc4',
                    'name': 'London'
                },
                'distance': 350,
                'schedule': [
                    {
                        'id': '4b5659e-0cf3-414e-8a99-78d5d82a9dc6',
                        'price': 50,
                        'start': {
                            'date': '2024-08-31 08:00:00.000000',
                            'timezone_type': 3,
                            'timezone': 'Europe/Tallinn'
                        },
                        'end': {
                            'date': '2024-08-31 10:00:00.000000',
                            'timezone_type': 3,
                            'timezone': 'Europe/Tallinn'
                        },
                        'company': {
                            'id': '4b5658b3cf3-414e-8a99-78d5d82a9dc9',
                            'state': 'NoBus'
                        }
                    }
                ]
            }
        ]
    }

    # no data available
    if not data:
        return None

    # create a new dataset
    # valid until, and take timezone in data['expires']['timezone'], and type in data['expires']['timezone_type'] into account
    with Session() as session:
        dataset = Dataset(
            expires_date=data['expires']['date'],
            expires_timezone_type=data['expires']['timezone_type'],
            expires_timezone=data['expires']['timezone']
        )

        # add routes
        for route_data in data['routes']:
            route = Route(
                uuid=route_data['id'],
                from_id=route_data['from']['id'],
                from_name=route_data['from']['name'],
                to_id=route_data['to']['id'],
                to_name=route_data['to']['name'],
                distance=route_data['distance']
            )

            # add schedules
            for schedule_data in route_data['schedule']:
                schedule = Schedule(
                    uuid=schedule_data['id'],
                    price=schedule_data['price'],
                    start_date=schedule_data['start']['date'],
                    start_timezone_type=schedule_data['start']['timezone_type'],
                    start_timezone=schedule_data['start']['timezone'],
                    end_date=schedule_data['end']['date'],
                    end_timezone_type=schedule_data['end']['timezone_type'],
                    end_timezone=schedule_data['end']['timezone'],
                    company_id=schedule_data['company']['id'],
                    company_state=schedule_data['company']['state']
                )

                route.schedule.append(schedule)

            dataset.routes.append(route)

        session.add(dataset)
        session.commit()

        ensure_only_last_15_datasets(session)

        return dataset


def fetch_latest_dataset():
    with Session() as session:
        # since we don't know what timezone the data comes in,
        # lets fetch the last dataset as the base for the timezone

        # NOTE: this is a simplification, in a real-world scenario
        # we would need to handle timezones more carefully and can't
        # just assume that the last dataset is in the same timezone
        base_dataset = session.query(Dataset).first()

        # if no dataset exists, let's fetch a fresh one
        if not base_dataset:
            return fetch_fresh_dataset()

        # get the current time in the timezone of the base dataset
        current_time = get_current_time_in_tz(
            base_dataset.expires_timezone,
            base_dataset.expires_timezone_type
        )

        # let's see if we have any datasets that are still valid
        dataset = session.query(Dataset) \
            .options(joinedload(Dataset.routes).joinedload(Route.schedule)) \
            .filter(Dataset.expires_date > current_time.strftime('%Y-%m-%d %H:%M:%S')) \
            .order_by(Dataset.expires_date.desc()) \
            .first()

        # if we have any valid datasets, let's return the latest one
        if dataset:
            return dataset

        # if we don't have any valid datasets, let's fetch a fresh data
        return fetch_fresh_dataset()


def fetch_dataset(dataset_id):
    with Session() as session:
        # since we don't know what timezone the data comes in,
        # lets fetch the last dataset as the base for the timezone

        # NOTE: this is a simplification, in a real-world scenario
        # we would need to handle timezones more carefully and can't
        # just assume that the last dataset is in the same timezone
        base_dataset = session.query(Dataset).first()

        # if no dataset exists
        if not base_dataset:
            return None

        # get the current time in the timezone of the base dataset
        current_time = get_current_time_in_tz(
            base_dataset.expires_timezone,
            base_dataset.expires_timezone_type
        )

        dataset = session.query(Dataset) \
            .options(joinedload(Dataset.routes).joinedload(Route.schedule)) \
            .filter(Dataset.id == dataset_id) \
            .filter(Dataset.expires_date > current_time.strftime('%Y-%m-%d %H:%M:%S')) \
            .first()

        return dataset.to_dict() if dataset else None


def fetch_routes(start_location, end_location):
    dataset = fetch_latest_dataset()

    if not dataset:
        return None

    # find routes that match our criteria
    routes = []
    for route in dataset.routes:
        if route.from_name == start_location and route.to_name == end_location:
            routes.append(route.to_dict())

    return {
        'dataset_id': dataset.id,
        'expires': {
            'date': dataset.expires_date,
            'timezone_type': dataset.expires_timezone_type,
            'timezone': dataset.expires_timezone
        },
        'items': routes
    }


def fetch_route(route_id):
    with Session() as session:
        route = session.query(Route).filter(Route.id == route_id).first()

        return route.to_dict() if route else None


def fetch_schedule(schedule_id):
    with Session() as session:
        schedule = session.query(Schedule).filter(Schedule.id == schedule_id).first()

        return schedule.to_dict() if schedule else None