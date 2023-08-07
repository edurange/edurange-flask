
import React, {useContext, useState} from 'react';
import * as cardHelper from './cardHelper';
import { MainFrameContext } from '../../../main_frame/MainFrame';


// dataCategoryIndex determines whether it is a user, scenario, etc
// dateItemIndex determines which of the category's items to select
// secondaryIndex is just there in case we need it

const CategoryCard = ({ categoryIndex, secondaryIndex }) => {
    
    const { session_instructorData_state } = useContext(MainFrameContext);
    


    return (
      <div className='card'>
        <div className='card-title'>{formatTitle(title)}</div>
        <div className='card-content'>{content}</div>
      </div>
    );
  };
  