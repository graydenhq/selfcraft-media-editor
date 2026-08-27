SelfCraft Media Editor (SME) — Specification v1.0 

# **SelfCraft Media Editor** 

## **(SME)** 

Foundation Architecture & Development Specification _An Intelligent, Offline-First Media Production System_ 

##### **Version 1.0** 

Status: Approved for Implementation Prepared for SelfCraft Academy 

_"Create Once. Produce Everywhere."_ 

Page 1 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### Document Control 

|**Field**|**Detail**<br>|
|---|---|
|Product Name|SelfCrafMedia Editor(SME)<br>|
|Document Set|Foundaton Architecture & Development Specifcaton|
|Version|1.0<br>|
|Status|Approved for Implementaton<br>|
|Owner|SelfCrafAcademy<br>|
|Audience|Engineers, contractors, and future maintainers implementng<br>SME|



#### How to Use This Document 

This specification is written for any developer or development team picking up the project cold. It is organized so that Part I gives the product context needed to make good judgment calls, Part II defines the internal architecture and how modules communicate, and Part III defines engineering process — coding standards, testing, security, and deployment. 

Section 1.5 defines the Version 1.0 scope explicitly. Anything not listed there is out of scope for the first release, regardless of what is described elsewhere in this document as a future capability. When in doubt, build the smaller thing first. 

Page 2 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### Table of Contents 

##### **Part I — Product Foundation** 

|1. Vision & Product Strategy....................................................................................................................5|
|---|
|2. Product Requirements.........................................................................................................................8|
|**Part II — System Architecture**|
|3. Sofware Architecture.......................................................................................................................13<br>|
|4. System Workfow...............................................................................................................................17|
|5. AI Engine............................................................................................................................................20|
|6. Knowledge Engine.............................................................................................................................23|
|7. Media Engine.....................................................................................................................................25|
|8. Template Engine................................................................................................................................28|
|9. UI/UX Specifcaton............................................................................................................................31|
|10. Setngs Manager.............................................................................................................................34|
|**Part III — Engineering & Delivery**|
|11. Development Roadmap...................................................................................................................38|
|12. Internal API Reference.....................................................................................................................40|
|13. Testng Guide...................................................................................................................................41|
|14. Coding Standards.............................................................................................................................43|
|15. Security & Privacy............................................................................................................................46|
|16. Deployment Guide...........................................................................................................................48|
|Appendix A — Document Summary......................................................................................................50|



Page 3 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### Part I — Product Foundation 

This part defines why SME exists, who it serves, and exactly what Version 1.0 must deliver. 

Page 4 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 1. Vision & Product Strategy 

#### 1.1 Vision Statement 

SelfCraft Media Editor (SME) is an intelligent, offline-first media production system that transforms raw educational video into professional, publication-ready content with minimal human effort — enabling educators and organisations to produce high-quality content at scale. 

#### 1.2 Mission 

SME exists to eliminate repetitive video editing work by combining artificial intelligence, automation, and reusable editing templates into a single production system. It does not replace human creativity — it removes the repetitive production labour around it, so creators spend their time teaching, mentoring, and creating rather than editing. 

#### 1.3 Problem Statement 

Educational organisations lose significant time to repetitive post-production work: removing silence, cleaning audio, adding captions, applying branding, organising files, exporting for multiple platforms, and managing media libraries. This overhead slows publication and pulls creators away from the content itself. 

#### 1.4 Solution 

SME provides a single environment in which users store raw media and the system automatically organises projects, detects programme information and speakers, applies intelligent editing templates, runs a quality review, and exports platform-ready video. The majority of the editing process happens without manual intervention. 

#### 1.5 Version 1.0 Scope — Binding 

**_Note:_** _Anything not listed under Included below is explicitly out of scope for Version 1.0. Treat every future capability mentioned elsewhere in this document as a Phase 2+ candidate, not a v1.0 requirement._ 

###### **Included in v1.0** 

- Folder monitoring and automatic video detection 

- Preview and thumbnail generation 

- Three editing templates: Recorded Lesson, Teaching Reel, Testimonial Reel 

- AI transcription, captions, audio enhancement, silence removal 

- Folder/filename metadata extraction (programme, week, module, lesson) 

- AI quality review with pass/warning/failed status 

- Batch/queue processing with resume-on-restart 

- Export management with versioned filenames 

###### **Explicitly excluded from v1.0 (do not build yet)** 

Page 5 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

- Automatic publishing to social media 

- Cloud synchronisation 

- Team collaboration / multi-user permissions 

- AI-generated thumbnails 

- Editing-style learning from user corrections 

- Plugin marketplace 

- Multi-workspace / multi-brand support 

- macOS and Linux builds 

#### 1.6 Product Philosophy 

Every feature must satisfy at least one of the following principles. A feature that satisfies none of them should not be built. 

|**Principle**<br>|**Meaning**<br>|
|---|---|
|Automaton First|If a repettve task can be automated reliably,automate it.<br>|
|Simplicity Over Complexity|Users should spend more tme creatng content than confguring<br>sofware.<br>|
|Consistency<br>|Everyexported video maintains the sameproductonquality.<br>|
|Non-Destructve Editng|Original recordings are never modifed.|
|Modular Design<br>|Everysubsystem is independentlyreplaceable.<br>|
|Ofine First|The applicaton functons without an internet connecton<br>wheneverpossible.|
|AI as an Assistant|AI supports the user; it never removes their control over the<br>creatveprocess.|



#### 1.7 Non-Negotiable Project Rules 

These five rules override any conflicting instruction elsewhere in this specification or in future feature requests: 

- Never overwrite original media. 

- Every repetitive task should be automated where practical. 

- Every automation must be configurable. 

- The AI must explain or preview significant editing decisions before final export when its confidence is low. 

- The software must remain fully useful without any paid AI service. 

#### 1.8 Target Users 

###### **Primary** 

- SelfCraft Academy 

###### **Secondary** 

- Educational organisations and training institutions 

Page 6 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

- Leadership academies and online course creators 

- Coaches, mentors, and consultants 

- Professional speakers 

- Church media teams 

- Non-profit organisations 

#### 1.9 Primary Goals for v1.0 

- Reduce manual editing time by at least 70%. 

- Produce consistent, professional-quality video output. 

- Standardise branding across all content. 

- Support batch processing of multiple videos in one run. 

- Materially reduce time from recording to publication. 

#### 1.10 Success Indicators 

- A raw video can be processed with a single approval action. 

- Multiple videos can be processed in one production run. 

- Output quality is consistent across all supported content types. 

- Most editing decisions are made automatically. 

- Users rarely need manual timeline editing. 

#### 1.11 Product Identity 

|**Field**|**Value**<br>|
|---|---|
|Product Name<br>|SelfCrafMedia Editor|
|Abbreviaton|SME<br>|
|Category<br>|AI-Assisted Content Producton Sofware<br>|
|Platorm(v1.0)|Windows desktopapplicaton<br>|
|Architecture<br>|Ofine-frst,modular,AI-enhanced|
|Moto|"Create Once. Produce Everywhere."|



#### 1.12 Future Expansion (Phase 2+, informational only) 

The architecture should not preclude these, but none are requirements for v1.0: AI Thumbnail Studio, AI Script Assistant, AI Social Publisher, AI Analytics Dashboard, Cloud Synchronisation, Mobile Companion App, Team Collaboration Workspace, Plugin Marketplace. 

_Status: Approved Foundation Document — Version 1.0_ 

Page 7 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 2. Product Requirements 

#### 2.1 Product Overview 

SME is an AI-assisted desktop application that automates the editing, organisation, and export of educational videos. It is designed around automation rather than manual timeline editing: users interact primarily with folders and templates while the AI handles the production workflow. 

Product Goal: transform raw educational video into publication-ready content with a single production command. 

