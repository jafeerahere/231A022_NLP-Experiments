# AIDS_Sem7_NLP_Experiment01: Formulate Mini Project Problem Statement

**Name:** Jafeera Ansari  
**UIN:** _To be filled_  
**Subject:** CSDOL7011 – Natural Language Processing  
**Performed On:** _To be filled_

## Aim

Identify a real-world NLP problem, such as sentiment analysis or chatbot development, and frame a detailed problem statement for a mini project.

## Pre-Lab Questions

**1. What is a real-world problem that can be addressed using NLP techniques? Provide some examples.**

NLP can address problems involving the understanding, analysis, and generation of human language. Examples include customer-review sentiment analysis, spam detection, chatbots, machine translation, and automatic text summarization. RecallAI addresses the effort students spend converting lengthy lecture notes into concise revision material and practice questions.

**2. Why is it important to clearly define the problem statement before starting an NLP project?**

A clear problem statement establishes the users, goals, data requirements, project boundaries, expected outputs, and evaluation criteria. It prevents scope creep and helps developers choose techniques appropriate to the problem and available time.

**3. Choose a potential NLP application. What are the expected benefits of implementing this application?**

The selected application is **RecallAI — Intelligent Notes-to-Quiz Generator**. Its expected benefits are faster preparation of revision materials, concise summaries, easier identification of important concepts, automatically generated practice questions, and support for active recall. These benefits are project goals, not experimentally verified outcomes at this stage.

## Problem Statement

**Title: RecallAI — Intelligent Notes-to-Quiz Generator Using Natural Language Processing**

Students frequently receive lengthy lecture notes and educational passages but must manually identify key ideas, write summaries, and prepare questions for self-assessment. This preparation takes time and may result in important concepts being missed. Conventional digital note-taking tools store content but do not necessarily transform it into structured, interactive revision materials. RecallAI proposes an NLP-based application that processes student-provided educational text and produces concise summaries, important keywords, flashcards, and practice questions. Generated answers will be checked against the source notes to reduce unsupported content. The project focuses on making revision preparation easier while evaluating the factual accuracy and usefulness of the generated material.

**Objectives**

1. Accept English educational text and TXT notes as input.
2. Clean and segment input text for downstream NLP processing.
3. Generate concise summaries that preserve key concepts.
4. Extract important keywords and concepts from the notes.
5. Generate flashcards, multiple-choice questions, and short-answer questions with source-grounded answers.
6. Evaluate summary quality, question relevance, answer correctness, and processing time.

**Scope**

- *In scope:* English educational text, pasted text and TXT files, preprocessing, summarization, keyword extraction, flashcard generation, basic quiz generation, source-based answer checking, and evaluation on a small sample dataset.
- *Out of scope:* handwritten-note recognition, video/audio processing, multilingual support, training a large language model from scratch, full learning-management features, and automated grading of essays.

**Target Audience:** School and college students, competitive-examination aspirants, and teachers preparing supplementary revision material.

**Data Requirements:** Readable English lecture notes, educational passages, and appropriately licensed open educational resources. A small manually curated evaluation set will contain source passages, reference summaries, key concepts, and reviewed question-answer pairs. Preprocessing includes text cleaning, sentence segmentation, tokenization where needed, and splitting long documents into manageable sections. Personal or copyrighted notes should only be used with appropriate permission.

**Challenges & Assumptions:** Challenges include ambiguous or poorly structured notes, loss of important information during summarization, irrelevant questions, incorrect or unsupported generated answers, model input-length limits, and limited computational resources. The project assumes readable English text, sufficiently informative source material, and access to suitable pretrained models. Generated content is not assumed to be correct without evaluation.

**Evaluation Metrics:** ROUGE and BERTScore for comparison with reference summaries; human-reviewed question relevance, answer correctness, factual consistency with source notes, and clarity; plus average processing time. Evaluation will use a small held-out set, with results reported only after implementation and testing.

