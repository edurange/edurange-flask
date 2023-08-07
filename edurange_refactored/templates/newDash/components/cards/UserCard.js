
import React, {useContext, useState} from 'react';
import * as cardHelper from './cardHelper';
import { MainFrameContext } from '../../../main_frame/MainFrame';


const UserCard = ({ instructorDataIndex, categoryIndex, tertiaryIndex }) => {
    
    const { session_instructorData_state } = useContext(MainFrameContext);
    


    return (
      <div className='card'>
        <div className='card-title'>{formatTitle(title)}</div>
        <div className='card-content'>{content}</div>
      </div>
    );
  };
  