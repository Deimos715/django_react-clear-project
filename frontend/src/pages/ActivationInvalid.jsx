// frontend/src/pages/ActivationInvalid.jsx
import { useNavigate } from "react-router-dom";

const ActivationInvalid = () => {
    const navigate = useNavigate();

    return (
        <>
            <h1>Ссылка недействительна</h1>
            <p>
                Возможно, срок действия ссылки истёк или она уже использована.
            </p>

            <div style={{ display: "flex", gap: 12 }}>
                <button onClick={() => navigate("/login/")}>Войти</button>
                <button onClick={() => navigate("/home/")}>На главную</button>
            </div>
        </>
    );
};

export default ActivationInvalid;
