import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/stations/search';

export const searchStationByName = async (name) => {
    return axios.get(API_URL, {
        params: { name },
    }).then(response => response.data);
};

export const searchStationByCode = async (code) => {
    return axios.get(API_URL, {
        params: { code },
    }).then(response => response.data);
};

export const searchStationByCity = async (city) => {
    return axios.get(API_URL, {
        params: { city },
    }).then(response => response.data);
};
