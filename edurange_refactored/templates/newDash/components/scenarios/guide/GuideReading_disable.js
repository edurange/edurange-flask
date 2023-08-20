
import React  from 'react';

function GuideReading ( props ) {
    const r_text =  props.textData; // corrected prop name here
    
    return (
        <div dangerouslySetInnerHTML={{ __html: r_text }}></div>
        // Removed {r_text} from inside div
    );
}

export default GuideReading;
