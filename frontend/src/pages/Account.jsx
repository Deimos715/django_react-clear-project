import { useEffect, useState } from 'react';
import AuthService from '../services/auth';

const Account = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        AuthService.refresh()
            .catch(() => {
                setError("Сессия истекла. Войдите заново.");
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Загрузка...</p>;
    if (error) return <p style={{ color: "crimson" }}>{error}</p>;

    return (
        <div>
            <h1>Личный кабинет</h1>
            {/* твой контент */}
        </div>
    );
};

export default Account;
