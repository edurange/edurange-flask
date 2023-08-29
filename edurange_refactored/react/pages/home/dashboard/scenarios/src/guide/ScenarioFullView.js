import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';

import '../../../src/Dashboard.css'
import './Guide_fullView.css';

import { useContext } from 'react';
import { HomeRouterContext } from '../../../../src/Home_router';
import { ScenariosRouterContext } from '../Scenarios_router';
import { nanoid } from 'nanoid';
import { scenarioShells } from '../../../../../../modules/shells/scenarioType_shells';
import buildGuide from '../modules/buildGuide';

// UNDER HEAVY CONSTRUCTION

function ScenarioFullView() {

  const { scenarioID, pageID } = useParams(); // from URL parameters
  const { userData_state } = useContext(HomeRouterContext);
  const {
    guideBook_state, set_guideBook_state,
    guideContent_state, set_guideContent_state,
    scenarioList_state, set_scenarioList_state,
    scenarioPage_state, set_scenarioPage_state,
  } = useContext(ScenariosRouterContext);

  const meta = guideContent_state.scenario_meta;

  useEffect(() => {
    async function beginGuideBuild() {
      try {
        const contentReturn = await axios.get(`api/get_content/${scenarioID}`);
        const contentData = contentReturn.data;
        console.log(contentData)
        const guideReturn = buildGuide(contentData.contentJSON);
        set_guideContent_state(contentData);
        set_guideBook_state(guideReturn);
      } catch (error) {
        console.error('Error fetching data:', error);
      };
    };
    beginGuideBuild();
  }, [scenarioID]);


  // present empty / deflect while promises await
  if ((guideBook_state.length < 1) || (!meta)) {
    return (<>Scenario not found</>);
  }

  const SSH_IP = guideContent_state.SSH_IP[`${meta.scenario_name}_attacker`]
  const shellData = scenarioShells[`${meta.scenario_description}`];

  return (
    <>
      <div className='dashcard-fullview-frame'>
        <div className='dashcard-fullview-frame-carpet'>

          <div className="dashcard-fullview-left-frame">

            <section className='dashcard-fullview-placard-row'>
              <span className='dashcard-fullview-placard-title' >{meta.scenario_name}</span>
            </section>

            <section className='dashcard-fullview-splash-row'>

              <div className='dashcard-fullview-splash-image-section'>
                <div className='dashcard-fullview-splash-image' >
                  <img src={shellData.icon} />
                </div>
              </div>

              <div className='dashcard-fullview-splash-blurb-frame' >
                <div className='dashcard-fullview-splash-blurb-text'>
                  {shellData.description_short} <br />
                </div>
              </div>

            </section>

            <section className='dashcard-fullview-left-lower-section'>

              <section className='dashcard-fullview-left-mid-frame'>


                <div className='dashcard-fullview-left-lower-item'>
                  Keywords: {shellData.keywords.join(', ')}
                </div>

                <div className='dashcard-fullview-left-lower-item'>
                  Students: Mario, Toad, Bowser, DK
                </div>

                <div className='dashcard-fullview-left-lower-item'>
                  Student Groups: 2, 4
                </div>

                <div className='dashcard-fullview-left-lower-item'>
                  Scenario Groups: 1
                </div>

                <div className='dashcard-fullview-left-lower-item'>
                  <br />
                  Resources:
                  <br />
                  - Frequently Asked Questions (FAQ)
                  <br />
                  - Link to Resource
                  <br />
                  - Link to Resource
                  <br />
                  - Link to Resource
                </div>
              </section>
            </section>


          </div>

          <div className='dashcard-fullview-guide-frame'>
            <div className='dashcard-fullview-guide-main'>
              <div className='dashcard-fullview-controlbar-frame'>
                <div className='dashcard-fullview-controlbar-tabs-frame'>
                  <div className='dashcard-fullview-controlbar-tab dashcard-tab-left dashcard-tab-active'>Home</div>
                  {/* <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Brief</div> */}
                  {guideBook_state.map((val, key) => {
                    return (
                      <Link to={`/edurange3/dashboard/scenarios/${scenarioID}/${key + 1}`} key={nanoid(5)}>
                        <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>
                          Chpt.{key + 1}
                          {/* <div id='newdash-sidebar-icon'>{val.icon}</div>
                        <div id='newdash-sidebar-title'>{val.title}</div> */}
                        </div>
                      </Link>
                    );
                  })}
                  <div className='dashcard-fullview-controlbar-tab dashcard-tab-right dashcard-tab-inactive'>Chpt.10</div>
                </div>

              </div>
              <article className='dashcard-fullview-guide-main-text'>
                {guideBook_state[pageID - 1]}
              </article>
            </div>
            <div className='dashcard-fullview-guide-footcontrol-frame'>
              <div className='dashcard-fullview-footcontrol-item footcontrol-ssh-text'>
                <div>
                  SSH: {SSH_IP}
                </div>
                <div>
                  user: {guideContent_state.credentialsJSON.username} pass: {guideContent_state.credentialsJSON.password}
                </div>
              </div>
              <div className='dashcard-fullview-footcontrol-item footcontrol-web-ssh-button'>Web-SSH</div>
              <div className='dashcard-fullview-footcontrol-item footcontrol-chat-button'>Chat</div>
            </div>

          </div>
        </div>
      </div>
    </>
  );
};

export default ScenarioFullView;


