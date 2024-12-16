import axios from "axios";

async function login(username, password) {
    try {
        const response = await axios.post('http://localhost:5000/login', {
            email: username,
            password: password,
        });

        const token = response.data.token;
        if (token) {
            localStorage.setItem('token', token);
            return 201;
        }
        return response.data;
    } catch (error) {
        if (error.response) {
            return { status: error.response.status, message: error.response.data.error };
        } else if (error.request) {
            return { status: null, message: "Проверьте соединение с сеть." };
        } else {
            return { status: null, message: "Ошибка на строне сервера. Попробуйте позднее." };
        }
    }
}

export default login;