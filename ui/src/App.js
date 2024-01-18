// [RUN WITH] npm start
/* pre prvog pokretanja u terminalu uneti 
npm install react-scripts --save
npm install react-router-dom
npm install axios
*/

//TODO: css za sve page-ve i prikaz proizvoda na Home page-u
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Login } from './Components/Login';
import { Register } from './Components/Register';
import { Home } from './Components/Home';
import { AddProduct } from './Components/AddProduct';
import { EditProfile } from './Components/EditProfile';
import { TransactionHistory } from './Components/TransactionHistory';
import { Card } from './Components/Card';
import { Account } from './Components/Account';
import { Balance } from './Components/Balance';
import { AddBalance } from './Components/AddBalance'


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/addProduct" element={<AddProduct />} />
        <Route path="/editProfile" element={<EditProfile />} />
        <Route path="/transactionHistory" element={<TransactionHistory />} />
        <Route path="/card" element={<Card />} />
        <Route path="/account" element={<Account />} />
        <Route path="/balance" element={<Balance />} />
        <Route path='/addBalance' element={<AddBalance />} />
      </Routes>
    </Router>
  )
}

export default App
