

// these classes will be used by a process that uses a 'current user data' object to build out the necessary final 'guide' object
// in general, database IDs (dbid) should not be exposed in UI, but unique IDs (uid) can, as they are just arbitrary values for React to use, and have no security implications.



import { nanoid } from "nanoid";

export class GuideQuestion_shell {
    constructor(input = {}) {
        this.uid = input.uid ?? nanoid(8); // the unique question ID Or index within the page -- mostly used for React functionality -- can be exposed in UI
        this.question_text = input.question_text ?? "";  // the question as it appears to student
        this.question_isEssay = input.question_isEssay || false; // is the answer in essay form?
        this.answer_expected = input.answer_expected ?? ""  // the correct input or set of inputs
        this.answer_isCorrect = input.answer_isCorrect || false; // has the question been successfully answered?
        this.answer_history = input.answer_history ?? []; // may not need this it it's stored in backend
        this.score_current = input.score_current ?? 0; // 
        this.score_max = input.score_max ?? 3; // replace with correct score max per question
    };
}

export class GuidePage_shell {
    constructor(input = {}) {
        this.uid = input.uid ?? nanoid(8); // the unique page ID Or index within the scenario. mostly used for React functionality -- can be exposed in UI
        this.pageNumber = input.pageNumber ?? 0;  // which page in the scenario guide is this
        this.questions = input.questions || [];

    }
}

export class ScenarioGuide_shell {
    constructor(input = {}) {
        this.dbid = input.dbid ?? "none" // the actual database id for the scenario instance. should not be exposed in UI (except admin/instructor if needed)
        this.uid = input.uid ?? nanoid(8); // the unique scenario ID - can be exposed in UI (is same as URL extension)
        this.title = input.title ?? "bad_title";  // scenario title e.g. "Getting_Started"
        this.active = input.status ?? false;
    }
}

export class UserScenarioCatalog_shell {
    constructor(input = {}) {
        this.uid = input.uid ?? nanoid(8); // the unique catalog ID - can be exposed in UI
        this.scenarios = input.scenarios ?? [];  // all the scenarios in the catalog
    }
}