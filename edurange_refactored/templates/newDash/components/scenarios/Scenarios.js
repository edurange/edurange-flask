import React from 'react';
// import pointing_finger from '../../../../../assets/img/card_img/pointing_hand.svg';
import '../main/NewDash.css'
import { nanoid } from 'nanoid';

import ScenarioCardDetail from './ScenarioCardDetail';
import ScenariosListView from './ScenariosListView';
import ScenarioFullView from './ScenarioFullView';

function Scenarios () {
    return (<ScenariosListView/>);
};

export default Scenarios;
