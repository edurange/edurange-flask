
import React from 'react';
import ScenariosTable from './ScenariosTable';
import elf from '../../../../../assets/img/card_img/elf.svg';
import fingerprint from '../../../../../assets/img/card_img/fingerprint.svg';
import getting_started from '../../../../../assets/img/card_img/getting_started.svg';
import kick from '../../../../../assets/img/card_img/kick.svg';
import survivalist from '../../../../../assets/img/card_img/survivalist.svg';
import maze from '../../../../../assets/img/card_img/maze.svg';
import twoHeads from '../../../../../assets/img/card_img/twoHeads.svg';
import wrangler from '../../../../../assets/img/card_img/wrangler.svg';
import alchemy from '../../../../../assets/img/card_img/alchemy.svg';
import '../main/NewDash.css';
import '../main/cards.css';
import MyLorey from '../../../main_frame/components/temp/MyLorey';


import { MainFrameContext } from '../../../main_frame/MainFrame';
import { useContext } from 'react';

import { ScenarioShell } from '../../../../scripts/routing/loginHelper';
import { nanoid } from 'nanoid';

function ScenarioCard (inputScenario) {

    const fakeData = {
        uid: nanoid(5),
        title: "hello",
        keywords: ["letsaGo", "mamaMia","okiDoki", "waaaaaahhhh"]
    }

    const {session_instructorData_state} = useContext( MainFrameContext );

    if (!session_instructorData_state.scenarios){return <></>}
    const currentScenario = session_instructorData_state.scenarios[1];
    
    

    return (
        <div className='newdash-itemcard-frame'>
            <div className='newdash-itemcard-frame-carpet'>

            
            <div className="newdash-itemcard-placard-frame">
            
                <div className='newdash-itemcard-placard-image-section'>

                            <div className='newdash-itemcard-placard-image' >
                                <img src={maze}/>
                            </div>

                </div>
                <div className='newdash-itemcard-placard-meta-section'>

                    <div className='newdash-itemcard-placard-meta-frame' >
                        <div className='newdash-itemcard-placard-meta-item'>
                            Title: {currentScenario.name}
                        </div>
                        <div className='newdash-itemcard-placard-meta-item'>
                            Instance ID: {currentScenario.uid};
                        </div>
                        <div className='newdash-itemcard-placard-meta-item'>
                            Difficulty: Easy
                        </div>
                        <div className='newdash-itemcard-placard-meta-item'>
                            Keywords: {fakeData.keywords.join(', ')}
                        </div>
                    </div>

                </div>

            </div>
                    
            <div className='newdash-itemcard-content-frame'>
                <div className='newdash-itemcard-content-main'>
                <article className='newdash-itemcard-content-main-text'>
                    <MyLorey/>
                </article>
                </div>
                <div className='newdash-itemcard-content-footer'></div>
            </div>

               
            </div>
        </div>
    );
};

export default ScenarioCard;


