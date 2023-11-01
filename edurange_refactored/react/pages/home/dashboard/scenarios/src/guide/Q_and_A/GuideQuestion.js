
import React, {useState}  from 'react';
import { nanoid } from 'nanoid';
import './Q_and_A.css'
import SubmitButton from './SubmitButton';

function GuideQuestion ( {
    // itemContentType,
    // itemContentPointer,
    // chapterNumber,
    // itemIndexInChapter,
    scenario_id,
    question_num,
    itemContent } ) {





    return (
    <div className='edu3-question-frame' key={nanoid(3)}>
        <div className='edu-question-carpet'>

            <div className='edu3-question-text-row'>
                {itemContent.Text}
            </div>

            <div className='edu3-response-row'>

                <div className='edu3-response-row-left'>
                    
                    <div className='edu3-response-row-left-content'>
                        <label className='edu3-response-row-left-content-text' htmlFor='question'>Response:</label>
                        <input className='edu3-response-row-left-content-field' type='text' id='question' name='question' />
                    </div>
                </div>

                <div className='edu3-response-row-right'>
                    
                    <SubmitButton scenario_id={1} question_num={1} />


                </div>

            </div>
        </div>
    </div>
    );
};

export default GuideQuestion;
