
import { nanoid } from 'nanoid';
import React from 'react';
import { edurange_icons } from '../../ui/edurangeIcons';


export async function fetchScenarioList() {
    try {
        const response = await axios.get("/api/get_scenarios");
        if (response.data.scenarioTable) {
            return response.data.scenarioTable;
        };
    }
    catch (error) { console.log('get_scenarios_list error:', error); };
};


export async function getScenarioMeta(scenario_id) {
    try {
        const response = await axios.get("/api/get_scenario_meta");
        if (response.data.meta) {
            return response.data.meta;
        };
    }
    catch (error) { console.log('get_scenarios_meta error:', error); };
};


export function reactify_question({
    itemContentType,
    itemContentPointer,
    chapterNumber,
    itemIndexInChapter,
    itemContent }) {

    const handleSubmit = event => {
        event.preventDefault();
        const usernameInput = event.target.elements.username.value;
        const passwordInput = event.target.elements.password.value;
        sendLoginRequest(usernameInput, passwordInput);
    };

    return (
        <div key={nanoid(3)}>

            <br></br>
            {itemContent.Text}
            <br></br>
            <div className='edu3-login-submit-frame' onSubmit={handleSubmit}>

                <div key={nanoid(3)} className='edu3-login-submit-row'>

                    <div className='edu3-login-submit-item'>
                        <label className='edu3-login-prompt-text' htmlFor='question'>Response:</label>
                        <input className='edu3-login-input-text' type='text' id='question' name='question' />
                    </div>
                </div>

                <div className='edu3-login-submit-row-right'>
                    <button className='edu3-login-button' type='submit'>
                        {edurange_icons.eye_icon}
                    </button>
                </div>

            </div>
            <br></br>
        </div>
    );
};


export function reactify_reading({
    itemContentType,
    itemContentPointer,
    chapterNumber,
    itemIndexInChapter,
    itemContent }) {

    return (
        <div key={nanoid(5)}>
            <br></br>
            <div dangerouslySetInnerHTML={{ __html: itemContent }} />
            <br></br>
        </div>
    );
};

