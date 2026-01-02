import axios from 'axios';

class StartDataService {
    getStartMessage() {
        return axios.get('http://localhost:8000/api/home/');
    }
}

export default new StartDataService();