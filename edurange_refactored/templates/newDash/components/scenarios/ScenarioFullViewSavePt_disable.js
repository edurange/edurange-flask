
import React from 'react';
import { useParams } from 'react-router-dom';

import '../main/NewDash.css';
import './CardFullView.css';


import MyLorey from '../../../main_frame/components/temp/MyLorey';
import { MainFrameContext } from '../../../main_frame/MainFrame';
import { useContext } from 'react';
import { scenarioShells } from './ScenariosData'

function ScenarioFullView() {

  const { uid } = useParams();
  if (!uid) { return (<>Scenario not found</>) }
  const { session_instructorData_state } = useContext(MainFrameContext);
  if (!session_instructorData_state.scenarios) { return (<>Scenario not found</>) };
  const cardData = session_instructorData_state.scenarios.find((cardData) => cardData.uid === uid);

  const thisScenarioData = scenarioShells[`${cardData.description}`]


  return (
    <div className='dashcard-fullview-frame'>
      <div className='dashcard-fullview-frame-carpet'>

        <div className="dashcard-fullview-left-frame">

          <section className='dashcard-fullview-placard-row'>
              <span className='dashcard-fullview-placard-title' >"{cardData.description}"</span>
              <span className='dashcard-fullview-placard-subtitle'>Instance ID:{cardData.uid}</span>
          </section>

          <section className='dashcard-fullview-splash-row'>

            <div className='dashcard-fullview-splash-image-section'>
              <div className='dashcard-fullview-splash-image' >
                <img src={thisScenarioData.icon} />
              </div>
            </div>

            <div className='dashcard-fullview-splash-blurb-frame' >
              <div className='dashcard-fullview-splash-blurb-text'>
                {thisScenarioData.description_short} <br />
              </div>
            </div>

          </section>

          <section className='dashcard-fullview-left-lower-section'>

            <section className='dashcard-fullview-left-mid-frame'>

              
              <div className='dashcard-fullview-left-lower-item'>
                Keywords: {thisScenarioData.keywords.join(', ')}
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

                <div className='dashcard-fullview-controlbar-tab dashcard-tab-left dashcard-tab-active'>Intro</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.1</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.2</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.3</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.4</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.5</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-right dashcard-tab-inactive'>Chpt.6</div>
              </div>

            </div>
            <article className='dashcard-fullview-guide-main-text'>
              {thisScenarioData.description_long}
              <MyLorey /> 
            </article>
          </div>
          <div className='dashcard-fullview-guide-footcontrol-frame'>
            <div className='dashcard-fullview-footcontrol-item footcontrol-ssh-text'>
              <div>
                SSH: 123.456.789.012:1234
              </div>
              <div>
                user: 1337h4x0r pass: sh4d0wruN  [COPY]
              </div>
            </div>
            <div className='dashcard-fullview-footcontrol-item footcontrol-web-ssh-button'>Web-SSH</div>
            <div className='dashcard-fullview-footcontrol-item footcontrol-chat-button'>Chat</div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default ScenarioFullView;