#### 2.2 Supported Video Types 

|**Type**|**Orientaton**|**Characteristcs**|
|---|---|---|
|A — Recorded Lesson|16:9 Landscape<br>|Long-form teaching, structured course content,<br>premiumquality,minimal editngafer AI<br>|
|B — Teaching Reel<br>|9:16 Vertcal<br>|Short educatonal clips, fast-paced editng,<br>natve social style,sof branding<br>|
|C — Testmonial Reel|9:16 Vertcal|Partcipant stories; AI detects partcipant name;<br>programme identfed from folder;sof branding|



#### 2.3 User Workflow (End to End) 

- 1. Launch SME 

- 2. Media Library opens 

- 3. SME scans watched folders 

- 4. New videos detected 

- 5. Previews generated 

- 6. AI identifies content type 

- 7. User reviews queue 

- 8. User starts production 

- 9. AI edits videos 

- 10. Quality review runs 

- 11. Export 

- 12. Stored in Edited Videos folder 

#### 2.4 Functional Requirements 

|**ID**|**Requirement**<br>|
|---|---|
|FR-001|Automatcallydetect new videos inside watched folders.|
|FR-002|Generatepreview thumbnails for everyvideo.<br>|
|FR-003|Playvideopreviews before editng.<br>|
|FR-004|Automatcally determine the editng template from folder locaton or the actve<br>productonprofle.|



Page 8 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

|**ID**|**Requirement**<br>|
|---|---|
|FR-005|Automatcally detect Programme, Week, Module, Lesson Number, and Lesson Title<br>from folder hierarchy and flename for recorded lessons. Week, Module, and Lesson<br>are independent metadata — SME must never infer one from another; it reads<br>exactlywhat the folder structure states.<br>|
|FR-006|Automatcally detect partcipant names from testmonial videos via speech<br>recogniton. If confdence is below threshold, ask the user to confrm or correct the<br>name before rendering.<br>|
|FR-007|Generate captons automatcally.<br>|
|FR-008|Improve audioqualityautomatcally.<br>|
|FR-009|Remove unnecessarysilence automatcally.<br>|
|FR-010|Applythe correct editngtemplate automatcally.|
|FR-011|Perform AIQualityReview before export.<br>|
|FR-012|Export video using predefnedplatorm setngs.<br>|
|FR-013|Never overwrite original video fles.|
|FR-014|Store edited videos in the matching Edited Videos folder, preserving the original<br>flename and appending"(Edited)" or a version number.<br>|
|FR-015|Supportprocessingmultple videos in aproductonqueue.|



#### 2.5 Template Specifications 

##### Recorded Lesson Template 

- Coach introduction 

- Programme name, week, module, lesson number, lesson title 

- Premium captions 

- Audio enhancement 

- Silence removal 

- Quality review 

- Landscape export 

##### Teaching Reel Template 

- AI cuts 

- Dynamic captions 

- Zooms and motion effects 

- Soft CTA 

- Minimal branding 

- Vertical export 

- No lower-third speaker card 

##### Testimonial Reel Template 

- AI speaker detection 

- Participant name + programme title displayed 

Page 9 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

- Dynamic captions 

- Audio enhancement 

- Soft CTA 

- Vertical export 

Display format example: "Sarah Okafor — Youth Compass Guide Participant". 

#### 2.6 Folder Structure 

The folder structure is itself a metadata source — folder names feed the Folder Intelligence Engine directly. 

SelfCraft Media/ 

Raw Videos/ Recorded Classes/ Teaching Reels/ Testimonials/ 

Edited Videos/ Assets/ Exports/ Archive/ 

#### 2.7 Asset Management 

SME must centrally manage intros, outros, fonts, watermark, brand colours, music, motion graphics, and CTA templates. All assets must be editable without changing code. 

#### 2.8 Export Requirements 

|**Output**<br>Recorded<br>Lessons|**Forma**<br>**t**<br>MP4|**Codec**<br>H.264|**Audio**<br>AAC|**Resoluton**<br>1920×1080|**Frame Rate**<br>Match source<br>wherepractcal|**Quality**<br>High variable<br>bitrate|
|---|---|---|---|---|---|---|
|Social Reels|MP4|H.264|AAC|1080×1920|Match source<br>wherepractcal|High variable<br>bitrate|



#### 2.9 Performance Requirements 

- Queue multiple videos. 

- Continue processing after individual failures where possible. 

- Maintain production logs. 

- Resume interrupted jobs where practical. 

Page 10 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

#### 2.10 Quality Review Checklist 

- Audio clarity 

- Caption timing 

- Branding consistency 

- Speaker identification 

- Export settings 

- Rendering errors 

- Missing assets 

- Excessive silence 

#### 2.11 Error Handling Principle 

SME must never fail silently. On error it must: identify the affected video, explain the problem in plain language, suggest a corrective action where possible, and continue processing the remaining queue if appropriate. 

#### 2.12 Non-Functional Requirements 

- Offline-first architecture 

- Modular design 

- Cross-platform-ready design (Windows first) 

- Non-destructive editing 

- Secure local storage 

- High-performance batch processing 

_Status: Approved Foundation Draft — Version 1.0_ 

Page 11 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### Part II — System Architecture 

This part defines the complete internal design of SME: module structure, AI pipeline, data flow, and how every component communicates. Once approved, the core architecture should not change without a documented reason — extend it through new modules, not redesign. 

Page 12 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 3. Software Architecture 

#### 3.1 Architecture Principles 

- Modular 

- Offline-first 

- Event-driven 

- AI-assisted 

- Non-destructive 

- Scalable 

- Maintainable 

#### 3.2 High-Level Architecture 

A Workflow Orchestrator sits at the centre of the system as its coordination layer. Modules do not call each other directly — they communicate through the Orchestrator. This keeps modules independently replaceable, makes new features insertable without rewriting existing modules, isolates failures, and lets future capability (e.g. cloud or distributed rendering) be added by extending the Orchestrator rather than redesigning the system. 

Media Library    AI Processing Engine    Configuration \                |                    / Workflow Orchestrator 

/            |             \ 

Queue Manager   Quality Reviewer   Export Manager 

| Edited Video Library 

#### 3.3 Core Modules 

|**Module**|**Responsibility**|
|---|---|
|Media Asset Management<br>(MAM) Engine|Indexes video, manages thumbnails/previews, tracks original vs.<br>edited versions, detects duplicates, monitors watched folders,<br>verifes original-fle integrity.<br>|
|Folder Intelligence Engine|Reads folder structure and flename to extract Programme, Week,<br>Module, Lesson Number, Lesson Title. Never infers one feld from<br>another — reads exactlywhat the user's folder structure states.<br>|
|Media Analysis Engine|Analyses each video before editng: resoluton, aspect rato,<br>duraton,audioquality,frame rate,orientaton,faces,speech.<br>|
|AI Processing Engine|The intelligence layer: speech recogniton, capton generaton,<br>silence detecton, speaker-name detecton, editng decisions, CTA<br>inserton, qualityanalysis.|
|Template Engine|Holds the three v1.0 templates (Recorded Lesson, Teaching Reel,<br>Testmonial Reel), each defning animaton, captons, branding,<br>music,intro/outro,and export format.|



Page 13 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

