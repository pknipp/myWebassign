import React, { useState, useContext, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import AuthContext from '../auth'
import Question from './Question';


const Questions = () => {
    const { fetchWithCSRF, currentUser } = useContext(AuthContext);
    const [, setErrors] = useState([]);
    const [, setMessages] = useState([]);
    const [questions, setQuestions] = useState([]);
    const [showMoreQuestions, setShowMoreQuestions] = useState(false);

    useEffect(() => {
        (async () => {
            const response = await fetchWithCSRF(`/api/questions`);
            const responseData = await response.json();
            if (!response.ok) return setErrors(responseData.errors);
            if (responseData.messages) return setMessages(responseData.messages);
            setQuestions(responseData.questions);
        })();
    }, [])

    return (
        <>
            <h3>Questions authored by me:</h3>
            <NavLink exact to={"/questions/0"} className="nav" activeClassName="active">
                create new question
            </NavLink>
            <ul>
                {questions.filter(question => question.owner.id === currentUser.id).map(question => {
                    return <li><Question key={question.id} question={question} /></li>
                })}
            </ul>
            <span>
                <button onClick={() => setShowMoreQuestions(!showMoreQuestions)}>
                    {showMoreQuestions ? "Hide " : "Show "}
                </button>
                <span padding-left={"10px"}> questions authored by other instructors.</span>
            </span>
            {!showMoreQuestions ? null :
                <>
                    <h3>Other's questions:</h3>
                    <ul>
                        {questions.filter(question => question.owner.id !== currentUser.id).map(question => {
                            return <li><Question key={question.id} question={question} /></li>
                        })}
                    </ul>
                </>
            }
        </>
    )
};

export default Questions;
