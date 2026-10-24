# Presentation and viva notes

## A five-minute demonstration

1. Open the app and show EN01. Both tools label the praise positive. Explain that the displayed values are sentiment scores, not confidence.
2. Select NG01 and press Analyze. 'Not good' becomes negative. Explain why removing stopwords would damage this sentence.
3. Select SA01 and press Analyze. Compare the positive predictions with the negative reference reading. Explain that positive words can be sarcastic in context.
4. Select DV03 and run it. Show the Hindi adapter's negative result and the matched word खराब. Select HI04 to show negation in Romanized Hindi. Expand Compare original English tools to show why the English-only dictionaries returned zero.
5. Open Compare 36 inputs. Show accuracy, the four disagreements and confusion matrices. Filter Hindi and Any tool incorrect. Four of six Hindi inputs are wrong; the two factual inputs happen to be neutral.
6. Open Hindi sentiment. Discuss resources, two-annotator labeling, script handling, negation and evaluation on an untouched test set. Explain the implemented lexicon rules and the resources for extending coverage.

## Likely questions

**Why VADER and TextBlob?** Both are real, reproducible NLP tools with different scoring implementations. They run on a laptop without API access, so the same inputs can be compared directly.

**What is VADER?** Valence Aware Dictionary and sEntiment Reasoner. It combines a sentiment lexicon with rules that account for signals such as punctuation, capitalization, modifiers and negation. The compound score is normalized to -1 through +1.

**What is TextBlob doing here?** Its default English PatternAnalyzer supplies polarity and subjectivity. This project maps polarity into three labels using its declared threshold rule.

**How does Hindi scoring work?** A Hindi/Hinglish dictionary supplies word valences. Nearby negation reverses sentiment, intensity words strengthen it, and a normalization formula maps the sum to -1 through +1. The interface labels this method separately from VADER and TextBlob.

**What is the dataset?** Thirty-six illustrative examples authored for the project with AI assistance. They are six examples per category and have intended sentiment labels. They are not independent real-world test data.

**Why is TextBlob's accuracy higher?** It gets two more examples right on this set. That is too little evidence for a general ranking. It handles the restaurant complaint and the neutral Diwali schedule better in these outputs.

**Why does SA03 display 0.0500 but say neutral?** The raw score is 0.04999999999999999. Classification uses that full-precision value, which is just below 0.05. The displayed value is rounded. This is a floating-point boundary effect; either label still misses the intended negative sentiment.

**What does the confusion matrix mean?** Each row is the reference class and each column is the predicted class. Diagonal counts are correct. For VADER, six negative references become positive and six become neutral.

**Why macro F1?** It weights each of the three classes equally instead of letting the larger negative class dominate. F1 is the harmonic mean of precision and recall. Zero-support class values are set to zero, which matters if looking at a subgroup.

**Is neutral always a factual statement?** No. An English lexicon can return zero when it recognizes no sentiment-bearing words in Hindi. That makes praise and criticism look neutral too.

**Why not remove punctuation or translate everything?** Punctuation is useful to VADER, and the assignment asks for the same input in both tools. Translation introduces another system and can change meaning. It should be compared as a separate pipeline.

**What would improve Hindi performance?** A Hindi/Hinglish labeled corpus, native-speaker annotation, normalization that preserves negation and slang, and a fine-tuned Hindi-capable encoder. Compare it fairly with lexicon and optional translation baselines.

**What should you say about authorship?** The implementation, report and illustrative data were prepared with AI assistance. The predictions and screenshots are actual local runs. Explain the choices and limitations in your own words.
