

import React from 'react';
import { Link } from 'react-router-dom';

import '../../../src/Dashboard.css'
import './Guide_fullView.css';
import { scenarioShells } from '../../../../../../modules/shells/scenarioType_shells';

// UNDER HEAVY CONSTRUCTION

function Guide_infoFrame({guideBook, guideContent}) {

    const meta = guideContent.scenario_meta;

    // GUARD
    if ((guideBook.length < 1) || (!meta)) { return (<>Scenario not found</>); }
    // GUARD

    const SSH_IP = guideContent.SSH_IP[`${meta.scenario_name}_nat`]
    const shellData = scenarioShells[`${meta.scenario_description}`];
    
    return (
        <>
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
                        
                        <br/>
                        Resources:
                        <br/>
                        <Link to="/edurange3/info/FAQ">- Frequently Asked Questions (FAQ)</Link>
                        {shellData.resources.map((val, key) => {
                            return (
                                <div key={key}>
                                    <a href={val.link} target="_blank" rel="noopener noreferrer">
                                        - {val.label}
                                    </a>
                                </div>
                            );
                        })}
                        <br></br>

                        <button className='dashcard-fullview-left-lower-item'>
                            GET HINT
                        </button>
                        <br></br>
                        <button className='dashcard-fullview-left-lower-item'>
                            REQUEST HELP
                        </button>

                    </div>

                </section>
            </section>
        </>
    );
};

export default Guide_infoFrame;


