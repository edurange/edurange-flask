


import React from 'react';
import { scenarioShells } from '../../../../../../modules/shells/scenarioType_shells';
import './FootControls.css';

// UNDER HEAVY CONSTRUCTION

function FootControls_left({ guideContent, set_leftPane_state }) {

  const meta = guideContent.scenario_meta;

  // GUARD
  if ((!meta)) { return (<>Scenario not found</>); }
  // GUARD

  const SSH_IP = guideContent.SSH_IP[`${meta.scenario_name}_nat`]
  const shellData = scenarioShells[`${meta.scenario_description}`];

  return (
      <div className='left-footcontrol-frame'>

        <div
          className='footcontrol-item footcontrol-info-button'
          onClick={() => set_leftPane_state(0)}>
          Info
        </div>
        <div
          className='footcontrol-item footcontrol-pseudo-ssh-button'
          onClick={() => set_leftPane_state(1)}>
          webSSH
        </div>

        <div className='footcontrol-item footcontrol-chat-button'>
          Chat
        </div>

        <div className='footcontrol-item footcontrol-ssh-text'>
          <div> SSH:  1234</div>
          <div> user: butt pass: head </div>
        </div>
      </div>
  );
};

export default FootControls_left;

