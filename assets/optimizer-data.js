/* Shared data for the AI Prompt Optimizer.
   Loaded in the browser (window.AIA_OPT) and by the server (require). Edit starters here. */
(function (root, factory) {
  var data = factory();
  if (typeof module === "object" && module.exports) module.exports = data;
  else root.AIA_OPT = data;
})(typeof self !== "undefined" ? self : this, function () {
  var SKILLS_REPO = "https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills";
  var DATA_REPO = "https://github.com/Open-Medical-Affairs/Data-Sources";
  return {
    skillsRepo: SKILLS_REPO,
    dataRepo: DATA_REPO,
    therapeuticAreas: {
      "oncology-mm": { product: "NORVANTIB", area: "oncology (multiple myeloma)", label: "Oncology · NORVANTIB" },
      "immunology-ad": { product: "DERMALYX", area: "immunology (atopic dermatitis)", label: "Immunology · DERMALYX" },
      "cardiometabolic-obesity": { product: "ADIPOSYN", area: "cardiometabolic (obesity)", label: "Cardiometabolic · ADIPOSYN" },
      "own": { product: "", area: "", label: "My own material" }
    },
    skills: ["advisory-board-design","capability-detection","citation-integrity","clinical-trials-search","competitive-intelligence","congress-abstract-and-poster","congress-intelligence","consulting-grade-design","data-connection","data-visualization-for-medical","deliverable-quality-review","diagram-and-schema","document-ingestion","evidence-appraisal","evidence-gap-analysis","evidence-synthesis","executive-briefing","field-insight-synthesis","field-medical-planning","guideline-engagement","hcp-discovery-and-access","insight-generation","integrated-evidence-plan","interactive-html-report","investigator-initiated-study-review","kol-engagement-brief","launch-field-training","launch-medical-readiness","launch-timeline-and-governance","library-menu","literature-surveillance","medical-affairs-foundations","medical-affairs-metrics","medical-affairs-orchestrator","medical-content-operations","medical-correspondence","medical-education-program","medical-information-response","medical-launch-plan","medical-slide-deck","medical-strategy-plan","medical-terminology-mapping","meeting-transcription","mlr-review-readiness","msl-administrative-operations","msl-post-call-follow-up","msl-pre-call-planning","patient-engagement-planning","payer-value-dossier","pdf-generation","plain-language-summary","promotional-material-medical-review","public-evidence-search","pubmed-search","real-world-evidence-design","regulatory-label-intelligence","safety-communication","scientific-communication-strategy","scientific-manuscript","scientific-platform","spreadsheet-analysis","strategic-analysis","systematic-literature-review","visual-abstract","workshop-launcher"],
    /* Short starters that expand into full assignments. mode: single | swarm */
    starters: [
      { id: "launch", label: "Build a launch plan for ADIPOSYN", mode: "swarm", ta: "cardiometabolic-obesity", mission: "launch-plan-swarm",
        skills: ["medical-launch-plan", "launch-timeline-and-governance", "launch-field-training", "launch-medical-readiness", "executive-briefing"],
        files: ["product-profile.md", "medical-plan.md", "launch-readiness-register.md", "evidence-landscape.md", "medical-education-needs.md"],
        deliverables: ["Medical launch plan (Word) with objectives, tactics, owners and budget lines", "Launch timeline and governance calendar (Excel)", "Field training curriculum outline", "Readiness scorecard with red/amber/green and gaps", "One-page executive summary"],
        workers: ["Strategy lead: medical objectives and tactics (medical-launch-plan)", "Timeline and governance lead (launch-timeline-and-governance)", "Field training lead (launch-field-training)", "Readiness auditor (launch-medical-readiness)"] },
      { id: "congress", label: "Set up a congress monitoring swarm for ASCO", mode: "swarm", ta: "oncology-mm", mission: "congress",
        skills: ["congress-intelligence", "competitive-intelligence", "literature-surveillance", "executive-briefing"],
        files: ["congress-abstracts.md", "competitor-announcements.md", "evidence-landscape.md", "product-profile.md"],
        deliverables: ["Daily congress digest (one page per day)", "Competitor data table with source citations", "'What changed for us' brief with implications and owners"],
        workers: ["Abstract scout: screens sessions and abstracts (congress-intelligence)", "Competitor analyst (competitive-intelligence)", "Literature watcher: matching publications (literature-surveillance)"] },
      { id: "adboard", label: "Draft an ad board package on DERMALYX", mode: "single", ta: "immunology-ad", mission: "advisory-board",
        skills: ["advisory-board-design", "evidence-gap-analysis", "medical-slide-deck"],
        files: ["evidence-landscape.md", "advisory-board-transcript.md", "product-profile.md", "kol-dossiers.md"],
        deliverables: ["Advisory board objectives and agenda", "Discussion questions mapped to evidence gaps", "Pre-read slide deck (PowerPoint)", "Participant criteria (no named individuals)"] },
      { id: "insights", label: "Turn these field notes into insights", mode: "single", ta: "oncology-mm", mission: "field-insights",
        skills: ["field-insight-synthesis", "executive-briefing"],
        files: ["field-observations.csv", "interaction-notes.md", "medical-plan.md"],
        deliverables: ["Top three insights with confidence and source record IDs", "Leadership brief (Word + PDF)", "Possible safety findings flagged for routing"] },
      { id: "medinfo", label: "Medical info response on NORVANTIB dosing", mode: "single", ta: "oncology-mm", mission: "medical-information",
        skills: ["medical-information-response", "citation-integrity"],
        files: ["medical-information-enquiries.csv", "product-profile.md", "evidence-landscape.md"],
        deliverables: ["Standard response letter, balanced and on-label", "Reference list with every claim cited", "Off-label and adverse event flags"] },
      { id: "kol-map", label: "Map KOLs for obesity in the Northeast", mode: "single", ta: "cardiometabolic-obesity", mission: "hcp-access",
        skills: ["hcp-discovery-and-access", "field-medical-planning", "kol-engagement-brief"],
        files: ["kol-dossiers.md", "field-account-plan.csv", "medical-plan.md"],
        deliverables: ["Expert map by scientific area and region (table)", "Coverage and access gaps", "Engagement priorities for the field team"] },
      { id: "gaps", label: "Find evidence gaps for our asset", mode: "single", ta: "immunology-ad", mission: "evidence-investment",
        skills: ["evidence-gap-analysis", "integrated-evidence-plan", "real-world-evidence-design"],
        files: ["evidence-landscape.md", "integrated-evidence-plan.csv", "structured-evidence-table.csv", "payer-hta-brief.md"],
        deliverables: ["Evidence gap matrix (stakeholder x question x strength)", "Ranked list of studies to fund with rationale", "One-page recommendation"] },
      { id: "pubs", label: "Create a publication plan", mode: "swarm", ta: "oncology-mm", mission: "publication",
        skills: ["scientific-platform", "scientific-manuscript", "congress-abstract-and-poster", "plain-language-summary", "data-visualization-for-medical"],
        files: ["publication-plan.md", "scientific-platform-draft.md", "manuscript-draft.md", "abstract-poster-brief.md"],
        deliverables: ["18-month publication plan (Excel) with congress targets", "Messages mapped to the scientific platform", "Plain-language summary plan"],
        workers: ["Platform keeper: messages and consistency (scientific-platform)", "Manuscript planner (scientific-manuscript)", "Congress planner (congress-abstract-and-poster)", "Plain-language writer (plain-language-summary)"] },
      { id: "kol-prep", label: "Prep me for a tough KOL meeting", mode: "single", ta: "immunology-ad", mission: "kol-meeting",
        skills: ["kol-engagement-brief", "msl-pre-call-planning"],
        files: ["kol-dossiers.md", "interaction-notes.md", "evidence-landscape.md"],
        deliverables: ["Two-page pre-call brief", "Likely questions with balanced, referenced answers", "Topics to avoid or route (off-label, promotional)"] },
      { id: "transcript", label: "Turn a meeting transcript into actions", mode: "single", ta: "cardiometabolic-obesity", mission: "transcript",
        skills: ["meeting-transcription", "field-insight-synthesis"],
        files: ["advisory-board-transcript.md"],
        deliverables: ["Clean summary with decisions", "Action list with owners and dates", "Insights worth escalating"] },
      { id: "readiness", label: "Is the medical team launch-ready?", mode: "single", ta: "cardiometabolic-obesity", mission: "launch-readiness",
        skills: ["launch-medical-readiness", "mlr-review-readiness"],
        files: ["launch-readiness-register.md", "mlr-review-comments.md", "medical-plan.md"],
        deliverables: ["Readiness scorecard (red/amber/green)", "Top risks with mitigations and owners", "Go / no-go recommendation for the human to decide"] },
      { id: "thirty", label: "Run the next 30 days of Medical Affairs", mode: "swarm", ta: "oncology-mm", mission: "thirty-day-capstone",
        skills: ["medical-strategy-plan", "field-insight-synthesis", "integrated-evidence-plan", "medical-content-operations", "executive-briefing", "medical-slide-deck"],
        files: ["medical-plan.md", "field-observations.csv", "integrated-evidence-plan.csv", "medical-impact-metrics.csv"],
        deliverables: ["30-day operating plan with weekly milestones", "Leadership deck (PowerPoint, 10 slides)", "Risk and decision log"],
        workers: ["Strategy lead (medical-strategy-plan)", "Insights lead (field-insight-synthesis)", "Evidence lead (integrated-evidence-plan)", "Content operations lead (medical-content-operations)"] }
    ]
  };
});
