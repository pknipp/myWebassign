import React, { useContext } from 'react';
import AuthContext from '../auth'

const LogOut = () => {
    const { fetchWithCSRF, setCurrentUser, setUserType } = useContext(AuthContext);
    const deleteSession = async e => {
        e.preventDefault();
        const response = await fetchWithCSRF('/api/session', {method: 'DELETE'});
        if (response.ok) {
            setCurrentUser(null);
            setUserType(null);
        }
    };

    return (
        <form onSubmit={deleteSession}>
            <button type="submit">Logout</button>
        </form>
    );
};
export default LogOut;