|**Module**|**Responsibility**<br>|
|---|---|
|Rendering Engine|Assembles video, mixes audio, renders captons and moton<br>graphics,encodes fnal output.<br>|
|Quality Review Engine<br>|Runs automatcally afer rendering; checks audio, video, captons,<br>branding, speaker detecton, CTA, export quality; assigns a status<br>and fags issues.<br>|
|Producton Manager|Controls the workfow end to end: start, pause, resume, retry,<br>complete batchjobs.<br>|
|Queue Manager|Maintainsproducton order andper-item status.<br>|
|Export Manager<br>|Applies export profle, generates output flenames, creates versions,<br>saves output,verifes export.<br>|
|Confguraton Manager|Stores editable setngs: fonts, watermark, CTA, colours, intro/outro,<br>music, export setngs, AI behaviour. No code changes required to<br>update.|
|Knowledge Engine|Central repository of trusted reference data (speakers, programmes,<br>templates,CTAs,brand assets)— see Secton 6.<br>|
|Project Logger|Records every producton session: start/end tme, duraton, errors,<br>AI confdence,exportpath, qualityscore.|



#### 3.4 Production Workflow 

Video Detected → Preview Generated → Metadata Read → Template Selected → AI Analysis → Editing → Rendering → Quality Review → Export → Production Log Updated 

#### 3.5 Internal Folder Structure 

selfcraft-media-editor/ app/ core/ engines/ templates/ assets/ database/ config/ logs/ cache/ exports/ projects/ plugins/ updates/ Each folder has a single responsibility. 

#### 3.6 AI Pipeline 

Speech AI → Transcription → Speaker Detection → Metadata Extraction → Editing Decisions → Caption Generation → Quality Review 

Page 14 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

This pipeline can be improved independently as AI models evolve, without changing the modules around it. 

#### 3.7 Configuration Flow 

Settings → Configuration Manager → Template Engine → Rendering Engine A settings change immediately affects future productions without requiring an application restart, where practical. 

#### 3.8 Error Recovery 

If one item in a queue fails, the queue continues; the failed item is reported for review rather than halting the batch. 

#### 3.9 Security 

- Original videos are read-only. 

- All editing is non-destructive. 

- User data remains local by default. 

- No external upload without explicit user approval. 

- Production logs are stored locally. 

#### 3.10 Performance Goals 

- Detect new media automatically. 

- Queue jobs without an artificial limit, subject to storage and hardware. 

- Resume interrupted processing. 

- Minimise memory usage where practical. 

- Use GPU acceleration when available, with a working CPU-only fallback. 

#### 3.11 Extension System (Phase 2+) 

A future plugin system should allow new capability without modifying the core application: AI plugins, caption plugins, export plugins, template plugins, publishing plugins, language plugins. Not required for v1.0 — the module boundaries above should simply not preclude it. 

#### 3.12 Technology Stack 

|**Layer**|**Choice**|
|---|---|
|Frontend|React + TypeScript,Electron desktopshell|
|Backend|Python|
|Core framework|FastAPI(local API between UI andprocessingengine)|
|Speech AI|Whisper(speech-to-text)|
|Video analysis|OpenCV|
|Media processing /<br>rendering|FFmpeg, orchestrated from Python|



Page 15 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

|**Layer**|**Choice**|
|---|---|
|Confguraton storage|JSON initally;migrate to SQLite if scale requires it|



#### 3.13 Design Rule 

Every engine must satisfy three conditions: it can be tested independently; it communicates only through well-defined interfaces; it can be upgraded without breaking the rest of the system. 

#### 3.14 Deferred: Multi-Workspace Support 

**_Note:_** _A Workspace Manager (multiple brands/organisations, each with its own programmes, branding, templates, and assets) is a credible Phase 2+ direction if SME is ever offered beyond SelfCraft Academy. It is deliberately not part of v1.0 — building it now would add configuration surface area with no current user. Keep module boundaries clean enough that it can be added later without a rewrite; do not build it yet._ 

_Status: Approved Draft — Version 1.0_ 

Page 16 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 4. System Workflow 

This chapter defines how every video moves through SME, from appearing in a watched folder to the final edited version being stored. Every production follows the same reliable process. 

#### 4.1 Application Startup 

Application Starts → Load Configuration → Load Asset Library → Load Templates → Start Folder Watcher → Scan Media Library → Generate Preview Cache → Ready For Production 

#### 4.2 New Video Detection 

New Video Found → Validate File → Generate Thumbnail → Generate Preview → Add To Production Queue 

The user never manually imports files. 

#### 4.3 Folder Intelligence Workflow 

Example: Recorded Classes / Youth Compass Guide / Week 3 / Module 1 / "Lesson 7 - Building Daily Discipline.mp4" 

Extracted metadata: Programme = Youth Compass Guide · Week = Week 3 · Module = Module 1 · Lesson Number = 7 · Lesson Title = Building Daily Discipline. No assumption is made about numbering relationships between these fields. 

#### 4.4 Template Selection 

|**Source Folder**|**Template Applied**|
|---|---|
|Recorded Classes/|Recorded Lesson Template|
|TeachingReels/<br>|TeachingReel Template<br>|
|Testmonials/|Testmonial Reel Template|



The user can manually override the detected template if necessary. 

#### 4.5 AI Processing Workflow 

Speech Recognition → Transcription → Silence Detection → Caption Generation → Speaker Detection (testimonials only) → Editing Decisions → Timeline Construction 

#### 4.6 Rendering Workflow 

Clean Audio → Remove Silence → Insert Intro → Apply Motion Graphics → Render Captions → Insert CTA → Render Video Each step is logged for troubleshooting. 

#### 4.7 Quality Review Workflow 

- Audio Quality 

- Caption Timing 

Page 17 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

- Caption Accuracy 

- Video Resolution 

- Branding 

- CTA Present 

- Speaker Information 

- Export Settings 

- Rendering Errors 

If every check passes, status is READY. Otherwise, status is REVIEW REQUIRED. 

#### 4.8 Export Workflow & Naming Convention 

Rendered Video → Generate Output Name → Check Existing File → Create Version If Needed → Save To Edited Folder → Update Production Log 

Example: "Lesson 7 - Building Daily Discipline.mp4" → "Lesson 7 - Building Daily Discipline (Edited).mp4". If that file already exists: "...(Edited v2).mp4". 

#### 4.9 Queue Behaviour 

If a job fails: record the error, continue with the next item, notify the user at the end of the run — never halt the whole batch on a single failure. 

#### 4.10 Watch Folder Behaviour 

SME monitors watched folders in real time. When files are added, renamed, moved, or deleted, the Media Library updates automatically. No manual refresh is required. 

#### 4.11 Failure Recovery 

If processing stops unexpectedly, on restart SME detects the previous production session and prompts: Resume, or Discard. This prevents losing long production sessions. 

#### 4.12 Future Cloud Workflow (Phase 2+) 

The architecture should allow Local, Cloud, or Hybrid processing in the future without changing the production workflow itself. Not a v1.0 requirement. 

#### 4.13 Production Profiles 

A Production Profile is a saved preset for a production session, so the user doesn't reselect folders and options every time. Choosing a profile automatically applies the correct template and settings to the right content. 

|**Profle**<br>|**Behaviour**|
|---|---|
|DailyContent Profle<br>|Processes onlyTeachingReels from the watched folders.|
|Course Producton Profle<br>|Processes onlyRecorded Lessons with the full lesson template.<br>|
|Testmonial Campaign|Processes onlyTestmonial Reels,applyingthe current campaign|



Page 18 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

|**Profle**|**Behaviour**|
|---|---|
|Profle|CTA.|



#### 4.14 Workflow Principles 

- Predictable 

- Repeatable 

- Recoverable 

- Non-destructive 

- Mostly automatic 

- User-controllable 

_Status: Approved Draft — Version 1.0_ 

Page 19 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 5. AI Engine 

The AI Engine is the decision-making centre of SME. Its role is to automate repetitive editing decisions while preserving consistent quality — it acts as an intelligent production assistant, never as a replacement for creative control. 

#### 5.1 AI Subsystems 

