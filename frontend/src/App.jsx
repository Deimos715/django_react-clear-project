import { Routes, Route } from 'react-router-dom'; // Импортируем роутер
import Home from './pages/Home' // Импортируем роутер
import Login from './pages/Login'
import Account from './pages/Account'
import Taplink from './pages/Taplink'
import Help from './pages/Help'
import NotFound from './pages/NotFound'

const App = () => {
    return (
    <main>
        {/* Определяем маршруты */}
        {/* path - Передаём путь который будет остлеживать react-router || element передаём Название компонента изначально импортируя его выше */}
        <Routes> 
            <Route path='home' element={<Home />} />
            <Route path='login' element={<Login />} />
            <Route path='account' element={<Account />} />
            <Route path='taplink' element={<Taplink />} />
            <Route path='help' element={<Help />} />
            <Route path='*' element={<NotFound />} />
        </Routes>
    </main>
    );
};



export default App;