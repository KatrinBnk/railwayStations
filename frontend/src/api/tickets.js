import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const fetchAvailableSeats = async ({ trainId, departureStationId, arrivalStationId, date }) => {
    try {
        const response = await axios.get(`${API_URL}/seats`, {
            params: {
                train_id: trainId,
                departure_station_id: departureStationId,
                arrival_station_id: arrivalStationId,
                date: date,
            },
        });

        console.log("Ответ от API мест:", response.data);
        return response.data;
    } catch (error) {
        console.error("Ошибка при запросе мест:", error);
        throw error;
    }
};
