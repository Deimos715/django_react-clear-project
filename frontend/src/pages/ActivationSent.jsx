import { useNavigate } from "react-router-dom";

const ActivationSent = () => {
    const navigate = useNavigate();

    return (
        <div className="container">
            <h1>Подтвердите email</h1>
            <p>
                Мы отправили письмо для подтверждения на ваш email. Перейдите по
                ссылке из письма, чтобы активировать личный кабинет.
            </p>

            <button onClick={() => navigate("/login/")}>Перейти к входу</button>
        </div>
    );
};

export default ActivationSent;