|**Subsystem**|**Responsibilites**<br>|**Outputs**|
|---|---|---|
|Speech<br>Intelligence|Speech-to-text transcripton, speaker-name<br>detecton, capton tming, confdence scoring.<br>|Transcript, word<br>tmestamps, speaker<br>confdence<br>|
|Video Intelligence|Face detecton, shot-boundary detecton,<br>orientaton detecton, moton analysis, frame<br>quality.<br>|Scene informaton, face<br>positon, moton tmeline|
|Audio Intelligence|Noise detecton, silence detecton, volume<br>balancing,audioqualityscoring.<br>|Cleaned audio, loudness<br>report,silence map|
|Metadata<br>Intelligence|Reads folder names, flenames, template type,<br>and confguraton.<br>|Programme, week,<br>module, lesson<br>number/ttle, content<br>category|
|Template<br>Intelligence|Chooses the template based on folder locaton<br>and actveproductonprofle.<br>|Selected template|
|Quality<br>Intelligence|Checks audio, captons, branding, resoluton,<br>export setngs, CTA, speaker info afer<br>rendering.|Pass / Warning / Failed|



#### 5.2 Decision Rules by Confidence 

|**Confdence**|**Example**<br>|**Behaviour**<br>|
|---|---|---|
|High|Orientaton detecton; reading lesson ttle<br>from flename; programme from folder<br>|Proceed automatcally.<br>|
|Medium|Detectng a partcipant's name from speech|Ask for user confrmaton if<br>confdence falls below the<br>confgured threshold.|
|Low|Cannot determine the correct template;<br>cannot identfy speech; branding assets<br>missing|Pause processing for that item<br>and notfy the user.|



#### 5.3 AI Confidence Thresholds (default, configurable) 

|**Task**|**Default Threshold**<br>|
|---|---|
|Folder metadata<br>|100%(deterministc — not a modelpredicton)|
|Template selecton<br>|95%|
|Orientaton detecton<br>|99%|
|Speech transcripton<br>|90%|
|Speaker name detecton|85%|



Page 20 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

**<mark>Task Default Threshold</mark>** <mark>Capton alignment 95%</mark> 

#### 5.4 Caption Intelligence 

- Generate accurate subtitles. 

- Split lines naturally. 

- Avoid covering the speaker's face where possible. 

- Follow the active template's caption style. 

#### 5.5 CTA Intelligence 

The AI does not write CTAs. It retrieves the currently active CTA from the Configuration Manager (e.g. "Join our current challenge"), so campaigns can change without touching editing logic. 

#### 5.6 Speaker Detection 

###### **Recorded Lessons** 

Defaults to the configured speaker profile (e.g. "Coach Excel, Founder, SelfCraft Academy") unless another speaker profile is selected. 

###### **Testimonials** 

Speech Intelligence listens to the introduction (e.g. "My name is Sarah Okafor..."), extracts the name, and displays it with the programme name: "Sarah Okafor — Youth Compass Guide Participant." If uncertain, SME requests confirmation before rendering. 

#### 5.7 AI Processing Memory 

The AI keeps temporary memory for the current job only — transcript, metadata, processing state, quality checks — and discards it after completion unless a future version enables an explicit learning feature. 

#### 5.8 Privacy 

- AI processing runs locally whenever practical. 

- No video leaves the user's device without explicit permission. 

- External AI services remain optional, never required. 

#### 5.9 AI Failure Handling 

- Record the error. 

- Continue with non-dependent tasks where possible. 

- Mark the job for review. 

- Never corrupt the original media. 

Page 21 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

#### 5.10 AI Design Principles 

- Explainable 

- Consistent 

- Reproducible 

- Non-destructive 

- Configurable 

The AI assists the user; it never removes their ability to review or override a decision. 

#### 5.11 Implementation Risk — Editing Decision Logic 

**_Note:_** _Of everything in this specification, the actual logic behind "AI editing decisions" (what to cut, where to zoom, how to pace a reel) is the least defined and the highest-risk piece to build. Before committing sprint time to it, run a short technical spike: take 3–5 real recordings, and prototype rulebased heuristics (e.g. cut on silence + filler-word detection, zoom on emphasis via audio energy) before reaching for a learned model. Confirm the approach on real footage before writing it into the Media Engine as if it were settled._ 

#### 5.12 Future AI Modules (Phase 2+) 

- Highlight detection 

- Automatic B-roll suggestions 

- Auto thumbnail generation 

- Multi-language captions 

- Voice enhancement 

- Content summarisation 

- Editing preference learning 

_Status: Approved Draft — Version 1.0_ 

Page 22 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 6. Knowledge Engine 

The Knowledge Engine is the central repository of information used across SME. It does not edit video and it does not make AI decisions — it provides trusted reference data to every other module. Design philosophy: every piece of information has one authoritative source; change it once and every part of SME uses the updated value. 

#### 6.1 Knowledge Categories 

|**Category**|**Contents**<br>|
|---|---|
|Speaker Database|Name, role, organisaton, preferred display name, default template,<br>actve status. Example: "Coach Excel — Founder, SelfCraf Academy —<br>Default Speaker — Actve."<br>|
|Programme Database|Programme name, descripton, status, folder name, default CTA, default<br>intro/outro. Example: "Youth Compass Guide — Folder: Youth Compass<br>Guide — Status: Actve."|
|Course Structure<br>Database|The academic structure (Programme → Week → Module → Lesson<br>Number → Lesson Title) that detected metadata is validated against<br>when available.<br>|
|Template Library|All producton templates, each with animaton, capton style, CTA<br>placement,motongraphics,watermark behaviour,exportprofle.<br>|
|CTA Library|Reusable calls to acton. Only one CTA is actve at a tme unless a<br>Producton Profle overrides it.<br>|
|Brand Asset Library|Watermark text, fonts, brand colours, music, intro, outro, moton<br>graphics — all editable through the applicaton.<br>|
|Social Media Library<br>|Ofcial accounts (Facebook, Instagram, TikTok, YouTube, LinkedIn)<br>inserted into end cards where applicable.<br>|
|Producton Profles|Folders, templates, CTA, export setngs, and priority for a saved<br>productonpreset.|



#### 6.2 Relationships 

Programme → Course Structure → Videos → Templates → Rendering Every module reads from the same source, so there is never a conflicting copy of the same fact. 

#### 6.3 Access Rules 

|**Module**<br>|**Read**|**Write**|
|---|---|---|
|Confguraton Manager|Yes|Yes|
|Programme Manager|Yes|Yes|
|Speaker Manager|Yes|Yes|
|Template Manager|Yes|Yes|
|RenderingEngine|Yes|No|
|AI Engine|Yes|No|



Restricting write access to authorised managers prevents accidental corruption of shared reference data. 

Page 23 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

#### 6.4 Pre-Production Validation 

- Programme exists 

- Template exists 

- CTA exists 

- Required assets exist 

- Export profile exists 

If anything is missing, the production dashboard reports it before rendering begins — not mid-render. 

#### 6.5 Design Principles 

- Centralised 

- Editable 

- Versioned 

- Consistent 

- Reliable 

- Independent from AI logic 

#### 6.6 Future Expansion (Phase 2+) 

- Multi-language branding 

- Multiple organisations 

- Team permissions 

- Sponsor libraries 

- Intro/outro collections 

- Sound-effect libraries 

- AI editing presets 

_Status: Approved Draft — Version 1.0_ 

Page 24 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 7. Media Engine 

The Media Engine transforms raw media into professionally edited video. It receives instructions from the Workflow Orchestrator and AI Engine, executes them, and produces the final output. It must always perform non-destructive editing, leaving original files untouched. 

#### 7.1 Sub-Engines 

Video Engine · Audio Engine · Caption Engine  →  Rendering Engine  →  Export Engine 

##### Video Processing 

- Read and decode video files 

- Detect orientation 

- Trim unwanted sections 

- Apply AI editing decisions 

