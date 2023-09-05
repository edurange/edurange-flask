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
import SSH_web from '../../../src/components/ssh/SSH_web';
import Guide_infoFrame from './Guide_infoFrame';

// UNDER HEAVY CONSTRUCTION

function ScenarioFullView() {

  const { scenarioID, pageID } = useParams(); // from URL parameters
  const { userData_state } = useContext(HomeRouterContext);
  const {
    guideBook_state, set_guideBook_state,
    guideContent_state, set_guideContent_state,
  } = useContext(ScenariosRouterContext);

  const [ leftPane_state, set_leftPane_state ] = useState(0)

  const meta = guideContent_state.scenario_meta;

  useEffect(() => {
    async function beginGuideBuild() {
      try {
        const contentReturn = await axios.get(`api/get_content/${scenarioID}`);
        const contentData = contentReturn.data;
        const guideReturn = buildGuide(contentData.contentJSON);
        set_guideContent_state(contentData);
        set_guideBook_state(guideReturn);
      } catch (error) {
        console.error('Error fetching data:', error);
      };
    };
    beginGuideBuild();
  }, [scenarioID]);

  function launchWebSSH(SSH_address, user, pass) {

    const url = `http://10.0.0.55:1337/ssh/host/${SSH_address}`;
    window.open(url, '_blank');

  }

//// GUARD /////
if ((guideBook_state.length < 1) || (!meta)) { return (<>Scenario not found</>); }
//// GUARD /////

  const SSH_username = guideContent_state.credentialsJSON.username;
  const SSH_password = guideContent_state.credentialsJSON.password;

  const SSH_IP = guideContent_state.SSH_IP[`${meta.scenario_name}_nat`]
  const shellData = scenarioShells[`${meta.scenario_description}`];

  const tabActiveClass = 'dashcard-fullview-controlbar-tab dashcard-tab-active'
  const tabInactiveClass = 'dashcard-fullview-controlbar-tab dashcard-tab-inactive'

  const infoPane = (
  <Guide_infoFrame 
    guideBook={guideBook_state} 
    guideContent={guideContent_state} />)

  const sshPane = (
  <SSH_web 
    SSH_address={SSH_IP}
    SSH_username={SSH_username}
    SSH_password={SSH_password} />)

  return (
    <>
      <div className='dashcard-fullview-frame'>
        <div className='dashcard-fullview-frame-carpet'>

          <div className="dashcard-fullview-left-frame">

          {(leftPane_state===1) ? sshPane : infoPane }

          </div>

          <div className='dashcard-fullview-guide-frame'>
            <div className='dashcard-fullview-guide-main'>
              <div className='dashcard-fullview-controlbar-frame'>
                <div className='dashcard-fullview-controlbar-tabs-frame'>

                    <div className={`dashcard-tab-left ${pageID === "0" ? tabActiveClass : tabInactiveClass}`}>
                      <Link to={`/edurange3/dashboard/scenarios/${scenarioID}/0`}>
                          Brief
                      </Link>
                    </div>

                    {guideBook_state.map((val, key) => {
                      return (
                        <div key={key} className={`dashcard-tab-middles ${pageID === (key+1).toString() ? tabActiveClass : tabInactiveClass}`}>
                            <Link to={`/edurange3/dashboard/scenarios/${scenarioID}/${key + 1}`} key={nanoid(5)}>
                                Chpt.{key + 1}
                            </Link>
                          </div>
                      );
                    })}

                    <div className={`dashcard-tab-right ${pageID === "1337" ? tabActiveClass : tabInactiveClass}`}>
                      <Link to={`/edurange3/dashboard/scenarios/${scenarioID}/1337`}>
                          Debrief
                      </Link>
                    </div>
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
                  user: {SSH_username} pass: {SSH_password}
                </div>
              </div>
              <div className='dashcard-fullview-footcontrol-item footcontrol-info-button' onClick={() => set_leftPane_state(0)}>Info</div>
              <div className='dashcard-fullview-footcontrol-item footcontrol-pseudo-ssh-button' onClick={() => set_leftPane_state(1)} >edu3-SSH</div>
              <div className='dashcard-fullview-footcontrol-item footcontrol-web-ssh-button' onClick={() => launchWebSSH( SSH_IP, SSH_username, SSH_password ) }>Web-SSH</div>
              <div className='dashcard-fullview-footcontrol-item footcontrol-chat-button'>Chat</div>
            </div>

          </div>
        </div>
      </div>
    </>
  );
};

export default ScenarioFullView;


