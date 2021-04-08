![NetAssign](question_editor.png)



# Contents

[schema](https://drawsql.app/appacademy-2/diagrams/net-assign)

[Heroku deployment](https://net-assign.herokuapp.com)

[Introduction](#introduction)

[Instructor/student dichotomy](#instructor/student-dichotomy)

[Question Editor](#question-editor)

[CRUD](#crud)

[Duplication of resources]()
CRUD + Duplicate (POST w/included ID#)

[Gradebook]() IN PROGRESS

# Introduction

[return to "Contents"](#contents)

[go to next section ("Instructor/student dichotomy")](#instructor/student-dichotomy)

My project (NetAssign) is a clone of [WebAssign](http://www.webassign.net), a leader in the delivery, administration, and automated grading of online assignments to students in high school and college.  This industry sector has revolutionized the manner in which classroom assignments are implemented this century.  My clone uses JavaScript and React (with functional components, hooks, and context) for the front-end, and it uses Flask, Python, SQLAlchemy, and PostgreSQL for the back-end.

# Instructor/Student dichotomy

[return to "Contents"](#contents)

[return to previous section](#introduction)

[go to next section ("Question editor")](#question-editor)

This app has two different types of users (instructors and students), with considerably different capabilities and UX.  In the Users table of database these types are distinguished simply by the boolean value in the <tt>isInstructor</tt> column.  An instructor have full CRUD-control for each of the seven other tables in the db, whereas a student has no access to the Questions table and has complete access only to the row(s) of the Users, Enrollments, and Submissions tables for which either the primary or foreign key coincides with that of the student.  The initial <tt>Welcome</tt> component invites the unregistered visitor to self-designate as a <tt>userType</tt> which is either <tt>instructor</tt> or <tt>student</tt> by selecting the appropriate <tt>NavLink</tt>.
(NOTE: in progress is a method for a sysadmin to monitor/approve instructor-designation after the signup phase.)

from the <tt>NavBar</tt> component:
```
const userTypes = ["instructor", "student"];
const UserTypes = userTypes.map(userType => userType[0].toUpperCase() + userType.slice(1));
// ... and later ...
const noUserType = (
    <>
        {UserTypes.map(UserType => (
            <NavLink exact to={`/welcome${UserType}`}>
                {`${UserType}s`}
            </NavLink>
        ))}
    </>
);
// ... and later ...
return (
    <div className="nav-container">
        {head}
        <div>
            {!userType ? noUserType : // ...
        </div>
    </div>
)
```
This selection passes through these three children of the the <tt>Switch</tt> element in the <tt>App</tt> component in order to update the value of <tt>props.userType</tt>:
```
<AuthRoute exact path="/welcome" component={Welcome} />
<AuthRoute exact path="/welcomeInstructor" userType={"instructor"} component={Welcome} />
<AuthRoute exact path="/welcomeStudent" userType={"student"} component={Welcome} />
```
The updated props in the <tt>Welcome</tt> component causes the display of the value of the appropriate property of the <tt>welcome</tt> POJO, thereby displaying more specialized "welcome" information:
```
const Welcome = props => {
  const { userType, setUserType } = useContext(AuthContext);
  setUserType(props.userType);
  return (
    <div className="info text">
    // "welcome" POJO has two properties: "instructor" and "student"
        {welcome[props.userType] || general}
      </div>
  );
}
```
This designation then guides the unregistered user to sign-up as the appropriate type of user via different versions of the NavBar:

more from <tt>NavBar</tt> component:
```
const i = userTypes.indexOf(userType);
const yesUserType = (
    <>
        <NavLink to={`/login${UserTypes[i]}`} className="nav" activeClassName="active">
            Login In
        </NavLink>
        <NavLink to={`signup${UserTypes[i]}`} className="nav" activeClassName="active">
            Sign Up
        </NavLink>
        <NavLink to={`/welcome${UserTypes[(i + 1) % 2]}`} className="nav">
            Switch to {`Switch to ${UserTypes[(i + 1) % 2]} Side`}
        </NavLink>
    </>
)
/// ... and later, with more details than before:
return (
    <div className="nav-container">
        {head}
        <div>
            {!userType ? noUserType : !currentUser ? yesUserType : // ...
        </div>
    </div>
)
```
After logging in or signing up, the user is then provided access to non-<tt>Auth</tt> routes.  From this point onward in the user experience, three different mechanisms prevent students from accessing resoures to which they are not authorized, the first two in the front-end and the third one in the back.

(1) <tt>Route</tt> wrappers:
```
const ProtectedInstructorRoute = ({ component: Component, path, exact }) => {
    const { currentUser } = useContext(AuthContext)
    return (
        <Route
            path={path}
            exact={exact}
            render={props => (currentUser && currentUser.is_instructor)
                    ? <Component currentUser={currentUser} />
                    : <Redirect to="/login" />
            }
        />
    )
}
```
(2) conditional rendering of buttons and other resources:

The following code from the <tt>Enrollments</tt> component allows a student to drop a course but additionally allows an instructor both to edit the course details and to see the course's roster.  (For obvious reasons this code also prevents an instructor from withdrawing from the course.)
```
{currentUser.is_instructor ?
    <>
        <NavLink to={`/courses/edit/${course.course.id}`}>
            edit
        </NavLink>
        <NavLink to={`/roster/${course.course.id}`}>
            roster
        </NavLink>
    </>
:
    <button onClick={e => deleteEnrollment(e, currentUser.id, course.id)}>
        Drop
    </button>
}
```

(3) conditional early returns from back-end:

The following lines are from the back-end route <tt>deployments.py</tt>.
```
instructor_id = Course.query.get(course_id).instructor_id
if not instructor_id == current_user.id:
    return {"errors": ["You are not authorized to this."]}, 401
```

# Question editor

[return to "Contents"](#contents)

[return to previous section ("Instructor/student dichotomy")](#instructor/student-dichotomy)

[go to next section ("CRUD")](#crud)

NetAssign presently allows for two different categories of questions: "numerical" and "fill in the blank".  (The latter includes "true-false".)  Both question categories involve the use of a simple input element:
```
<input
    type="text"
    placeholder="Response"
    value={response}
    onChange={e => setResponse(e.target.value)}
/>
```
The two question-types differ in terms of how the student-response is handled (ie "graded") in the back-end.  Below are the relevant lines from <tt>submissions.py</tt>, the back-end route for student submissions (ie, responses to questions):
```
tolerance = 0.02
    # five lines omitted for the sake of brevity
    if request.method == 'PUT':
        # ten lines omitted for brevity
        grade = None  # declared in an outer scope
        if response != None:
            if isinstance(answer, str): # fill-in-the-blank question
                grade = (answer == response)
            else: # numerical question
                grade=abs(answer-float(response))<=tolerance*abs(answer) or abs(answer-float(response))<tolerance
```
As indicated above, the data-type of the answer (key) is a string for fill-in-the-blank but is a number for a numerical question.  A response to a fill-in-the-blank question is marked correct if and only if the student response exactly matches the answer.  However a response to a numerical question is marked correct either if the student's reponse is within 2% of the answer or is within 0.02 of the answer.

One of the most powerful features of NetAssign is its ability to randomize questions and their answers.  This feature assures instructors that their students not simply copying answers from each other.  Accordingly the <tt>Questions</tt> table of of the database does not simply contain one column with a simple string for the question and another column with a simple string (or number) for the correct answer.  Instead there are three separate columns: <tt>question_code</tt>, <tt>inputs</tt>, and <tt>answer_code</tt>.  I'll now discuss these sequentially.
1. <tt>question_code</tt>:

This is a string with both regular text and zero or more instances of brace-pairs, each containing a string with the name of a variable which'll be randomized in a manner specified by the contents of the <tt>inputs</tt> column.  Below are three examples of this, taken from the seeder data in <tt>database.py</tt>
```
"T or F: {animal} have four legs."
"{factor1} times {factor2} equals ... "
"What is the {power}th power of the {ordinal}th prime number?"
```
2. <tt>inputs</tt>:

Each of these is a <tt>JSON.stringify</tt>-ed multi-dimensional array, the dimension for which is either three or two depending upon the nature of the randomization.  Consider the following example, which corresponds to the last of the three examples above, and which involves both types of randomization:
```
[['power', 4, 7, 3], [['ordinal', 4, 5, 6, 7], ['prime', 7, 11, 13, 17]]]
```
The outer array contains two elements, corresponding to the fact that there are two different randomizations which must be performed.  Let's consider these one element at a time.  The first element consists of a flat array:
```
['power', 4, 7, 3]
```
This signifies that the variable <tt>power</tt> should randomly receive 3 + 1 = 4 different values which are spread evenly between a minimum value of 4 and a maximum value of 7.  Hence, <tt>power</tt> should be randomly chosen from the set {4, 5, 6, 7} (using notation from mathematics, not JavaScript).

Next consider the second element in <tt>inputs</tt>, which consists of a two-dimensional array. This signifies that there are two or more variables, which must be chosen in a correlated manner.
```
[['ordinal', 4, 5, 6, 7], ['prime', 7, 11, 13, 17]]
```
This contains two sub-subarrays each of length *N* + 1, where *N* is the number of different randomized values that these variables should assume.  The zeroth element of each sub-subarray is the name of the particular variable, and the remaining *N* elements (which themselves need *not* be numbers) are the values that the particular variable may assume.  Note that these randomizations occur in a correlated manner.  For instance, if <tt>ordinal</tt> equals 5, then <tt>prime</tt> equals 11.  (ie, the 5th prime number is 11.)

In this particular example there is exactly one instance of the first type of randomization and one instance of the second type of randomization, but there can be any combination of the different types of randomizations.

3. <tt>answer_code</tt>:

This is a string.  For a fill-in-the-blank question this simply corresponds to the answer.  For a numerical question, however, this string is a mathematical/algebraic/trigonometric expression which provides the answer.  The syntax used is both intuitive and powerful.  It probably includes the names of your variables (not enclosed with braces), parentheses, and operators such as +, -, *, /, and/or ^ (for exponentiation).
Click <a href="http://www.partow.net/programming/exprtk">
www.partow.net/programming/exprtk</a> for more details.  For the second and third examples given at the top of this section, what follows are the respective strings for the <tt>answer_code</tt>:
```
"factor1 * factor2"
 "prime^power"
 ```

# CRUD

[return to "Contents"](#contents)

[return to previous section ("Question editor")](#question-editor)

The database has four joins tables: Enrollments (which joins Users and Courses), Appearances (joins Assignments and Questions), Deployments (Assignments and Courses), and Submissions (Deployments and Users).  The respective CRUD-functionalities for these four
enrollments (users, courses), appearances (questions, assignments), deployments (courses, assignments, but can be multiple), submissions (deployments, users)

Table | Du | C | R | U | D | Joins?
------| ---- | --| - | - | - | -
Users | N    | Y | Y | Y | Y | N
Questions| Y | Y | Y | Y | Y | N