- Scene transition management 

- Motion graphics and watermark placement 

- Intro/outro insertion 

Future: crop/reframe, stabilisation, colour correction. 

##### Audio Processing 

- Noise reduction and hum removal 

- Volume normalisation 

- Silence detection and removal 

- Audio enhancement 

- Background music mixing, fade in/out, CTA music 

- Loudness balancing 

Future: echo reduction, AI voice enhancement, automatic microphone matching, breath reduction. 

##### Caption Engine 

- Receive transcript and synchronise captions 

- Break long sentences naturally 

- Position captions intelligently 

- Apply the active template's caption style 

- Avoid covering faces where practical 

|**Template**|**Capton Style**<br>|
|---|---|
|Recorded Lessons|Clean, professional,minimal animaton<br>|
|Teaching Reels<br>|Dynamic, animated, large mobile-friendly text, retenton-<br>focused<br>|
|Testmonial Reels|Elegant,easyto read,emoton-focused,consistent branding|



Page 25 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

#### 7.2 Rendering Order 

Background Video → Video Effects → Motion Graphics → Watermark → Captions → Audio → CTA → Encode 

#### 7.3 Export Profiles 

|**Profle**|**Format**|**Codec**|**Resoluton**|**Audio**|**Frame Rate**|**Qual**<br>**ity**|
|---|---|---|---|---|---|---|
|Recorded Lesson|MP4|H.264|1920×1080|AAC|Match source|High<br>VBR|
|Social Video<br>(Reel/Testmonial)|MP4|H.264|1080×1920|AAC|Match source|High<br>VBR|



#### 7.4 Media Pipeline 

Raw Video → Decode → Video Processing → Audio Processing → Caption Rendering → Motion Graphics → Brand Assets → Final Rendering → Export → Edited Video 

#### 7.5 Error Recovery 

- Save intermediate progress where practical. 

- Record the failure. 

- Keep the original file intact. 

- Continue with the next queued job. 

- Notify the user after the production run. 

#### 7.6 Performance Optimisation 

- Use GPU acceleration when available; fall back to CPU automatically. 

- Cache reusable assets (logos, intros, outros, fonts). 

- Process independent tasks in parallel when safe. 

- Reuse decoded assets across a batch where possible. 

#### 7.7 Asset Management Sub-Engine 

Assets (intros, outros, fonts, music, motion graphics, CTAs, watermark text) are managed as versioned, reusable resources rather than plain files: indexed, version-tracked, checked for missing/duplicate entries, validated for template compatibility, and cached for faster rendering. This keeps the Media Engine focused purely on processing while a dedicated component manages what it depends on. 

#### 7.8 Future Expansion (Phase 2+) 

- Multi-camera editing 

- AI B-roll insertion 

- Auto colour grading 

Page 26 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

- Auto reframing 

- Background replacement 

- AI object tracking / eye-contact correction 

- HDR export, 4K/8K workflows 

#### 7.9 Design Principles 

- Fast 

- Stable 

- Non-destructive 

- Modular 

- Hardware-aware 

- Deterministic 

- Extensible 

_Status: Approved Draft — Version 1.0_ 

Page 27 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 8. Template Engine 

The Template Engine provides reusable editing templates that keep every video consistent with the brand. Templates define what appears, when, and how — they never edit video directly; they hand structured instructions to the Media Engine. 

#### 8.1 Shared Rules 

Every template inherits from the Configuration Manager: brand colours, fonts, watermark text, motion graphics, CTA library, social handles, intro/outro assets, and export profile. No template may contain hard-coded branding. 

#### 8.2 Template A — Recorded Class 

|**Field**|**Detail**<br>|
|---|---|
|Purpose<br>|Premium educatonal lessons for online courses and learning platorms|
|Targetplatorms<br>|Learning portals,recorded courses,YouTube long-form|
|Aspect rato|16:9|



Workflow: Video Starts → Professional Intro → Course Information Card → Lesson Begins → Teaching Content → Closing Screen → Export. 

Opening card (displays 5–7 seconds): speaker name and role, programme, week, module, lesson number, lesson title — all sourced automatically from the folder structure and filename. 

During lesson: no large overlays, optional watermark, professional captions, clean transitions, audio enhancement, silence removal. 

Closing screen: thank-you message, programme name, brand identity. Unlike reels, recorded lessons do not include a challenge/registration CTA. 

#### 8.3 Template B — Teaching Reel 

|**Field**|**Detail**<br>|
|---|---|
|Purpose<br>|Engagingshort-form educatonal content natve to social media|
|Targetplatorms<br>|Instagram Reels,TikTok,Facebook Reels,YouTube Shorts,LinkedIn Video|
|Aspect rato|9:16|



Opening: no intro animation — starts immediately on the strongest teaching moment. 

During video: AI-generated dynamic captions, intelligent zooms, fast-paced editing, silence removal, audio enhancement, small optional watermark, no lower-third speaker card — focus stays entirely on the teaching. 

Closing screen (2–3 seconds): brand identity, social handles, CTA loaded dynamically from the CTA Library. 

#### 8.4 Template C — Testimonial Reel 

|**Field**|**Detail**|
|---|---|
|Purpose|Authentc,trustworthy partcipant testmonials for social media|



Page 28 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

|**Field**|**Detail**|
|---|---|
|Targetplatorms<br>|Instagram Reels,TikTok,Facebook Reels,YouTube Shorts,LinkedIn Video|
|Aspect rato|9:16|



Opening: the AI analyses the introduction; if the participant states their name, SME extracts and displays it with the programme name (e.g. "Sarah Okafor — Youth Compass Guide Participant"). If confidence is below the configured threshold, SME asks for confirmation before rendering. 

During video: dynamic captions, audio enhancement, silence removal, natural pacing, minimal branding — the participant remains the visual focus. 

Closing screen: thank-you, CTA, brand identity, social handles. 

#### 8.5 Template Selection Rules 

|**Folder**|**Template**|
|---|---|
|Recorded Classes/|Recorded Class|
|TeachingReels/|TeachingReel|
|Testmonials/|Testmonial Reel|



Users may manually override the detected template. 

#### 8.6 Pre-Render Validation 

- Required assets exist. 

- Export profile is available. 

- Fonts are installed or bundled. 

- CTA is available where applicable. 

- Branding configuration is complete. 

Any missing dependency is reported before processing begins. 

#### 8.7 Future Templates (Phase 2+) 

- Podcast Clips 

- Webinar Highlights 

- Event Recaps 

- Promotional Videos 

- Announcement Videos 

- Documentary Style 

- Interview Style 

- Multi-Speaker Panels 

Adding a new template should require no changes to the Media Engine. 

#### 8.8 Design Principles 

- Consistent 

Page 29 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

- Editable 

- Reusable 

- Modular 

- Platform-appropriate 

- Non-destructive 

- Configurable through the application 

_Status: Approved Draft — Version 1.0_ 

Page 30 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 9. UI/UX Specification 

SME should feel like a production control centre, not a traditional video editor. Users should rarely see a timeline or dozens of editing controls — they review, approve, and monitor production. Someone with little or no video-editing experience should still produce professional results. 

#### 9.1 UX Principles 

- Automation First 

- Minimal Clicks 

- Modern, Clean Layout 

- Fast Navigation 

- Beginner Friendly 

- Professional Appearance 

- Keyboard Shortcut Support 

**_Note:_** _Dark/light theme support is a Phase 2+ nicety, not required for v1.0._ 

#### 9.2 Main Navigation (always visible) 

- Dashboard 

- Media Library 

- Production Queue 

- Preview 

- Templates 

- Assets 

- Programmes 

- Speakers 

- Settings 

- Production Logs 

#### 9.3 Dashboard 

###### **Summary cards** 

