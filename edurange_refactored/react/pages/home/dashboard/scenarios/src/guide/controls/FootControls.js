


import React from 'react';
import { scenarioShells } from '../../../../../../../modules/shells/scenarioType_shells';
import './FootControls.css';
import edurange_icons from '../../../../../../../modules/ui/edurangeIcons';
import Copy_button from '../panes/Copy_button';
import Copy_button_small from '../panes/Copy_button_small';

const zws = `\u200B`;


// UNDER HEAVY CONSTRUCTION

function FootControls({ guideContent, updatePane, paneSide }) {

  const meta = guideContent.scenario_meta;

  // GUARD
  if ((!meta)) { return (<>Scenario not found</>); }
  // GUARD
  
  const SSH_key = `${guideContent.unique_scenario_name}_StartingLine`
  const SSH_IP = guideContent.SSH_IP
  const SSH_username = guideContent.credentialsJSON.username;
  const SSH_password = guideContent.credentialsJSON.password;
  const shellData = scenarioShells[`${meta.scenario_description}`];
  const [SSH_ip, SSH_port_str] = SSH_IP.split(':');

  const sshCommand = `ssh ${SSH_username}@${SSH_ip} -p ${SSH_port_str}`;

  const left_controls = (
    <>
      <div className='footcontrol-frame'>

        <div
          className='footcontrol-item footcontrol-info-button'
          onClick={() => updatePane("info")}>
          Info
        </div>

        <div
          className='footcontrol-item footcontrol-web-ssh-button'
          onClick={() => updatePane("ssh")}>
          web-SSH
        </div>

        <div className='footcontrol-item footcontrol-chat-button'>
          Chat
        </div>

        <section className='footcontrol-item footcontrol-sshinfo-frame'>

          <div className='footcontrol-ssh-label-frame'>
            <div className='footcontrol-ssh-label-text'>
              SSH
            </div>
          </div>

          <section className='footcontrol-ssh-creds-frame'>

            <section className='footcontrol-ssh-sublabel-frame'>
              <div className='footcontrol-ssh-sublabel-item'>
                cmd:
              </div>
              <div className='footcontrol-ssh-sublabel-item'>
                pw:
              </div>
            </section>

            <section className='footcontrol-ssh-creds-values-frame'>
              <div className='footcontrol-ssh-creds-values-row'>
                  <div className='footcontrol-ssh-creds-values-text'>  
                    ssh {SSH_username}{zws}@{SSH_ip} -p {SSH_port_str} 
                  </div>
              </div>
              <div className='footcontrol-ssh-creds-values-row'>
                  <div className='footcontrol-ssh-creds-values-text'>  
                    {SSH_password}
                  </div> 
              </div>
            </section >
         
          </section>

          <div className='footcontrol-ssh-copy-section'>
            <div className='footcontrol-ssh-buttons-column'>
                {<Copy_button_small thingToCopy = {sshCommand}/>}
                {<Copy_button_small thingToCopy = {SSH_password}/>}
            </div>
            <div className='footcontrol-ssh-copy-label'>
              COPY
            </div>  
          </div>


        </section>

      </div>
    </>
  );

  const right_controls = (
    <>
      <div className='footcontrol-frame'>

        <div
          className='footcontrol-item footcontrol-info-button'
          onClick={() => updatePane("guide")}>
          Guide
        </div>

        <div
          className='footcontrol-item footcontrol-web-ssh-button'
          onClick={() => updatePane("ssh")}>
          WebSSH
        </div>

        <div className='footcontrol-item footcontrol-chat-button'>
          Chat
        </div>

        <div className='footcontrol-item footcontrol-ssh-text'>
          <div> Scenario Progress:  </div>
          <div> Points: 123 / Max: 456 </div>
        </div>

      </div>
    </>
  );

  let controlsToUse;

  if (paneSide === 'left')        { controlsToUse = left_controls; }
  else if (paneSide === 'right')  { controlsToUse = right_controls; }
  else                            { controlsToUse = (<></>); };

  return controlsToUse;
};

export default FootControls;

