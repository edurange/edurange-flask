
import React  from 'react';
import { nanoid } from 'nanoid';
import './Q_and_A.css'

function GuideReading ( {
    itemContentType,
    itemContentPointer,
    chapterNumber,
    itemIndexInChapter,
    itemContent } ) {
        
    return (
        <div className='edu3-reading-frame' key={nanoid(3)}>
            <div className='edu3-reading-carpet'>
                <div className='edu-reading-text' dangerouslySetInnerHTML={{ __html: itemContent }}></div>
            </div>
        </div>
    );
}

export default GuideReading;
