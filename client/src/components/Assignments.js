import React, { useState, useContext, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import AuthContext from '../auth'
import Assignment from './Assignment';

const Assignments = () => {
    const { fetchWithCSRF, currentUser } = useContext(AuthContext);
    const [, setErrors] = useState([]);
    const [, setMessages] = useState([]);
    const [assignments, setAssignments] = useState([]);
    const [showMoreAssignments, setShowMoreAssignments] = useState(false);

    const getAssignments = async () => {
        const response = await fetchWithCSRF("/api/assignments");
        const data = await response.json();
        setErrors(data.errors || []);
        setMessages(data.messages || []);
        setAssignments(data.assignments || []);
    };

    useEffect(() => {
        getAssignments();
    }, []);

    return (
        <>
            <h3>My assignments:</h3>
            <NavLink exact to={"/assignments/0"} className="nav" activeClassName="active">
                create new assignment
            </NavLink>
            <ul>
                {assignments.filter(assignment => assignment.owner.id === currentUser.id)
                    .map(assignment => (
                        <Assignment key={`aid${assignment.id}`} assignment={assignment}/>
                    ))
                }
            </ul>
            <span>
                <button onClick={() => setShowMoreAssignments(!showMoreAssignments)}>
                    {showMoreAssignments ? "Hide " : "Show "}
                </button>
                <span padding-left={"10px"}>
                    assignments owned by other instructors.
                </span>
            </span>
            {!showMoreAssignments ? null :
                <>
                    <h3>Other's assignments:</h3>
                    <ul>
                        {assignments.filter(assignment => assignment.owner.id !== currentUser.id)
                            .map(assignment => (
                                <li>
                                    <Assignment key={assignment.id} assignment={assignment}/>
                                </li>
                            ))
                        }
                    </ul>
                </>
            }
        </>
    )
};

export default Assignments;
