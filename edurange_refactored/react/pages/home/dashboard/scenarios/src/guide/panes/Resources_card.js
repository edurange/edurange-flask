

import React from 'react';
import { scenarioShells } from '../../../../../../../modules/shells/scenarioType_shells';
import { Link } from 'react-router-dom';
import { nanoid } from 'nanoid';
import './Resources_card.css';

function Resources_card({ guideContent }) {

    const meta = guideContent.scenario_meta;

    // GUARD
    if ((!meta)) { return (<>Scenario not found</>); }
    // GUARD

    const shellData = scenarioShells[`${meta.scenario_description}`];

    return (
        <section className='resources-frame'>
            <div className='resources-placard'>Resources</div>
            <div className='resources-items-container'>

                <Link to="/edurange3/info/FAQ">
                    <div className='resource-item' key={nanoid(2)}>-
                        <div className='resource-link'>

                            Frequently Asked Questions (FAQ)
                        </div>
                    </div>
                </Link>
                {shellData.resources.map((val, key) => {
                    return (
                        <a key={key} href={val.link} target="_blank" rel="noopener noreferrer">
                            <div className='resource-item' >-
                                <div className='resource-link' >
                                    {val.label}
                                </div>
                            </div>
                        </a>
                    )
                })}
            </div>
        </section>
    );
};

export default Resources_card;

