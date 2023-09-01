
// import React, { useState, useEffect, useContext } from 'react';
// import GuideQuestion from './GuideQuestion';
// import GuideReading from './GuideReading';
// import fetchHelper from '../../../../../../../modules/utils/fetchHelper';
// import { HomeRouterContext } from '../../../../../src/Home_router';



// function GuideInterpreter ( input_scenarioID  ) {

//      input_scenarioID = 2; // fix


// ///////////////////////////////////////////////////////////////
//     // const [scenarioInterpretation_state, set_scenarioInterpretation_state] = useState({
//     //     scenario_shellContent : {},
//     //     scenario_uniqueContent : {},
//     // });
//     const [shellContent_state, set_shellContent_state] = useState(0);  
//     const [uniqueContent_state, set_uniqueContent_state] = useState(0);  
//     const [guide_pageNumber_state, set_guide_pageNumber_state] = useState(0);  
// ////////////////////////////////////////////////////////////////

// const {
//     set_userData_state,
//     set_instructorData_state,
//     set_login_state,
//     csrfToken_state

//   } = useContext(HomeRouterContext);

//     if (!csrfToken_state) {
//         console.log("no csrf abort")
//         return (<>NO CSRF</>)}
//     useEffect(() => {
//         async function mount_scenarioContent () {
//             try {
//                 const shellContent_response = await fetchHelper (
//                     "POST",
//                     `/edurange3/dashboard/get_scenario`, 
//                     {},
//                     csrfToken_state
//                     );
//                 const shellContent = await shellContent_response;
//                 if (!shellContent) {return <>nothing here</>}
//                 set_shellContent_state (shellContent);
//                 console.log ("shellContent",shellContent);
//                 // return


                
//                 // const uniqueContent_response = await fetchHelper (
//                 //     `/api/get_state/${input_scenarioID}`);
//                 // const uniqueContent_JSON = await uniqueContent_response.json();
//                 // console.log ("uniqueContent_JSON",uniqueContent_JSON);

//                 // set_scenarioInterpretation_state(prevState => ({
//                 //     // ...prevState,                                // check this
//                 //     scenario_shellContent: shellContent,
//                 //     scenario_uniqueContent: uniqueContent_JSON
//                 // }));
//             } catch (error) {
//                 console.error('Error fetching data:', error);
//             }
//         };
//         mount_scenarioContent();
//       }, []);

//     //   console.log ("lets debug:", scenarioInterpretation_state)
//     if (!shellContent_state.Readings) {return <>no scenario found</>}
//     // if (Object.keys(shellContent_state).length < 1) {return <>no scenario found</>}
//     const { Sections, Readings, Questions } = shellContent_state.StudentGuide;
//     const orderGuide = shellContent_state.StudentGuide.SectionOrder;
//     let pageToDisplay = "";

//     const guideArray = [];
//     if (orderGuide){

//         const sectionOrderPointer = orderGuide[guide_pageNumber_state];
        
//         // const guideObject = { readings: [], questions: [] }

//         // console.log(scenarioInterpretation_state.scenario_uniqueContent);

//         for (let i = 0; i < Sections[guide_pageNumber_state].Order.length; i++ ) {

//             const orderIndexType = Sections[`${sectionOrderPointer}`].Order[i][0];
//             const orderIndexValue = Sections[`${sectionOrderPointer}`].Order[i][1];
            
//             if (orderIndexType === "r") {
//                 const returnReading = <GuideReading textData={Readings[orderIndexValue-1]} />
                
//                 console.log("PUSHING READING: ",returnReading);
//                 guideArray.push(returnReading);
//                 // guideObject.readings.push(Readings[orderIndexValue])
//             };
//             if (orderIndexType === "q") {

//                 const returnQuestion = <GuideQuestion questionData={Questions[orderIndexValue-1]} />
//                 ;
//                 console.log("PUSHING QUESTION: ",returnQuestion);
//                 guideArray.push(returnQuestion);
//                 // guideArray.push(Questions[orderIndexValue]);
//             };

//         };

//     }

//       console.log("GUIDE ARRAY:",guideArray)
    
//     return (
//             <>
//                 <div>
//                     THIS IS WHERE THE GUIDE ARRAY SHOULD BE
//                     {guideArray.map((component, index) => (
//                         React.cloneElement(component, { key: index })
//                     ))}
//                 </div>
//             </>
        
//     );
// }

// export default GuideInterpreter;

//         // pageToDisplay = ( <div dangerouslySetInnerHTML={{ __html: guideObject.readings }} /> );
