import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useContext } from 'react';
import { HomeRouterContext } from '../../../../src/Home_router';
import { ScenariosRouterContext } from '../Scenarios_router';
import InfoPane from './panes/InfoPane';
import GuidePane from './panes/GuidePane';
import FootControls from './controls/FootControls';
import SSH_web from './ssh/SSH_web';

import '../../../src/Dashboard.css';
import './Scenario_controller.css';

function Scenario_controller() {
  
  const { scenarioID, pageID } = useParams(); // from URL parameters
  const { userData_state } = useContext(HomeRouterContext);
  const { guideContent_state, set_guideContent_state } = useContext(ScenariosRouterContext);

  const [leftPaneName_state, set_leftPaneName_state] = useState("info");
  const [rightPaneName_state, set_rightPaneName_state] = useState("guide");
  const meta = guideContent_state.scenario_meta;

  const [sliderNum_state, set_SliderNum_state] = useState(45); // pane size ratio, bigger num = bigger left side
  const leftWidth = `${sliderNum_state}%`;
  const rightWidth = `${100-sliderNum_state}%`;
  const rightOffset = `${sliderNum_state}%`;

  function handleSliderChange (event) {
    set_SliderNum_state(event.target.value);
};

  useEffect(() => {
    async function getContent() {
      try {
        const contentReturn = await axios.get(`api/get_content/${scenarioID}`);
        const contentData = contentReturn.data;
        set_guideContent_state(contentData);
      } catch (error) {
        console.error('Error fetching data:', error);
      };
    };
    getContent();
  }, [scenarioID]);

  if ((!meta)) { return (<>Scenario not found</>); }; // GUARD

  const SSH_username = guideContent_state.credentialsJSON.username;
  const SSH_password = guideContent_state.credentialsJSON.password;
  const scenarioName_raw = meta.scenario_name;
  const scenarioName_sani = scenarioName_raw.split('_').join('');

  const SSH_IP = guideContent_state.SSH_IP[`${scenarioName_sani}_nat`];

  const panes = {
    info : (
      <InfoPane
        guideContent={guideContent_state}
      />
    ),  
    ssh : (
      <SSH_web
        SSH_address={SSH_IP}
        SSH_username={SSH_username}
        SSH_password={SSH_password} 
      />
    ), 
    guide : (
      <GuidePane
        guideContent={guideContent_state}
      />
    )
  };
  const leftPaneToShow = panes[leftPaneName_state];
  const rightPaneToShow = panes[rightPaneName_state];

  return (
    <>
    <div className='scenario-paneSlider-frame'>
                    <input className='scenario-paneSlider' type="range" min="0" max="100" value={sliderNum_state} onChange={handleSliderChange} />
    </div>
      <div className='scenario-frame'>
        <div className='scenario-frame-carpet'>
          <div className="scenario-leftpane-frame" style={{ minWidth: leftWidth, maxWidth: leftWidth }}>
            {leftPaneToShow}
            <FootControls 
              guideContent={guideContent_state} 
              updatePane={set_leftPaneName_state}
              paneSide={"left"}
            />
          </div>

          <div className='scenario-rightpane-frame' style={{ minWidth: rightWidth, maxWidth: rightWidth, left: rightOffset }}>
            {rightPaneToShow}
            <FootControls  
              guideContent={guideContent_state} 
              updatePane={set_rightPaneName_state}
              paneSide={"right"}
            />
          </div>
        </div>
      </div>
    </>
  );
};
export default Scenario_controller;