Videos Waiting, Currently Processing, Completed Today, Failed, Estimated Time Remaining. 

###### **Quick actions** 

- Scan Folders 

- Start Production 

- Resume Production 

- Pause Queue 

- Open Edited Videos 

Page 31 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

- Open Settings 

###### **Recent activity feed** 

Example: "Lesson 7 Rendered", "Testimonial 15 Completed", "Reel 84 Exported", "⚠ Missing Intro Video." 

#### 9.4 Media Library 

Folder panel: Recorded Classes, Teaching Reels, Testimonials, Edited Videos, Archive. 

Each video card shows: thumbnail, filename, programme, duration, resolution, status, template, date added. 

Filters: programme, video type, status, date, resolution, aspect ratio. Search by lesson title, programme, speaker, or filename. 

#### 9.5 Preview Screen 

Left panel — video player: play, pause, frame step, volume, full screen. 

Right panel — metadata (programme, week, module, lesson, template, resolution, duration) and AI analysis (audio quality, caption confidence, speaker detection, chosen template). 

Actions: preview edited version, re-run analysis, change template, edit metadata, add to / remove from queue. 

#### 9.6 Production Queue 

Lists every job with status (Processing / Waiting / Completed) and progress percentage. Actions: Pause, Resume, Retry, Cancel, and optional reorder. 

#### 9.7 Asset Manager 

Categories: Logos, Fonts, Music, Intros, Outros, Motion Graphics, Watermarks, CTA Screens. Each asset shows preview, version, last modified, and which templates use it. Actions: Add, Replace, Delete, Duplicate, Preview. 

#### 9.8 Settings 

|**Group**|**Contents**<br>|
|---|---|
|General|Language,theme,auto-save,GPU acceleraton, processingthreads|
|Branding|Watermark text,brand colours,fonts,intro,outro<br>|
|Export|Resoluton,bitrate,codec,audio setngs,namingconventon<br>|
|AI|Capton confdence threshold, speaker detecton threshold, auto-approve<br>confdence,silence removal sensitvity<br>|
|Storage|Watch folders,cache locaton,export folder,archive folder|



Page 32 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

#### 9.9 Programme, Speaker & Template Managers 

Programme Manager: name, folder mapping, default CTA, intro, outro, active status. Speaker Manager: presenter profiles (name, role). Template Manager: duplicate, edit rules, preview output style, and assign templates to production profiles. 

#### 9.10 Notifications 

Every notification explains the issue and suggests a corrective action where possible — e.g. "⚠ Missing Font", "⚠ CTA Not Configured", "✗ Audio Processing Failed." 

#### 9.11 Production Logs 

Each session records start/end time, videos processed, successes, failures, duration, and output location. Searchable and filterable for troubleshooting. 

#### 9.12 Accessibility 

- Scalable text sizes 

- High-contrast mode 

- Keyboard navigation 

- Status indicators that don't rely on colour alone 

- Screen-reader-friendly labels where practical 

#### 9.13 Design Test 

Every screen should let the user quickly answer one of: What needs my attention? What is the system doing? Can I fix a problem easily? Can I approve production with confidence? 

_Status: Approved Draft — Version 1.0_ 

Page 33 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 10. Settings Manager 

The Settings Manager is the central configuration system for SME. It stores every user-editable setting and distributes it to the relevant modules. No template or engine may contain hard-coded branding, export settings, or campaign information. 

#### 10.1 Settings Categories 

- General Settings 

- Branding 

- Fonts 

- Export Profiles 

- CTA Manager 

- Social Media 

- AI Configuration 

- Storage 

- Performance 

- Notifications 

- Backup & Restore 

#### 10.2 Branding 

Fields: organisation name, display name, watermark text, primary/secondary/accent colour, logo (future), default intro, default outro. Applied automatically across every template. Must support future multi-workspace capability without a redesign, even though multi-workspace itself is not built in v1.0. 

#### 10.3 Font Manager 

Categories: heading, body, caption, title font. Defaults: Poppins SemiBold, Inter, Noto Sans (fallback). Supports uploading custom fonts, previewing, assigning per template, and language fallback. 

#### 10.4 Export Settings 

Recorded Lesson profile: 1920×1080, 16:9, H.264, MP4, AAC, match-source frame rate, high VBR. Teaching Reel profile: 1080×1920, 9:16, H.264, MP4, AAC, match-source frame rate, high VBR. Testimonial Reel uses the Teaching Reel profile unless overridden. 

Advanced options: GPU vs. CPU encoding, maximum file size (optional), audio/video bitrate, colour space, render priority. 

#### 10.5 CTA Manager 

Fields: title, description, display text, end screen, button text (future), QR code (future), status. Only one CTA is active by default; Production Profiles may override it. 

Page 34 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

#### 10.6 Social Media Manager 

Supported platforms: Facebook, Instagram, TikTok, YouTube, LinkedIn. Fields: platform, display name, username, profile URL, visibility, display order. Templates reference these automatically. 

#### 10.7 AI Settings 

Speech: transcription confidence threshold, speaker detection threshold. Editing: silence removal sensitivity, auto-cut sensitivity, motion intensity, caption animation level. Approval: auto-approve highconfidence edits, require review for low-confidence items, enable AI quality scoring. 

#### 10.8 Storage Settings 

Configurable locations for Raw Videos (Recorded Classes, Teaching Reels, Testimonials), Edited Videos, Assets, Cache, Logs, Archive. Users may add additional watch folders. 

#### 10.9 Performance Settings 

Processing: GPU acceleration, CPU threads, parallel rendering, background processing, cache size. Optimisation: preview resolution, thumbnail quality, memory usage limit. 

#### 10.10 Notification Settings 

Events: production started/complete/failed, missing assets, AI review required, export complete. Delivery methods: in-app, desktop notification, optional sound alert. 

#### 10.11 Backup & Restore 

Exportable/importable configuration bundle: branding, templates, fonts, CTAs, social handles, export profiles, AI preferences, production profiles — enough to move a complete SME setup to another machine. 

#### 10.12 Validation Rules 

- Required branding fields present 

- Asset paths exist 

- Export profiles valid 

- Watch folders accessible 

- Font files supported 

- Social media entries correctly formed 

Invalid configuration is highlighted with a suggested fix, not a silent failure. 

#### 10.13 Security 

- Protect configuration files from corruption. 

- Keep version history of major changes. 

Page 35 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

- Allow restoring a previous configuration. 

- Prevent accidental deletion of active settings. 

#### 10.14 Design Principles 

- Centralised 

- Editable 

- Versioned 

- Easy to understand 

- Safe to modify 

- Fully integrated with every engine 

Changing a setting updates future productions automatically without requiring an application restart, where practical. 

_Status: Approved Draft — Version 1.0_ 

Page 36 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### Part III — Engineering & Delivery 

This part turns the architecture into an executable plan: the build order, internal API contracts, testing strategy, coding standards, security posture, and how the application is packaged and shipped. 

Page 37 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 11. Development Roadmap 

#### 11.1 Development Principles 

- Build the foundation first. 

- Keep the application usable after every milestone. 

- Test continuously. 

- Avoid breaking existing functionality. 

- Prioritise automation over feature quantity. 

#### 11.2 Resourcing Assumption 

**_Note:_** _The sprint plan below assumes a small dedicated team (roughly 2–3 engineers) working full time. If you are building this solo or part-time, treat every sprint duration as a multiplier of your actual available hours per week against a standard 40-hour sprint-week — e.g. at 10 hours/week, a "2-week" sprint takes roughly 8 weeks. Re-baseline the roadmap against your real capacity before committing to dates with anyone._ 

#### 11.3 Recommended Build Order Within the Roadmap 

