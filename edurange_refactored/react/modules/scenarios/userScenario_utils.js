import { 
    GuideQuestion_shell, 
    GuidePage_shell, 
    ScenarioGuide_shell, 
    UserScenarioCatalog_shell 
} from "../shells/scenario_guide_shells";
import { nanoid } from 'nanoid';

import { fakeAnswers } from "./scenario_dummyData";
export function buildScenarioGuideCatalog() {

    // 1. Start with the questions:
    const populatedQuestions = fakeAnswers.map(answer => new GuideQuestion_shell(answer));

    // 2. Dynamically generate the pages using the questions:
    const populatedPages = populatedQuestions.map((_, index) => {
        return new GuidePage_shell({
            uid: nanoid(),
            pageNumber: index + 1,
            questions: populatedQuestions
        });
    });

    // 3. Use the generated pages to generate the scenarios:
    const populatedScenarios = populatedPages.map((_, index) => {
        const scenarioData = {
            dbid: `${index + 1000}`,  // Simulated DBID based on index for dynamic assignment.
            uid: nanoid(),
            title: `Scenario ${index + 1}`,
            active: true,
        };
        const scenarioInstance = new ScenarioGuide_shell(scenarioData);
        scenarioInstance.pages = populatedPages;  // Assigning all pages to each scenario
        return scenarioInstance;
    });

    // 4. Use the generated scenarios to populate the catalog for a user:
    const populatedCatalog = [
        new UserScenarioCatalog_shell({ 
            uid: nanoid(),
            scenarios: populatedScenarios
        })
    ];

    console.log(populatedCatalog);
    return populatedCatalog;
}

