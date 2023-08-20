
import React, { useState, useEffect } from 'react';
import GuideQuestion from './GuideQuestion';
import GuideReading from './GuideReading';



function GuideInterpreter ( input_scenarioID  ) {

     input_scenarioID = 2; // fix


///////////////////////////////////////////////////////////////
    const [scenarioInterpretation_state, set_scenarioInterpretation_state] = useState({
        scenario_shellContent : {},
        scenario_uniqueContent : {},
    });
    const [guide_pageNumber_state, set_guide_pageNumber_state] = useState(0);  
////////////////////////////////////////////////////////////////


    useEffect(() => {
        async function mount_scenarioContent () {
            try {
                const shellContent_response = await fetch(`/api/get_content/${input_scenarioID}`);
                const shellContent_JSON = await shellContent_response.json();
                if (!shellContent_JSON) {return <>nothing here</>}
                console.log ("shellContent_JSON",shellContent_JSON);
                
                const uniqueContent_response = await fetch(`/api/get_state/${input_scenarioID}`);
                const uniqueContent_JSON = await uniqueContent_response.json();
                console.log ("uniqueContent_JSON",uniqueContent_JSON);

                set_scenarioInterpretation_state(prevState => ({
                    // ...prevState,                                // check this
                    scenario_shellContent: shellContent_JSON,
                    scenario_uniqueContent: uniqueContent_JSON
                }));
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        mount_scenarioContent();
      }, []);

    if (Object.keys(scenarioInterpretation_state.scenario_shellContent).length < 1) {return <>no scenario found</>}
      
    const { Sections, Readings, Questions } = scenarioInterpretation_state.scenario_shellContent.StudentGuide;
    const orderGuide = scenarioInterpretation_state.scenario_shellContent.StudentGuide.SectionOrder;
    let pageToDisplay = "";

    const guideArray = [];
    if (orderGuide){

        const sectionOrderPointer = orderGuide[guide_pageNumber_state];
        
        // const guideObject = { readings: [], questions: [] }

        console.log(scenarioInterpretation_state.scenario_uniqueContent);

        for (let i = 0; i < Sections[guide_pageNumber_state].Order.length; i++ ) {

            const orderIndexType = Sections[`${sectionOrderPointer}`].Order[i][0];
            const orderIndexValue = Sections[`${sectionOrderPointer}`].Order[i][1];
            
            if (orderIndexType === "r") {
                const returnReading = <GuideReading textData={Readings[orderIndexValue-1]} />
                
                console.log("PUSHING READING: ",returnReading);
                guideArray.push(returnReading);
                // guideObject.readings.push(Readings[orderIndexValue])
            };
            if (orderIndexType === "q") {

                const returnQuestion = <GuideQuestion questionData={Questions[orderIndexValue-1]} />
                ;
                console.log("PUSHING QUESTION: ",returnQuestion);
                guideArray.push(returnQuestion);
                // guideArray.push(Questions[orderIndexValue]);
            };

        };

    }

      console.log("GUIDE ARRAY:",guideArray)
    
    return (
            <>
                <div>
                    THIS IS WHERE THE GUIDE ARRAY SHOULD BE
                    {guideArray.map((component, index) => (
                        React.cloneElement(component, { key: index })
                    ))}
                </div>
            </>
        
    );
}

export default GuideInterpreter;

        // pageToDisplay = ( <div dangerouslySetInnerHTML={{ __html: guideObject.readings }} /> );
