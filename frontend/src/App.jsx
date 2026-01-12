import { Routes, Route } from 'react-router-dom'; // Импортируем роутер
import Home from './pages/Home' // Импортируем роутер
import Login from './pages/Login'
import Account from './pages/Account'
import Taplink from './pages/Taplink'
import Help from './pages/Help'
import NotFound from './pages/NotFound'
import Register from './pages/Register';
import ActivationSuccess from './pages/ActivationSuccess';
import ActivationInvalid from './pages/ActivationInvalid';
import ActivationSent from './pages/ActivationSent';
import PasswordChange from './pages/PasswordChange';
import PasswordChangeSuccess from './pages/PasswordChangeSuccess';
import PasswordResetRequest from './pages/PasswordResetRequest';
import PasswordResetSent from './pages/PasswordResetSent';
import PasswordResetConfirm from './pages/PasswordResetConfirm';
import PasswordResetSuccess from './pages/PasswordResetSuccess';
import PasswordResetInvalid from './pages/PasswordResetInvalid';

const App = () => {
    return (
    <main>
        {/* Определяем маршруты */}
        {/* path - Передаём путь который будет остлеживать react-router || element передаём Название компонента изначально импортируя его выше */}
        <Routes> 
            <Route path='home/' element={<Home />} />
            <Route path='login/' element={<Login />} />
            <Route path='account/' element={<Account />} />
            <Route path='taplink/' element={<Taplink />} />
            <Route path='help/' element={<Help />} />
            <Route path='*' element={<NotFound />} />
            <Route path="register/" element={<Register />} />
            <Route path='activation/success/' element={<ActivationSuccess />} />
            <Route path='activation/invalid/' element={<ActivationInvalid />} />
            <Route path='activation/sent/' element={<ActivationSent />} />
            <Route path='password/change/' element={<PasswordChange />} />
            <Route path='password/change/success/' element={<PasswordChangeSuccess />} />
            <Route path="password/reset/" element={<PasswordResetRequest />} />
            <Route path="password/reset/sent/" element={<PasswordResetSent />} />
            <Route path="password/reset/confirm/:uidb64/:token/" element={<PasswordResetConfirm />} />
            <Route path="password/reset/success/" element={<PasswordResetSuccess />} />
            <Route path="password/reset/invalid/" element={<PasswordResetInvalid />} />
        </Routes>
    </main>
    );
};



export default App;
