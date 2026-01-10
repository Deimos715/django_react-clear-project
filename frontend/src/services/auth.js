import api from './api';

class AuthService {
    login(email, password) {
        return api.post('/auth/login/', { email, password })
            .then((res) => {
                const access = res?.data?.access || '';
                if (!access) {
                    throw new Error('Не пришёл access');
                }
                this.setAccess(access);
                return res;
            });
    }

    refresh() {
        return api.post('/auth/refresh/', {})
            .then((res) => {
                const access = res?.data?.access || '';
                if (!access) {
                    throw new Error('Refresh не вернул access');
                }
                this.setAccess(access);
                return res;
            });
    }

    logout() {
        return api.post('/auth/logout/', {})
            .catch(() => {
                // даже если сервер упал — всё равно чистим access локально
            })
            .finally(() => {
                this.clearAccess();
            });
    }

    register(payload) {
        return api.post('/auth/register/', payload).then((response) => response.data);
    }

    setAccess(access) {
        localStorage.setItem('access', access);
    }

    getAccess() {
        return localStorage.getItem('access') || '';
    }

    clearAccess() {
        localStorage.removeItem('access');
    }

    isAuthenticated() {
        return !!this.getAccess();
    }

    getAuthHeader() {
        const access = this.getAccess();
        return access ? { Authorization: `Bearer ${access}` } : {};
    }

    /**
     * Опционально: единая точка для защищённых запросов без interceptors.
     * Делает запрос -> если 401 -> refresh -> повторяет запрос.
     */
    authorizedRequest(config) {
        const cfg = {
            ...config,
            headers: {
                ...(config.headers || {}),
                ...this.getAuthHeader(),
            },
        };

        return api(cfg).catch((err) => {
            if (!err?.response || err.response.status !== 401) {
                return Promise.reject(err);
            }

            return this.refresh()
                .then(() => {
                    const retryCfg = {
                        ...cfg,
                        headers: {
                            ...(cfg.headers || {}),
                            ...this.getAuthHeader(),
                        },
                    };
                    return api(retryCfg);
                })
                .catch((refreshErr) => {
                    this.clearAccess();
                    return Promise.reject(refreshErr);
                });
        });
    }
}

export default new AuthService();
