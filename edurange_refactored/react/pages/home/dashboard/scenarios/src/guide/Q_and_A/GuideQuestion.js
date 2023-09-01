
import React  from 'react';
import { nanoid } from 'nanoid';
import './Q_and_A.css'

function GuideQuestion ( {
    itemContentType,
    itemContentPointer,
    chapterNumber,
    itemIndexInChapter,
    itemContent } ) {

    const q_points =  itemContent.Answers.Points;
    const q_value =  itemContent.Answers.Value;
    const q_options =  itemContent.Options; 
    const q_text =  itemContent.Text;
    const q_type =  itemContent.Type;
    

    const handleSubmit = event => {
        event.preventDefault();
        const usernameInput = event.target.elements.username.value;
        const passwordInput = event.target.elements.password.value;
        sendLoginRequest(usernameInput, passwordInput);
    };


    return (
    <div className='edu3-question-frame' key={nanoid(3)}>
        <div className='edu-question-carpet'>

            <div className='edu3-question-text-row'>
                {itemContent.Text}
            </div>

            <div className='edu3-response-row' onSubmit={handleSubmit}>

                <div className='edu3-response-row-left'>
                    
                    <div className='edu3-response-row-left-content'>
                        <label className='edu3-response-row-left-content-text' htmlFor='question'>Response:</label>
                        <input className='edu3-response-row-left-content-field' type='text' id='question' name='question' />
                    </div>
                </div>

                <div className='edu3-response-row-right'>
                    <button className='edu3-response-row-right-button' type='submit'>
                        CHECK
                    </button>
                </div>

            </div>
        </div>
    </div>
    );
};

export default GuideQuestion;