**Tools & Techniques:** Python; NLTK or spaCy for text preprocessing; Hugging Face Transformers and pretrained models for summarization and question generation; KeyBERT or a comparable keyword-extraction approach; Streamlit for the prototype interface; pandas for evaluation data; Git and GitHub for version control. Specific models may be adjusted based on available computing resources.

**Impact & Significance:** RecallAI aims to reduce repetitive preparation work and make active-recall practice more accessible. Its contribution is an integrated workflow that transforms unstructured study notes into several revision formats while treating factual grounding and evaluation as explicit design requirements. Any improvement in study efficiency or learning outcomes would require separate user testing and is not claimed by this experiment.

**Deliverables:** A proposed functional application prototype, text preprocessing module, summarization and keyword-extraction modules, flashcard and quiz generator, small evaluation dataset, evaluation report, technical documentation, and final presentation. These are planned deliverables rather than completed outputs of Experiment 1.

## Brief Theory

A well-defined NLP problem statement specifies the problem description, objectives, scope, target audience, data requirements, challenges and assumptions, evaluation metrics, tools and techniques, impact and significance, and deliverables. For RecallAI, **text summarization** condenses educational content, **keyword extraction** identifies important concepts, and **question generation** converts relevant source material into practice prompts. Source-grounded answer checking and human evaluation are necessary because generated text can omit facts or introduce unsupported information. Clearly defining these elements makes the mini project focused, feasible, and measurable.

## Implementation Explanation

No application code was implemented in Experiment 1. This experiment involved selecting a real-world educational NLP problem and documenting its requirements and proposed solution. The planned pipeline is:

`Student notes → Text preprocessing → Summarization and keyword extraction → Question and answer generation → Source-grounding checks → Flashcards and quizzes → Student review`

A later implementation will use pretrained NLP models and a lightweight web interface. Model outputs will be evaluated against reference material and human-reviewed samples before performance claims are made.

## Post-Lab Questions

**1. What are the key challenges that may arise when developing your chosen NLP solution?**

Major challenges include finding suitable educational passages and reference questions, handling ambiguous notes, preserving essential information in summaries, generating relevant questions, preventing hallucinated answers, and processing long documents within hardware and model limits. Human review is needed to assess whether outputs are educationally useful and supported by the notes.

**2. How would you determine the scope of your mini project to ensure it is achievable within a limited timeframe?**

The first prototype will accept English pasted text and TXT files and focus on four features: summarization, keyword extraction, flashcards, and basic quizzes. Pretrained models will reduce training requirements. Handwriting recognition, multilingual processing, video input, and advanced grading will be excluded. A small evaluation dataset and clear metrics will make progress measurable.

## Results

A complete problem statement was formulated for **RecallAI — Intelligent Notes-to-Quiz Generator**, covering the problem description, objectives, in-scope and out-of-scope features, target audience, data requirements, challenges and assumptions, evaluation metrics, tools and techniques, impact, and deliverables. A proposed processing pipeline and evaluation plan were also documented. No software implementation, model accuracy, or user-study results were produced in this experiment.

## Conclusion

RecallAI addresses the practical problem of converting lengthy educational notes into useful revision materials. The proposed NLP pipeline combines summarization, keyword extraction, and question generation to produce summaries, flashcards, and practice questions, with source-grounding checks and evaluation planned to assess reliability. Experiment 1 successfully defines a feasible project scope and measurable objectives; implementation and validation remain future project work.

**COs Covered:** CO5 – Apply NLP techniques to design real-world NLP applications such as machine translation, sentiment analysis, text summarization, information extraction, and question-answering systems.

## References

- Rizvi College of Engineering, CSDOL7011: Natural Language Processing – Lab Manual, Experiment No. 1.
- [Hugging Face Transformers documentation](https://huggingface.co/docs/transformers/index).
- [spaCy documentation](https://spacy.io/usage).
- [NLTK documentation](https://www.nltk.org/).
- [Streamlit documentation](https://docs.streamlit.io/).
