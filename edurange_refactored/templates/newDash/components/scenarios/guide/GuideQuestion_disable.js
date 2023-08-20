
import React  from 'react';



function GuideQuestion ( props ) {

    const q_points =  props.questionData.Answers.Points;
    const q_value =  props.questionData.Answers.Value;
    const q_options =  props.questionData.Options; 
    const q_text =  props.questionData.Text;
    const q_type =  props.questionData.Type;

    
    return (
    <div>
        Question: {q_text}
        <br></br>
        Answer Format: {q_type}
        <br></br>
        Flags: {q_options}
        <br></br>
        Points: {q_points}
        <br></br>
        Value: {q_value}
        <br></br>
    </div>
    );
};

export default GuideQuestion;
