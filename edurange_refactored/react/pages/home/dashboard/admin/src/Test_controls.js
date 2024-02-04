import React from 'react';


function Test_controls () {

    
    testScenario = {
        unique_name: 'getStart123',
        generic_name: 'Getting_Started',
        scenario_id: 1,
        groups: [1,2]
    }
    
    scenarioList = [testScenario]
    
    test_user = {
        username: 'buddy',
        group: [1,2],
        role: 'student',
        email: '',
    }

    const [navName_state, set_navName_state] = useState('logout');
    const [clipboard_state, set_clipboard_state] = useState('');
    const [sideNav_isVisible_state, set_sideNav_isVisible_state] = useState(true);
    const [sideNav_isSmall_state, set_sideNav_isSmall_state] = useState(false);
    const [userData_state, set_userData_state] = useState({});
    const [login_state, set_login_state] = useState(false);

    return (
        <>

        </>
    );
}

export default Test_controls;