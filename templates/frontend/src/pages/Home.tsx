import React from 'react';
import AppointmentList from '../components/AppointmentList';

const Home: React.FC = () => {
    return (
        <div>
            <h1>Welcome to the Healthcare System</h1>
            <p>Manage your appointments efficiently.</p>
            <AppointmentList />
        </div>
    );
};

export default Home;