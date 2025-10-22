import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App.jsx';
import Header from './components/Header.jsx';
import Footer from './components/Footer.jsx';
import './scss/styles.scss';

createRoot(document.getElementById('root')).render(
    <BrowserRouter > {/* Оборачиваем всё в BrowserRouter это оболочка для внутренних переходов */}
        <Header />
            <App />
        <Footer />
    </BrowserRouter>
);

