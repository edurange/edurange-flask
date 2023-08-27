import axios from 'axios';
import React, {useState, useEffect} from 'react';
import { useParams } from 'react-router-dom';

import '../../../../src/Dashboard.css'
import './CardFullView.css';

import { useContext } from 'react';

import GuideInterpreter from './GuideInterpreter';
import GuideHome from './GuideHome';
import { HomeRouterContext } from '../../../../src/Home_router';

// import FetchHelper from '../../../../../../../modules/utils/fetchHelper'



// UNDER HEAVY CONSTRUCTION




const GenericPageData = "this is generic page data"
const fakePages = [
  1, 2, 3, 4, 5, 6, 7, 8, 9
];
const fakeTabs = [ "Home", "Brief", ...fakePages.map(num => `Chpt.${num}`)];









function ScenarioFullView() {




  const { userData_state } = useContext(HomeRouterContext); //ok
  
  const { scenarioID, pageID } = useParams();
  console.log(`Received params for instance ${scenarioID} and pageID ${pageID}`); //ok





  if (!scenarioID) { return (<>Scenario not found</>); };
 




  async function get_guide(scenarioID) {
    fetchedGuide = await axios.get(`/api/get_guide/${scenarioID}`);
  };


// scenario 'type' to get shell data
// scenario instance data
// student's answers
// ssh info
// other instance-specific info (randomized values, etc)
// 



  // const scenarioInstanceData = instructorData_state.scenarios.find((scenarioInstanceData) => scenarioInstanceData.uid === uid); // returns data specific to this scenario instance, but not this user
  // if (!scenarioInstanceData) { return (<>Scenario not found</>) };
  
  // const scenarioShellData = scenarioShells[`${scenarioInstanceData.description}`]; // returns generic data for the scenario type (e.g. Getting_Started), things like: title, keywords, splash image, resources, etc.






  return (
    <>
    {/* <ScenarioGuideContext.Provider value={{ */}
      
      
    {/* }}> */}
    <div className='dashcard-fullview-frame'>
      <div className='dashcard-fullview-frame-carpet'>

        <div className="dashcard-fullview-left-frame">

          <section className='dashcard-fullview-placard-row'>
              <span className='dashcard-fullview-placard-title' >"description"</span>
              {/* <span className='dashcard-fullview-placard-title' >"{scenarioInstanceData.description}"</span> */}
              {/* <span className='dashcard-fullview-placard-subtitle'>Instance UID:{scenarioInstanceData.uid}</span> */}
          </section>

          <section className='dashcard-fullview-splash-row'>

            <div className='dashcard-fullview-splash-image-section'>
              <div className='dashcard-fullview-splash-image' >
                {/* <img src={scenarioShellData.icon} /> */}icon
              </div>
            </div>

            <div className='dashcard-fullview-splash-blurb-frame' >
              <div className='dashcard-fullview-splash-blurb-text'>
                {/* {scenarioShellData.description_short} <br /> */} short description
              </div>
            </div>

          </section>

          <section className='dashcard-fullview-left-lower-section'>

            <section className='dashcard-fullview-left-mid-frame'>

              
              <div className='dashcard-fullview-left-lower-item'>
                {/* Keywords: {scenarioShellData.keywords.join(', ')} */} keywords
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
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Brief</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.1</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.2</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.3</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.4</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.5</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.6</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.7</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.8</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-inactive'>Chpt.9</div>
                <div className='dashcard-fullview-controlbar-tab dashcard-tab-right dashcard-tab-inactive'>Chpt.10</div>
              </div>

            </div>
            <article className='dashcard-fullview-guide-main-text'>
              {/* {scenarioShellData.description_long} */} long
              {/* <GuideInterpreter/> */}
              {/* < ScenComp/> */}
              {/* <scenarioShellData.tutorial/> */}
              {/* <MyLorey />  */}
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
    {/* </ScenarioGuideContext.Provider> */}
    </>
  );
};

export default ScenarioFullView;


