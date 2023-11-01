

import React,  {useState} from 'react';
import axios from 'axios';


// dataCategoryIndex determines whether it is a user, scenario, etc
// dateItemIndex determines which of the category's items to select
// secondaryIndex is just there in case we need it

function SubmitButton ({scenario_id, question_num}) {

    const [inputText, setInputText] = useState('');
    
    async function handleSubmit(){

        try{
            const pointsAwarded = await axios.post(('/api/check_response', {
                scenario_id: scenario_id,
                question_num: question_num,
                student_response: inputText
            })
            )
            // console.log(`Submission for scenario ${scenario_id} question ${question_num}: "${inputText}" was awarded ${pointsAwarded} points!`)


        } catch (err) { console.log(`Submission error: ${err}`); };

    }


    return (
        <div>
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter text"
        />
        <button onClick={handleSubmit}>CHECK</button>
      </div>
    );
  };
export default SubmitButton;