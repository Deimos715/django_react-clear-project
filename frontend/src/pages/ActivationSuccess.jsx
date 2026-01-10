import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "../services/auth";

const ActivationSuccess = () => {
    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [refreshed, setRefreshed] = useState(false);

    useEffect(() => {
        AuthService.refresh()
            .then(() => {
                setRefreshed(true);
            })
            .catch(() => {
                setError(
                    "Аккаунт активирован, но авто-вход не выполнен. Нажмите “Войти”."
                );
            })
            .finally(() => {
                setLoading(false);
            });
    }, [navigate]);

    return (
        <>
            <h1>Email подтверждён</h1>

            {loading && <p>Завершаем вход...</p>}

            {!loading && !error && (
                <>
                    <p>Готово. Можете перейти в личный кабинет.</p>
                    {refreshed && (
                        <button onClick={() => navigate("/account/")}>
                            В личный кабинет
                        </button>
                    )}
                </>
            )}

            {!loading && error && (
                <>
                    <p style={{ color: "crimson" }}>{error}</p>
                    <button onClick={() => navigate("/login/")}>Войти</button>
                </>
            )}
        </>
    );
};

export default ActivationSuccess;