Even though all three templates are in v1.0 scope, build and fully prove the Recorded Lesson pipeline end-to-end (Sprints 1–4, one template only) before adding Teaching Reel and Testimonial Reel support in Sprint 5. This gives you a working, demonstrable product much earlier and surfaces integration problems in the AI/rendering pipeline while the surface area is still small. 

#### 11.4 Sprint Plan 

|**Sprint**|**Durat**<br>**on**|**Focus**|**Objectves**|**Deliverables**|
|---|---|---|---|---|
|Sprint<br>0|1 week|Project<br>Foundaton|Repository structure, dev<br>environment, coding<br>standards, CI-ready structure,<br>confguraton framework|Running desktop shell,<br>inital project structure,<br>setngs loader, logging<br>system|
|Sprint<br>1|2<br>weeks|Media Asset<br>Management<br>|Folder monitoring, media<br>indexing, thumbnail/preview<br>generaton<br>|Media Library, Watch<br>Folder service, preview<br>system|
|Sprint<br>2|2<br>weeks|Workfow<br>Engine|Workfow Orchestrator,<br>Queue Manager, Producton<br>Profles, job scheduling<br>|End-to-end processing<br>pipeline, Queue UI, resume<br>support|
|Sprint<br>3|3<br>weeks|AI Engine|Speech transcripton, capton<br>generaton, silence detecton,<br>speaker detecton, metadata<br>extracton|Local AI processing,<br>confdence scoring, AI<br>analysis reports|
|Sprint<br>4|3<br>weeks|Media Engine|Video processing, audio<br>enhancement, rendering<br>pipeline,export engine|First fully edited videos,<br>export profles, rendering<br>optmisaton|



Page 38 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

|**Sprint**|**Durat**<br>**on**|**Focus**|**Objectves**|**Deliverables**|
|---|---|---|---|---|
|Sprint<br>5|2<br>weeks|Template<br>Engine|Recorded Class, Teaching<br>Reel, Testmonial templates|Producton-ready<br>templates, asset<br>integraton, CTA<br>integraton|
|Sprint<br>6|3<br>weeks|User Interface|Dashboard, Media Library,<br>Preview screen, Setngs,<br>Asset Manager|Complete desktop<br>interface, navigaton, user<br>workfows|
|Sprint<br>7|2<br>weeks|Quality &<br>Optmisaton|Performance tuning, GPU<br>acceleraton, error handling,<br>loggingimprovements|Stable beta version,<br>performance<br>improvements|
|Sprint<br>8|2<br>weeks|Release<br>Candidate|Final testng, documentaton<br>updates, bug fxing,<br>packaging|SME v1.0 Release<br>Candidate|



#### 11.5 Milestones 

- Milestone 1: Core Infrastructure Complete 

- Milestone 2: Media Pipeline Operational 

- Milestone 3: AI Editing Functional 

- Milestone 4: Production Templates Complete 

- Milestone 5: Desktop Application Feature Complete 

- Milestone 6: Stable Release Candidate 

- Milestone 7: Version 1.0 Production Release 

#### 11.6 Version Strategy 

|**Version**|**Meaning**|
|---|---|
|v0.1 Alpha|Internalprototype<br>|
|v0.5 Alpha|Basic editng|
|v0.8 Beta|Feature complete|
|v0.9 RC|Release candidate|
|v1.0|Stablepublic release|
|v1.5(future)|AI improvements|
|v2.0(future)|Cloud features<br>|
|v3.0(future)|Mult-user workspace|



_Status: Approved Draft — Version 1.0_ 

Page 39 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 12. Internal API Reference 

SME's modules communicate only through published interfaces — no module reaches into another module's internal implementation. 

#### 12.1 Module Communication 

Dashboard → Workflow Orchestrator → { Media Engine, AI Engine, Knowledge Engine, Template Engine, Settings Manager, Export Engine } 

#### 12.2 Core Interfaces 

|**Interface**|**Example Methods**|
|---|---|
|Media API|scanFolders(),loadVideo(), generatePreview(), getMediaMetadata()<br>|
|AI API|transcribeAudio(), detectSpeaker(), generateCaptons(), analyseVideo(),<br>scoreQuality()|
|Template API|loadTemplate(),validateTemplate(),applyTemplate(),listTemplates()|
|RenderingAPI|buildTimeline(),renderVideo(),cancelRender(),resumeRender()|
|Export API<br>|exportVideo(),verifyExport(),createVersion()<br>|
|Setngs API|getSetngs(), saveSetngs(), validateSetngs(), backupSetngs(),<br>restoreSetngs()|
|Knowledge API|getProgramme(), getSpeaker(), getCTA(), getBrandAssets()|



#### 12.3 Processing Pipeline 

Media Scanner → Workflow Orchestrator → AI Analysis → Template Selection → Media Processing → Rendering → Quality Review → Export Every stage receives structured data and returns a structured result. 

#### 12.4 Error Contract 

Every API response includes: status, result, error (if any), timestamp, processing duration, and confidence score where applicable. 

#### 12.5 Versioning 

Internal APIs follow semantic versioning (e.g. v1.0.0, v1.1.0, v2.0.0). Breaking changes require a major version increment. 

_Status: Approved Draft — Version 1.0_ 

Page 40 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 13. Testing Guide 

Every new feature must include corresponding automated and manual tests before release. 

#### 13.1 Testing Levels 

|**Level**|**Purpose**<br>|**Examples**<br>|
|---|---|---|
|Unit<br>|Individual components in isolaton|Folder scanner, capton generator, export<br>naming,metadataparser,setngs validaton|
|Integraton|Modules working together<br>correctly<br>|AI → Template Engine; Template → Media<br>Engine; Media Engine → Export Engine;<br>Setngs → Rendering; Knowledge Engine →<br>Workfow<br>|
|End-to-End|Complete producton workfows<br>|Raw video → detecton → AI processing →<br>rendering→ export → edited video|
|Performance|Processing speed, rendering tme,<br>memory, GPU utlisaton, batch<br>efciency|—|
|Stress|Behaviour under heavy load|100 queued videos, large course libraries,<br>longrecordings,simultaneous renders|
|Recovery|Recovery from failure states|Unexpected shutdown, power failure, disk<br>full,corrupted assets,interrupted rendering|



#### 13.2 Test Data 

- Recorded lessons 

- Teaching reels 

- Testimonial reels 

- Corrupted media 

- Large media files 

- Varied resolutions and orientations 

#### 13.3 Acceptance Criteria 

A feature is complete only when: functional tests pass, integration tests pass, performance meets target, documentation is updated, and no critical regressions are introduced. 

#### 13.4 Regression Testing (before every release) 

- Run the full automated test suite. 

- Reprocess a standard benchmark media library. 

- Compare output against expected quality and metadata. 

- Verify templates, CTAs, branding, and export profiles remain correct. 

Page 41 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

#### 13.5 Quality Metrics to Track 

- Test coverage 

- Defect rate 

- Mean render time 

- AI confidence trends 

- Crash rate 

- Export success rate 

- Production recovery success rate 

#### 13.6 Release Gates 

A release cannot progress unless: no critical defects remain, high-priority defects are resolved or explicitly accepted, core workflows complete successfully, and documentation matches implemented behaviour. 

_Status: Approved Draft — Version 1.0_ 

Page 42 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 14. Coding Standards 

This chapter keeps the codebase consistent, maintainable, testable, and scalable across contributors, including future ones who never spoke to the original author. 

#### 14.1 Development Principles 

- Readability over cleverness 

- Modularity over duplication 

- Simplicity over unnecessary complexity 

- Composition over inheritance where appropriate 

- Non-destructive processing 

- Automation where practical 

#### 14.2 Project Structure 

selfcraft-media-editor/ app/ ui/ core/ workflow/ ai/ media/ templates/ knowledge/ settings/ assets/ export/ logging/ tests/ unit/ integration/ performance/ docs/ config/ plugins/ scripts/ 

