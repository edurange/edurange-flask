import React from 'react';
import { scenarioShells } from '../../../../../../../modules/shells/scenarioType_shells';
import Resources_card from './Resources_card';
import SSH_card from './SSH_card';
import './InfoPane.css';

function InfoPane({ guideContent }) {

  const meta = guideContent.scenario_meta;
  
  if ((!meta)) { return (<>Scenario not found</>); } // GUARD

  const shellData = scenarioShells[`${meta.scenario_description}`];

  return (
    <section className='er3-infopane-frame'>

      <section className='er3-infopane-splash-frame'>

        <section className='er3-infopane-placard-row'>
          <span className='er3-infopane-placard-title' >{meta.scenario_name}</span>
        </section>

        <section className='er3-infopane-splash-row'>
          <div className='er3-infopane-splash-image-section'>
            <div className='er3-infopane-splash-image' >
              <img src={shellData.icon} />
            </div>
          </div>
          <div className='er3-infopane-splash-blurb-frame' >
            <div className='er3-infopane-splash-blurb-text'>
              {shellData.description_short}
            </div>
          </div>
        </section>

        <section className='er3-infopane-keywords-row'>
          <div className='er3-infopane-keywords-item'>
            Keywords: {shellData.keywords.join(', ')}
          </div>
        </section>

      </section>

      <section className='er3-infopane-lower-section'>
        <Resources_card guideContent={guideContent} />
        <SSH_card guideContent={guideContent} />
      </section>

    </section>
  );
};
export default InfoPane;


