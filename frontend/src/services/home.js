import api from './api';

class StartDataService {
    getStartMessage() {
        return api.get('/home/');
    }
}

export default new StartDataService();