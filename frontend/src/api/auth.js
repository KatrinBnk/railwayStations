// loginRequest.js
import axios from 'axios';

const loginRequest = async (form) => {
    try {
        return await axios.post('http://127.0.0.1:5000/login', {
            email: form.email,
            password: form.password
        });
    } catch (error) {
        throw error;
    }
};

export { loginRequest };

const registerRequest = async (form) => {
    try {
        return await axios.post('http://127.0.0.1:5000/register', {
            email: form.email,
            password: form.password,
            first_name: form.first_name,
            last_name: form.last_name,
            middle_name: form.middle_name,
            passport: form.passport
        });
    } catch (error) {
        throw error;
    }
};

export { registerRequest };