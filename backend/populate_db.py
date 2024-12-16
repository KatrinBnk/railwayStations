from datetime import datetime
from backend.models.comp import Comp
from backend.models.dates import Date
from backend.models.passengers import Passenger
from backend.models.schedules import Schedule
from backend.models.seats import Seat
from backend.models.staffs import Staff
from backend.models.stations import Station
from backend.models.trains import Train
from backend.models.typeWagon import TypeWagon
from backend.models.users import User
from backend.models.wagons import Wagon

from data import stations_data, type_wagons_data, users_data, passengers_data, trains_data, schedules_data, seats_data, \
    wagons_data, staffs_data, dates_data, comps_data

# Функции заполнения данных

def populate_stations(session):
    for station in stations_data:
        # Проверьте, что все ключи присутствуют в словаре
        if 'id' in station and 'name' in station and 'city' in station:
            new_station = Station(
                id=station['id'],
                name=station['name'],
                city=station['city']
            )
            session.add(new_station)
        else:
            print(f"Недостающие данные для станции: {station}")
    session.commit()

def populate_comps(session):
    for comp in comps_data:
        new_comp = Comp(
            id=comp['id'],
            wagon_id=comp["wagon_id"],
            number_wagon=comp['number_wagon']
        )
        session.add(new_comp)
    session.commit()

def populate_type_wagons(session):
    for type_wagon in type_wagons_data:
        new_type_wagon = TypeWagon(
            id=type_wagon['id'],
            description=type_wagon['description'],
            conveniences=type_wagon['conveniences'],
            count_seats=type_wagon['count_seats']
        )
        session.add(new_type_wagon)
    session.commit()

def populate_users(session):
    for user in users_data:
        new_user = User(email=user['email'], password=user['password'])
        session.add(new_user)
    session.commit()

def populate_passengers(session):
    for passenger in passengers_data:
        if not passenger.get('user_id'):  # Если 'user_id' нет или оно None, то установим None
            passenger['user_id'] = None

        new_passenger = Passenger(
            user_id=passenger['user_id'],
            last_name=passenger['last_name'],
            first_name=passenger['first_name'],
            middle_name=passenger['middle_name'],
            passport=passenger['passport']
        )
        session.add(new_passenger)
    session.commit()

def populate_trains(session):
    for train in trains_data:
        new_train = Train(
            id=train['id'],
            number=train['number'],
            type=train['type']
        )
        session.add(new_train)
    session.commit()

def populate_schedules(session):
    for schedule in schedules_data:
        arrival_time = datetime.strptime(schedule['arrival'], "%H:%M").time() if schedule['arrival'] else None
        departure_time = datetime.strptime(schedule['departure'], "%H:%M").time() if schedule['departure'] else None

        new_schedule = Schedule(
            id=schedule['id'],
            train_id=schedule['train_id'],
            station_id=schedule['station_id'],
            arrival_time=arrival_time,
            departure_time=departure_time,
            day_in=schedule['dayIN']
        )
        session.add(new_schedule)
    session.commit()

def populate_seats(session):
    for seat in seats_data:
        new_seat = Seat(
            id=seat['id'],
            wagon_id=seat['wagon_id'],
            number_seat=seat['number_seat'],
            type_seat=seat['type_seat']
        )
        session.add(new_seat)
    session.commit()

def populate_wagons(session):
    for wagon in wagons_data:
        new_wagon = Wagon(
            id=wagon['id'],
            type=wagon['type_id']
        )
        session.add(new_wagon)
    session.commit()

def populate_staffs(session):
    for staff in staffs_data:
        new_staff = Staff(
            user_id=staff['user_id'],
            station_id=staff['station_id'],
            last_name=staff['last_name'],
            first_name=staff['first_name'],
            middle_name=staff['middle_name'],
            position=staff['position']
        )
        session.add(new_staff)
    session.commit()

def populate_dates(session):
    for date_entry in dates_data:
        date_value = datetime.strptime(date_entry['date'], "%Y-%m-%d").date()

        new_date = Date(
            date=date_value,
            train_id=date_entry['train_id'],
            comp_id=date_entry.get('comp_id')
        )
        session.add(new_date)
    session.commit()

def populate_all(session):
    populate_stations(session)
    populate_comps(session)
    populate_type_wagons(session)
    populate_users(session)
    populate_passengers(session)
    populate_trains(session)
    populate_schedules(session)
    populate_seats(session)
    populate_wagons(session)
    populate_staffs(session)
    populate_dates(session)
