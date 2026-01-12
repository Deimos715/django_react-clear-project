import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "../services/auth";

export default function PasswordChange() {
    const navigate = useNavigate();

    const [oldPassword, setOldPassword] = useState("");
    const [newPassword1, setNewPassword1] = useState("");
    const [newPassword2, setNewPassword2] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const onSubmit = (e) => {
        e.preventDefault();
        setError("");

        if (!oldPassword || !newPassword1 || !newPassword2) {
            setError("Заполните все поля");
            return;
        }

        setLoading(true);

        AuthService.changePassword(oldPassword, newPassword1, newPassword2)
            .then(() => {
                navigate("/password/change/success/");
            })
            .catch((err) => {
                const data = err?.response?.data;

                // DRF-стиль ошибок: { field: [msg] } или строка
                if (data && typeof data === "object") {
                    const firstKey = Object.keys(data)[0];
                    const msg = Array.isArray(data[firstKey])
                        ? data[firstKey][0]
                        : data[firstKey];
                    setError(msg || "Ошибка смены пароля");
                } else {
                    setError("Ошибка смены пароля");
                }
            })
            .finally(() => {
                setLoading(false);
            });
    };

    return (
        <div className="container">
            <div className="recoveryPassword">
                <h1>Смена пароля</h1>

                {error && (
                    <div style={{ marginBottom: 16, color: "#c00" }}>
                        {error}
                    </div>
                )}

                <form className="w-50 mx-auto" onSubmit={onSubmit} noValidate>
                    <div
                        className="requiredFieldAndPassword"
                        style={{ width: "100%" }}
                    >
                        <input
                            type="password"
                            placeholder="Старый пароль"
                            value={oldPassword}
                            onChange={(e) => setOldPassword(e.target.value)}
                        />
                    </div>

                    <div
                        className="requiredFieldAndPassword"
                        style={{ width: "100%" }}
                    >
                        <input
                            type="password"
                            placeholder="Новый пароль"
                            value={newPassword1}
                            onChange={(e) => setNewPassword1(e.target.value)}
                        />
                    </div>

                    <div
                        className="requiredFieldAndPassword"
                        style={{ width: "100%" }}
                    >
                        <input
                            type="password"
                            placeholder="Повторите новый пароль"
                            value={newPassword2}
                            onChange={(e) => setNewPassword2(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        style={{ marginTop: 20 }}
                    >
                        {loading ? "Смена пароля…" : "Сменить пароль"}
                    </button>
                </form>
            </div>
        </div>
    );
}
