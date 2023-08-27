// import sample_content from "../../../../../../edurange-flask/scenarios/prod/getting_started/student_view/content.json";
import React, { useState } from 'react';
import {createRoot} from 'react-dom/client';

import GuideSection from "../guide-section/guide-section.component";
import TopicList from "../topic-list/topic-list.component";
import Chatbox from "../chatbox/chatbox.component";
import "./scenario.styles.css";
import fetchHelper from '../../../../react/api/common/fetchHelper';
import { HomeRouterContext } from '../../../../react/pages/home/src/Home_router';

function ScenComp (props) {
    // get content for this scenario

    const { csrfToken_state } = useContext(HomeRouterContext);

  
    const [scenState, set_scenState] = useState ({ 
        seenSection: 0,
        currentSection: 0,
        content: {},
        scenarioState: {},
    });
  

    function componentDidMount() {
    fetchHelper ('POST',`https://riparian.dev/edurange3/api/get_content/${scenState.scenarioId}`,{}, csrfToken_state)
      .then((resp) => resp.json())
      .then((json) => set_scenState({content: json}));

    fetchHelper ('POST',`https://riparian.dev/edurange3/api/get_state/${scenState.scenarioId}`,{}, csrfToken_state)
      .then((resp) => resp.json())
      .then((json) => set_scenState({scenarioState: json}));
  }

  function putAns(scenario_id, answer) {
    return null
    //TODO
  }
    if (Object.keys(scenState.content).length < 1) { return (<>NOPE</>) }
    
    const { Sections, Readings, Questions } = scenState.content.StudentGuide;
    return (
    <div className="student_view">
    <TopicList 
      currentSection={scenState.currentSection} 
      sections={Sections} 
      setState={p => {set_scenState(p)}}
    />
    <GuideSection 
      section={Sections[scenState.currentSection]} 
      readings={Readings} 
      questions={Questions} 
      scenarioState={scenState.scenarioState} 
      scenarioId={scenState.scenarioId} 
      csrf_token={scenState.csrf_token} 
    />
    <Chatbox 
      className='chatbox'
      uid={scenState.uid}
    />
      
  </div /* student-view */>           
    );
      
}
export default ScenComp;
// var e = document.getElementById('student_scenario');
// var root = createRoot(e);
// root.render(<StudentScenario scenarioId={e.attributes.scenario_id.value} uid={e.attributes.uid.value} />);
