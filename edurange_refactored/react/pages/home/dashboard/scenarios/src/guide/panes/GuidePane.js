import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { nanoid } from 'nanoid';
import buildGuide from '../../modules/utils/buildGuide';
import HomeChapter from '../Q_and_A/HomeChapter';
import './GuidePane.css';

function GuidePane({ guideContent, set_leftPane_state }) {

  const { scenarioID, pageID } = useParams(); // from URL parameters
  const [guideBook_state, set_guideBook_state] = useState([])

  const meta = guideContent.scenario_meta;

  useEffect(() => {
    async function beginGuideBuild() {
      try {
        const guideReturn = buildGuide(scenarioID, guideContent.contentJSON);
        set_guideBook_state(guideReturn);
      } catch (error) {
        console.error('Error fetching data:', error);
      };
    };
    beginGuideBuild();
  }, []);

  if ((guideBook_state.length < 1) || (!meta)) { return (<>Scenario not found</>); } // GUARD

  const tabActiveClass = 'guidepane-controlbar-tab guidepane-tab-active';
  const tabInactiveClass = 'guidepane-controlbar-tab guidepane-tab-inactive';

  const chapterToShow = () => {
    if (Number(pageID) === 0){ return <HomeChapter/>; }
    else if (Number(pageID) === 1337){ return <HomeChapter/>; }
    else { return guideBook_state[Number(pageID) - 1]; }
  };

  return (
    <>
      <div className='guidepane-guide-frame'>
        <div className='guidepane-guide-main'>

          <div className='guidepane-controlbar-frame'>
            <div className='guidepane-controlbar-tabs-frame'>

              <Link
                to={`/edurange3/dashboard/scenarios/${scenarioID}/0`}
                className={`guidepane-tab-left ${pageID === "0" ? tabActiveClass : tabInactiveClass}`}>
                <div >
                  Brief
                </div>
              </Link>

              {guideBook_state.map((val, key) => {
                return (
                  <Link
                    to={`/edurange3/dashboard/scenarios/${scenarioID}/${key + 1}`} key={nanoid(5)}
                    className={`guidepane-tab-middles ${pageID === (key + 1).toString() ? tabActiveClass : tabInactiveClass}`}>
                    <div key={key} >
                      Chpt.{key + 1}
                    </div>
                  </Link>
                );
              })}

              <Link
                to={`/edurange3/dashboard/scenarios/${scenarioID}/1337`}
                className={`guidepane-tab-right ${pageID === "1337" ? tabActiveClass : tabInactiveClass}`}>
                <div >
                  Debrief
                </div>
              </Link>

            </div>
          </div>

          <article className='guidepane-guide-text'>
            {chapterToShow()}
          </article>

        </div>
      </div>
    </>
  );
};

export default GuidePane;