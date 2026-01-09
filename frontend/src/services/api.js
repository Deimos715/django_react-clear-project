import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    withCredentials: true, // нужно, чтобы cookie refresh отправлялась при /auth/refresh/
});

export default api;