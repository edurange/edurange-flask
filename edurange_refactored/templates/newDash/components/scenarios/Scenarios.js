import React from 'react';
import ScenariosTable from './ScenariosTable';
// import pointing_finger from '../../../../../assets/img/card_img/pointing_hand.svg';
import '../main/NewDash.css'
import ScenarioCard from './ScenarioCard';
import { nanoid } from 'nanoid';
import elf from '../../../../../assets/img/card_img/elf.svg';
import fingerprint from '../../../../../assets/img/card_img/fingerprint.svg';
import getting_started from '../../../../../assets/img/card_img/getting_started.svg';
import kick from '../../../../../assets/img/card_img/kick.svg';
import survivalist from '../../../../../assets/img/card_img/survivalist.svg';
import telephoneWoman from '../../../../../assets/img/card_img/telephoneWoman.svg';
import turtle from '../../../../../assets/img/card_img/turtle.svg';
import twoHeads from '../../../../../assets/img/card_img/twoHeads.svg';
import wrangler from '../../../../../assets/img/card_img/wrangler.svg';



function Scenarios () {
    


    return (
        <>

                <div className='newdash-content-placard' >Scenarios</div>
                <ScenariosTable/>
                <ScenarioCard/>
        </>
    );
};

export default Scenarios;
