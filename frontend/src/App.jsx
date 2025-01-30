import React, {Fragment} from 'react';
import Header from './components/Header';
import Footer from './components/Footer';

const App = () => {

  return (
    <Fragment>
        <Header />

        <section>
          Тело страницы
        </section>

        <Footer />
    </Fragment>
  )
}

export default App
