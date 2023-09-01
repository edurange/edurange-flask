
// import React, { useState, useEffect, useContext } from 'react';
// import GuideQuestion from './GuideQuestion';
// import GuideReading from './GuideReading';
// import axios from 'axios';
// import { HomeRouterContext } from '../../../../src/Home_router';
// import { useParams } from 'react-router-dom';
// import { ScenariosRouterContext } from '../Scenarios_router';
// import buildGuide from './tempHelpers/buildGuide';
// import ScenarioChat from '../../chat/src/ScenarioChat';
// import ScenarioFullView from './ScenarioFullView';

// export const GuideContext = React.createContext();
// function Guide_controller(props) {

//     const { scenarioID, pageID } = useParams(); // from URL parameters
//     // const [ content_state, set_content_state] = useState({});


//     const { userData_state, login_state } = useContext(HomeRouterContext);

//     const { set_guide_state, set_content_state } = useContext(ScenariosRouterContext);


//     useEffect(() => {
//         async function beginGuideBuild() {
//             try {
//                 const contentReturn = await axios.get(`api/get_content/${scenarioID}`);
//                 const contentJSON = contentReturn.data.contentJSON;
//                 // console.log('contentJSON before guideReturn: ',contentJSON);
//                 const guideReturn = buildGuide(contentJSON);
//                 // console.log("guideReturn: ",guideReturn)
//                 set_content_state(contentJSON);
//                 set_guide_state(guideReturn);
//             } catch (error) {
//                 console.error('Error fetching data:', error);
//             };
//         };
//         beginGuideBuild();
//     }, [scenarioID]);
    

//     // console.log(guide_state)
//     return (    
//             <ScenarioFullView/> 
//         );
// }

// export default Guide_controller;

 