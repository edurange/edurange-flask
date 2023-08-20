
import React from 'react';
import { useParams } from 'react-router-dom';

// import ScenariosListView from './ScenariosListView';
// import elf from '../../../../../assets/img/card_img/elf.svg';
// import fingerprint from '../../../../../assets/img/card_img/fingerprint.svg';
// import getting_started_icon from '../../../../../assets/img/card_img/getting_started.svg';
// import kick from '../../../../../assets/img/card_img/kick.svg';
// import survivalist from '../../../../../assets/img/card_img/survivalist.svg';
// import maze from '../../../../../assets/img/card_img/maze.svg';
// import wrangler from '../../../../../assets/img/card_img/wrangler.svg';
// import alchemy from '../../../../../assets/img/card_img/alchemy.svg';
import twoHeads from '../../../../../assets/img/card_img/twoHeads.svg';

import '../main/NewDash.css';
import '../main/cards.css';

import MyLorey from '../../../main_frame/components/temp/MyLorey';
import { MainFrameContext } from '../../../main_frame/MainFrame';
import { useContext } from 'react';
import { nanoid } from 'nanoid';
import {scenarioShells} from './ScenariosData_disable'

function ScenarioCardDetail () {

    const { uid } = useParams();
    if (!uid){return(<>Scenario not found</>)}
    const {session_instructorData_state} = useContext( MainFrameContext );
    if (!session_instructorData_state.scenarios){return(<>Scenario not found</>)};
    const cardData = session_instructorData_state.scenarios.find((cardData) => cardData.uid === uid);
    
    const thisScenarioData = scenarioShells[`${cardData.name}`]


    return (
        <div className='newdash-itemcard-frame'>
            <div className='newdash-itemcard-frame-carpet'>

            
            <div className="newdash-itemcard-left-frame">
            
                <section className='newdash-itemcard-left-upper-frame'>

                    <div className='newdash-itemcard-left-upper-image-section'>
                                <div className='newdash-itemcard-left-upper-image' >
                                    <img src={thisScenarioData.icon}/>
                                </div>
                    </div>

                        <div className='newdash-itemcard-left-upper-meta-frame' >
                            <div className='newdash-itemcard-left-upper-meta-item'>
                                Title: {cardData.name}
                            </div>
                            <div className='newdash-itemcard-left-upper-meta-item'>
                                Instance ID: {cardData.uid};
                            </div>
                            <div className='newdash-itemcard-left-upper-meta-item'>
                                Difficulty: Easy
                            </div>
                            <div className='newdash-itemcard-left-upper-meta-item'>
                                Keywords: {thisScenarioData.keywords.join(', ')}
                            </div>
                        </div>

                    
                </section>
                
                <section className='newdash-itemcard-left-lower-frame'>
                    
                    <div className='newdash-itemcard-left-lower-item'>
                        Students: Mario, Toad, Bowser, DK
                    <div className='newdash-itemcard-left-lower-item'>
                        Description: {thisScenarioData.description_short}
                    </div>
                    </div>
                    <div className='newdash-itemcard-left-lower-item'>
                        Student Groups: 2, 4
                    </div>
                    <div className='newdash-itemcard-left-lower-item'>
                        Scenario Groups: 1
                    </div>
                </section>

            </div>
            <section className='newdash-itemcard-right-upper-frame'>
                <div className='newdash-itemcard-right-upper-ssh-frame'>

                <div>SSH IP: 123.456.123.456</div>
                <div>SSH PORT: 1234</div>
                <div>SSH USERNAME: example</div>
                <div>SSH PASSWORD: passExample</div>
                </div>
                <div className='newdash-itemcard-right-upper-buttons-frame'>

                <button>COPY SSH TO CLIPBOARD</button>
                <button>LAUNCH WEB-SSH</button>
                <button>GO TO QUESTIONS</button>
                </div>

            </section>
            <div className='newdash-itemcard-description-frame'>
                <div className='newdash-itemcard-description-main'>
                <article className='newdash-itemcard-description-main-text'>
                    <br></br>
                    Our functionality here.
                    <br></br>
                    <br></br>
                    Chat could go here perhaps?
                    <br></br>
                    <br></br>
                    Or just some documentation for the scenario...
                    <br></br>
                    <br></br>
                    <MyLorey/>
                </article>
                </div>
                <div className='newdash-itemcard-description-footer'></div>
            </div>

               
            </div>
            this is {uid}
        </div>
    );
};

export default ScenarioCardDetail;


