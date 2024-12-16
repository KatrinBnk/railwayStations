from flask import Blueprint, request, jsonify
from backend.models.stations import Station

stations_bp = Blueprint('stations', __name__)

@stations_bp.route('/stations/search', methods=['GET'])
def search_stations():
    name = request.args.get('name')
    code = request.args.get('code')
    city = request.args.get('city')

    query = Station.query

    # Фильтрация по имени станции
    if name:
        query = query.filter(Station.name.ilike(f"%{name}%"))

    # Фильтрация по коду станции
    if code:
        try:
            code = int(code)
        except ValueError:
            return jsonify({"error": "Код станции - integer."}), 400
        query = query.filter(Station.id == code)

    # Фильтрация по городу
    if city:
        query = query.filter(Station.city.ilike(f"%{city}%"))

    stations = query.all()

    if not stations:
        return jsonify({"message": "Станция не найдена."}), 404

    return jsonify([station.to_dict() for station in stations])


@stations_bp.route('/stations/all', methods=['GET'])
def get_all_stations():
    stations = Station.query.all()

    if not stations:
        return jsonify({"message": "Станция не найдена."}), 404

    return jsonify([station.to_dict() for station in stations])