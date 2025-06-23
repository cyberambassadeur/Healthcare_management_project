import React from 'react';

interface Appointment {
    id: number;
    patient: string;
    doctor: string;
    start_time: string;
    end_time: string;
    status: string;
    reason: string;
}

interface AppointmentListProps {
    appointments: Appointment[];
    onAppointmentClick: (id: number) => void;
}

const AppointmentList: React.FC<AppointmentListProps> = ({ appointments, onAppointmentClick }) => {
    return (
        <div>
            <h2>Appointment List</h2>
            <ul>
                {appointments.map(appointment => (
                    <li key={appointment.id} onClick={() => onAppointmentClick(appointment.id)}>
                        <strong>{appointment.patient}</strong> with Dr. {appointment.doctor} 
                        <br />
                        {appointment.start_time} - {appointment.end_time} 
                        <br />
                        Status: {appointment.status} | Reason: {appointment.reason}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AppointmentList;