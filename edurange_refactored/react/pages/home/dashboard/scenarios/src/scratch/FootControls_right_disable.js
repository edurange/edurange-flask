


import React from 'react';
import { scenarioShells } from '../../../../../../modules/shells/scenarioType_shells';
import './FootControls.css';

// UNDER HEAVY CONSTRUCTION

function FootControls_right({ guideContent, set_leftPane_state, paneSide }) {

  const meta = guideContent.scenario_meta;

  // GUARD
  if ((!meta)) { return (<>Scenario not found</>); }
  // GUARD

  const SSH_IP = guideContent.SSH_IP[`${meta.scenario_name}_nat`]
  const shellData = scenarioShells[`${meta.scenario_description}`];

  const frameClass = `${paneSide}-footcontrol-frame`
  console.log(frameClass)

  return (
      <div className={frameClass}>

        <div
          className='footcontrol-item footcontrol-info-button'
          onClick={() => set_leftPane_state(0)}>
          Help
        </div>
        <div
          className='footcontrol-item footcontrol-pseudo-ssh-button'
          onClick={() => set_leftPane_state(1)}>
          Stats
        </div>

        <div className='footcontrol-item footcontrol-chat-button'>
          Progess
        </div>

        <div className='footcontrol-item footcontrol-ssh-text'>
          <div> Scenario Progress:  </div>
          <div> Points: 123 / Max: 456 </div>
        </div>
      </div>
  );
};

export default FootControls_right;

