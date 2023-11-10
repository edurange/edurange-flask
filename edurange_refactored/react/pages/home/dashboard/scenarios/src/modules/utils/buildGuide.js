
// an "item" is a single reading or question

import GuideQuestion from "../../guide/Q_and_A/GuideQuestion";
import GuideReading from "../../guide/Q_and_A/GuideReading";

// one or more grouped items make up a 'chapter'

// all chapters make up a single scenario's guide 'book' array

// buildGuide() returns the book array

// Each 'chapter' will appear in the order designated by the 
// 'Content Order' pointers in the scenario's content.json, 
// and same with the items in each chapter

export default function buildGuide(scenarioID, contentJSON) {

    const readings = contentJSON.StudentGuide.Readings;
    const questions = contentJSON.StudentGuide.Questions;

    // 'Pad' certain arrays to align indices with content keys which start at 1
    const paddedChaptersOrder = [0, ...contentJSON.StudentGuide.SectionOrder];
    const paddedChapterMetas = [{}, ...contentJSON.StudentGuide.Sections];

    // 'guideBook' will store 'chapters'
    const guideBook = [];

    // Loop over each 'chapter' using the order from paddedChaptersOrder
    // begin loop at index 1 (align w/ padded order and content keys)
    for (let i = 1; i < paddedChaptersOrder.length; i++) {

        // retrieve chapter number pointed to by paddedChaptersOrder
        const thisChapterNum = paddedChaptersOrder[i]; 
        // unpack item reference array for chapter
        const thisItemReferenceArray = paddedChapterMetas[thisChapterNum]["Order"]; 

        // 'chapters' will store 'items'
        const bookChapter = [];

        // Loop over each 'itemReferencePair' (a two-element-array) in 'itemReferenceArray'
        // begin loop at index 0 (reference array itself is unpadded)
        for (let j = 0; j < thisItemReferenceArray.length; j++) {

            const itemReferencePair = thisItemReferenceArray[j];

            const itemContentType = itemReferencePair[0];    // 'q' or 'r'
            const itemContentPointer = itemReferencePair[1]; // Pointer to select content by key

            // 'items' store actual 'content'
            let itemObject = {
                itemContentType: itemContentType, // 'q' or 'r'
                itemContentPointer: itemContentPointer, // Pointer to the actual content
                chapterNumber: i,       // The chapter the item belongs to 
                itemIndexInChapter: j,  // Index of the item within its chapter
                itemContent: "",         // The actual content (populated below)
                scenario_id: scenarioID
            };

            // Assign content based on the type
            if (itemContentType === "r") {
                itemObject.itemContent = readings[itemContentPointer];
                itemObject = GuideReading(itemObject);  // convert to react component
            } else {
                itemObject.itemContent = questions[itemContentPointer];
                itemObject = GuideQuestion(itemObject); // convert to react component 
            }
            // Add the 'item' to the 'chapter'
            bookChapter.push(itemObject);
        }
        // Add the 'chapter' to the 'book'
        guideBook.push(bookChapter);
    }
    // Return the 'guide book' with all 'chapters' for single scenario
    return guideBook;
};