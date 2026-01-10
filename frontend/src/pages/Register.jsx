// frontend/src/pages/Register.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "../services/auth";

const Register = () => {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        email: "",
        first_name: "",
        last_name: "",
        middle_name: "",
        password: "",
        password2: "",
    });

    const [errors, setErrors] = useState({});
    const [submitting, setSubmitting] = useState(false);

    const onChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const setFieldError = (field, message) => {
        setErrors((prev) => ({ ...prev, [field]: message }));
    };

    const clearErrors = () => setErrors({});

    const normalizeApiErrors = (data) => {
        // DRF обычно возвращает {field: ["msg"]} или {detail: "..."} или строку
        if (!data) return { detail: "Ошибка регистрации." };

        if (typeof data === "string") return { detail: data };

        const out = {};
        for (const [key, value] of Object.entries(data)) {
            if (Array.isArray(value)) out[key] = value[0];
            else if (typeof value === "string") out[key] = value;
            else out[key] = "Ошибка.";
        }
        return out;
    };

    const onSubmit = (e) => {
        e.preventDefault();
        clearErrors();
        setSubmitting(true);

        AuthService.register({
            email: form.email,
            first_name: form.first_name,
            last_name: form.last_name,
            middle_name: form.middle_name,
            password: form.password,
            password2: form.password2,
        })
            .then(() => {
                navigate("/activation/sent/");
            })
            .catch((err) => {
                const data = err?.response?.data;
                const apiErrors = normalizeApiErrors(data);
                setErrors(apiErrors);
            })
            .finally(() => {
                setSubmitting(false);
            });
    };

    return (
        <div className="container">
            <h1>Регистрация</h1>

            {errors.detail && (
                <p style={{ color: "crimson" }}>{errors.detail}</p>
            )}

            <form
                onSubmit={onSubmit}
                style={{ display: "grid", gap: 12, maxWidth: 420 }}
            >
                <div>
                    <label>Email</label>
                    <input
                        name="email"
                        value={form.email}
                        onChange={onChange}
                    />
                    {errors.email && (
                        <div style={{ color: "crimson" }}>{errors.email}</div>
                    )}
                </div>

                <div>
                    <label>Фамилия</label>
                    <input
                        name="last_name"
                        value={form.last_name}
                        onChange={onChange}
                    />
                    {errors.last_name && (
                        <div style={{ color: "crimson" }}>
                            {errors.last_name}
                        </div>
                    )}
                </div>

                <div>
                    <label>Имя</label>
                    <input
                        name="first_name"
                        value={form.first_name}
                        onChange={onChange}
                    />
                    {errors.first_name && (
                        <div style={{ color: "crimson" }}>
                            {errors.first_name}
                        </div>
                    )}
                </div>

                <div>
                    <label>Отчество</label>
                    <input
                        name="middle_name"
                        value={form.middle_name}
                        onChange={onChange}
                    />
                    {errors.middle_name && (
                        <div style={{ color: "crimson" }}>
                            {errors.middle_name}
                        </div>
                    )}
                </div>

                <div>
                    <label>Пароль</label>
                    <input
                        type="password"
                        name="password"
                        value={form.password}
                        onChange={onChange}
                    />
                    {errors.password && (
                        <div style={{ color: "crimson" }}>
                            {errors.password}
                        </div>
                    )}
                </div>

                <div>
                    <label>Повтор пароля</label>
                    <input
                        type="password"
                        name="password2"
                        value={form.password2}
                        onChange={onChange}
                    />
                    {errors.password2 && (
                        <div style={{ color: "crimson" }}>
                            {errors.password2}
                        </div>
                    )}
                </div>

                <button type="submit" disabled={submitting}>
                    {submitting ? "Отправка..." : "Зарегистрироваться"}
                </button>
            </form>
        </div>
    );
};

export default Register;