Each directory has a single responsibility. 

#### 14.3 Naming Conventions 

|**Element**|**Conventon**|**Example**<br>|
|---|---|---|
|Files|lowercase_with_underscores.py|media_engine.py,workfow_orchestrator.py<br>|
|Classes|PascalCase|MediaEngine,CaptonRenderer,|



Page 43 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

|**Element**|**Conventon**|**Example**<br>|
|---|---|---|
|||WorkfowOrchestrator|
|Functons|descriptve_snake_case()|load_video(), detect_speaker(),<br>export_video()|
|Variables|meaningful names|current_template — not tmp|
|Constants|UPPERCASE_WITH_UNDERSCOR<br>ES|DEFAULT_EXPORT_PROFILE|



#### 14.4 Code Organisation 

- Each module performs one primary responsibility. 

- Minimise dependencies. 

- Expose a clear public interface. 

- Avoid circular references. 

#### 14.5 Error Handling 

Never suppress exceptions silently. Every recoverable error must be logged, produce a user-friendly message, suggest corrective action where possible, and preserve original media. 

#### 14.6 Logging Standards 

Every major action creates a structured log entry: timestamp, module, operation, status, duration, error (if applicable). Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. 

#### 14.7 Documentation Standards 

Every public class and function documents its purpose, parameters, return values, exceptions, and usage notes where helpful. Architecture changes must be reflected in documentation before release. 

#### 14.8 Code Quality Gate (before merging) 

- Formatting passes. 

- Static analysis passes. 

- Unit tests pass. 

- Integration tests pass. 

- No unused code or dependencies. 

- No hard-coded branding or file paths. 

#### 14.9 Dependency Management 

- Keep third-party libraries to the minimum necessary. 

- Document every dependency and its purpose. 

- Prefer actively maintained libraries. 

- Pin dependency versions for reproducible builds. 

Page 44 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

#### 14.10 Version Control 

Git with a standard branching strategy: main (stable releases), develop (integration), feature/*, bugfix/*, release/*, hotfix/*. Commit messages are descriptive — e.g. "feat(media): add silence removal pipeline". 

_Status: Approved Draft — Version 1.0_ 

Page 45 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 15. Security & Privacy 

This chapter defines how SME protects user data, media assets, and application integrity while maintaining an offline-first design. 

#### 15.1 Security Principles 

- Privacy by default 

- Least privilege 

- Defence in depth 

- Non-destructive editing 

- Explicit user consent for any external communication 

#### 15.2 Local Data Protection 

- Media remains on the user's device by default. 

- Processing occurs locally whenever practical. 

- No uploads occur without user approval. 

#### 15.3 Asset Integrity 

- Never overwrite original files. 

- Verify file integrity before processing. 

- Validate exported files after rendering. 

- Preserve metadata where appropriate. 

#### 15.4 Permissions 

SME requests only what its configured watch folders and selected features require: user-selected media folders, asset folders, export folders, and configuration storage. 

#### 15.5 Configuration Security 

- Validated before use. 

- Backed up before major changes. 

- Corruption is detected. 

- Rollback to a previous version is supported. 

#### 15.6 Backup Strategy 

Users can back up settings, templates, assets, production profiles, the knowledge database, and logs. Backups are restorable from within SME. 

Page 46 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

#### 15.7 Encryption 

- Encrypt sensitive local configuration if credentials or tokens are introduced in a future feature. 

- Use secure transport (HTTPS) for any optional online service. 

- Never store secrets in plain text. 

#### 15.8 Personal Data in Testimonial Content 

**_Note:_** _Testimonial videos capture participants' real names and personal stories via speech recognition — this is personal data, distinct from general application telemetry. Before shipping the Testimonial Reel template, define: what consent is obtained from participants before recording; how long extracted names/transcripts are retained after a video is edited; how a participant can request their testimonial be removed; and whether transcripts are purged along with the temporary AI processing memory described in Section 5.7, or retained longer for editing history. This is a governance decision for SelfCraft Academy to make explicitly, not something the software should default silently._ 

#### 15.9 Telemetry 

SME does not collect analytics by default. If optional telemetry is introduced in future, it must be opt-in, clearly explain what data is collected, and be disableable at any time. 

#### 15.10 Logging & Audit 

Security-relevant events are logged: failed configuration validation, asset integrity failures, unexpected processing errors, backup/restore operations. Logs avoid exposing sensitive information unnecessarily. 

#### 15.11 Future Security (Phase 2+) 

- Digital signatures for plugins 

- Role-based access for team editions 

- Secure cloud synchronisation 

- Encrypted workspace backups 

_Status: Approved Draft — Version 1.0_ 

Page 47 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### 16. Deployment Guide 

This chapter defines how SME is built, packaged, distributed, installed, updated, and maintained. 

#### 16.1 Supported Platforms 

Version 1.0 targets Windows 10 and Windows 11. macOS and Linux are future targets — see Section 1.5. 

#### 16.2 Build Process 

Development Build → Automated Tests → Static Analysis → Packaging → Release Candidate → Production Release 

Every release must pass the quality gates defined in Chapter 13. 

#### 16.3 Installation 

- Verify system requirements. 

- Install required runtime components. 

- Create application shortcuts (optional). 

- Initialise configuration folders. 

- Preserve user settings during upgrades. 

#### 16.4 System Requirements 

||**Minimum**|**Recommended**|
|---|---|---|
|OS|64-bit Windows 10/11|64-bit Windows 10/11|
|RAM|8 GB|16 GB or more|
|CPU|Quad-core|Mult-core|
|GPU|Optonal|Dedicated GPU with hardware video<br>encoding|
|Storage|SSD recommended, sufcient free<br>space for mediaprocessing|NVMe SSD|



#### 16.5 Updates 

- Manual update checks. 

- Optional automatic update notifications. 

- Release notes for every version. 

- Updates never overwrite user-created assets or settings without a migration path. 

#### 16.6 Release Packaging 

- Application binaries 

- Default templates 

- Default assets 

Page 48 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

- Configuration schema 

- Documentation 

- Licence information 

- Changelog 

#### 16.7 Versioning 

Semantic Versioning — Major: breaking architectural changes. Minor: new features. Patch: bug fixes and performance improvements. Example progression: v1.0.0 → v1.1.0 → v1.1.2 → v2.0.0. 

#### 16.8 Rollback 

- Restore the previous application version where practical. 

- Preserve user settings. 

- Preserve media libraries. 

- Preserve production logs. 

#### 16.9 Deployment Checklist 

- All automated tests pass. 

- Documentation is current. 

- Assets validated. 

- Templates validated. 

- Security review completed. 

- Performance benchmarks met. 

- Release package verified on a clean system. 

#### 16.10 Future Deployment (Phase 2+) 

- Automatic update service 

- Portable edition 

- Enterprise installer 

- Microsoft Store package 

- macOS installer 

- Linux packages (AppImage, Flatpak, or native) 

_Status: Approved Draft — Version 1.0_ 

Page 49 of 50 

SelfCraft Media Editor (SME) — Specification v1.0 

### Appendix A — Document Summary 

This specification consolidates the full SME foundation architecture into sixteen chapters across three parts: 

|**Part**|**Chapters**|**Covers**<br>|
|---|---|---|
|Part I|1–2|Vision, product strategy,and functonal requirements<br>|
|Part II|3–10|Sofware architecture, workfow, AI engine, knowledge engine,<br>media engine,template engine,UI/UX,and setngs<br>|
|Part III|11–16|Development roadmap, internal API reference, testng, coding<br>standards,security&privacy,and deployment|



Section 1.5 is the binding scope statement for Version 1.0. If any other chapter appears to expand that scope, Section 1.5 governs. 

Page 50 of 50 

