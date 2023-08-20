
import React, {useState, useEffect} from 'react';
import { useParams } from 'react-router-dom';

import '../../../../src/Dashboard.css'
import './CardFullView.css';

import { useContext } from 'react';
import { scenarioShells } from '../../../../../../../modules/scenarios/ScenariosData';

import GuideInterpreter from './GuideInterpreter';
import GuideHome from './GuideHome';
import { HomeRouterContext } from '../../../../../src/Home_router';

import {fetchData} from '../../../../../../../modules/utils/fetchHelper'

export const ScenarioGuideContext = React.createContext();

const GenericPageData = "this is generic page data"

const fakePages = [
  1, 2, 3, 4, 5, 6, 7, 8, 9
]
const fakeTabs = [ "Home", "Brief", ...fakePages.map(num => `Chpt.${num}`)];

function ScenarioFullView() {
  
  const { uid, pageID } = useParams();
  console.log(`Received params for instance ${uid} and pageID ${pageID}`)


  if (!uid) { return (<>Scenario not found</>) }

  // Retrieve from localStorage and parse it
  const recalledPageString = localStorage.getItem('guidePage');
  const recalledPage = recalledPageString ? JSON.parse(recalledPageString) : {
    uid: uid,
    pageID: pageID
  };

  console.log('2')
  
  const chosenPage = recalledPage.pageID || "home";
  console.log("PAGE CHOSEN:",chosenPage)
  
  // Save to localStorage in a stringified format
  if (chosenPage) { 
    localStorage.setItem('guidePage', JSON.stringify({
      uid: uid,
      pageID: chosenPage
    }));
  }

//--------------------------

  async function getGuide(){
    const fetchedPage = await fetchData('POST',"get_guide", {page: chosenPage}) 
    console.log("fetched page response", fetchedPage.message)
  }
  
  const currentPageData = (chosenPage !== "home") ?  getGuide() : GuideHome
    

  console.log(currentPageData)
  // const [guidePage_state, set_guidePage_state] = ({
  //   uid: uid,
  //   pageID: chosenPage,
  // })
  
  console.log('4')

  // const [guide_pageNumber_state, set_guide_pageNumber_state] = useState(0);  // home is 'home'. briefing then starts at 0 and chapter 1 is page 1 (in the content json)
  useEffect(() => {
    // set_guide_uid_state(Number(uid));
    // set_guidePage_state(Number(pageID) || "home");
    localStorage.setItem('guidePage', JSON.stringify({
      uid: uid,
      pageID: pageID}
    ));
  }, [pageID]);
  


  const { instructorData_state , userData_state } = useContext(HomeRouterContext);
  if (!instructorData_state.scenarios) { return (<>Scenario not found</>) };
  
  const scenarioInstanceData = instructorData_state.scenarios.find((scenarioInstanceData) => scenarioInstanceData.uid === uid); // returns data specific to this scenario instance, but not this user
  if (!scenarioInstanceData) { return (<>Scenario not found</>) };
  
  const scenarioShellData = scenarioShells[`${scenarioInstanceData.description}`] // returns generic data for the scenario type (e.g. Getting_Started), things like: title, keywords, splash image, resources, etc.

  // const userScenarioInstanceData = fetchData("get_scenario", {userID: userData_state.id}); // for prod - data specific to this user for this specific scenario instance
  // const userScenarioInstanceData = fetchData("POST","get_scenario", {userID: 2}); // for dev (will always get user 2's data for the specific scenario instance)




  return (
    <>
    <ScenarioGuideContext.Provider value={{
      
      // guide_pageNumber_state
      
    }}>
    <div className='dashcard-fullview-frame'>
      <div className='dashcard-fullview-frame-carpet'>

        <div className="dashcard-fullview-left-frame">

          <section className='dashcard-fullview-placard-row'>
              <span className='dashcard-fullview-placard-title' >"{scenarioInstanceData.description}"</span>
              {/* <span className='dashcard-fullview-placard-subtitle'>Instance UID:{scenarioInstanceData.uid}</span> */}
          </section>

          <section className='dashcard-fullview-splash-row'>

            <div className='dashcard-fullview-splash-image-section'>
              <div className='dashcard-fullview-splash-image' >
                <img src={scenarioShellData.icon} />
              </div>
            </div>

            <div className='dashcard-fullview-splash-blurb-frame' >
              <div className='dashcard-fullview-splash-blurb-text'>
                {scenarioShellData.description_short} <br />
              </div>
            </div>

          </section>

          <section className='dashcard-fullview-left-lower-section'>

            <section className='dashcard-fullview-left-mid-frame'>

              
              <div className='dashcard-fullview-left-lower-item'>
                Keywords: {scenarioShellData.keywords.join(', ')}
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
              {scenarioShellData.description_long}
              <GuideInterpreter/>
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
    </ScenarioGuideContext.Provider>
    </>
  );
};

export default ScenarioFullView;


