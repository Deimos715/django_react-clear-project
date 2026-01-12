import { NavLink } from 'react-router-dom';

export default function PasswordResetSent() {
    return (
        <div className="container">
            <div className="recoveryPassword">
                <h1>Письмо отправлено</h1>

                <p style={{ marginTop: 12 }}>
                    Если такой email существует, мы отправили письмо со ссылкой для восстановления пароля.
                    Проверьте входящие и папку «Спам».
                </p>

                <div style={{ marginTop: 20 }}>
                    <NavLink to="/login/">Вернуться ко входу</NavLink>
                </div>
            </div>
        </div>
    );
}