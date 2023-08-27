
import React, { useState, useEffect, useContext } from 'react';
import GuideQuestion from './GuideQuestion';
import GuideReading from './GuideReading';
import axios from 'axios';
import { HomeRouterContext } from '../../../../src/Home_router';
import { useParams } from 'react-router-dom';
import { ScenariosRouterContext } from '../Scenarios_router';
import buildGuide from './tempHelpers/buildGuide';

function Guide_controller(props) {

    const { scenarioID, pageID } = useParams(); // from URL parameters
    const [content_state, set_content_state] = useState({});
    const [guide_state, set_guide_state] = useState({});
    

    const {
        userData_state, login_state, 
        scenarioPage_state, set_scenarioPage_state
    } = useContext(HomeRouterContext);

    const { scenarioList_state 
    } = useContext(ScenariosRouterContext);


    useEffect(() => {
        async function beginGuideBuild() {
            try {
                const contentReturn = await axios.get(`api/get_content/${scenarioID}`);
                const contentJSON = contentReturn.data.contentJSON;
                console.log('contentJSON before guideReturn: ',contentJSON);
                const guideReturn = buildGuide(contentJSON);
                console.log("guideReturn: ",guideReturn)
                set_content_state(contentJSON);
                set_guide_state(guideReturn);
            } catch (error) {
                console.error('Error fetching data:', error);
            };
        };
        beginGuideBuild();
    }, [scenarioID]);
    

    // console.log(guide_state)
    return (<>Guide Controller Test Complete!</>);
}

export default Guide_controller;

 