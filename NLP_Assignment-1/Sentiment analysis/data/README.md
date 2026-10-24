# Challenge set

`challenge_set.csv` contains 36 project-authored illustrative inputs, six in each of English, Negation, Sarcasm, Indian English, Hinglish and Hindi. They are synthetic examples written for this coursework with AI assistance. They are not scraped tweets, customer records or a published benchmark.

Each record includes a stable ID, original text, reference sentiment, category, language description, intended meaning and linguistic challenge. Reference labels were assigned while preparing the examples, before running the comparison. No independent annotation, native-speaker review or agreement study has been performed. Hindi meanings are glosses for explanation; the tools receive only the original `text` field.

The reference distribution is 17 negative, 8 neutral and 11 positive. All six sarcasm cases are negative. The test set deliberately contains difficult cases; accuracy is descriptive for these examples only. An always-negative predictor gets 17/36, or 47.2%. An always-neutral predictor gets 8/36, or 22.2%.

Negated dislike in NG04 is labeled weak positive, although neutral is defensible. NG05 and NG06 use the final product-related clause for the overall sentiment; a mixed label is also defensible. Such ambiguity belongs in the interpretation of the result. No examples were relabeled or removed after inspecting predictions.

The Hindi and Hinglish factual examples test whether zero sentiment is appropriate. Their correct neutral predictions do not demonstrate Hindi comprehension. Both original tools return neutral for every Hindi and Hinglish example in this set. The separate Hindi adapter was developed afterwards and records its own checks in results/hindi_adapter.json.

The original comparison uses both tools' distributed English lexicons and rules. Inputs preserve punctuation, case, stopwords and script. No translation, transliteration or spelling correction is used. Only outer whitespace is stripped for custom inputs.

Columns:

| Column | Meaning |
|---|---|
| id | Unique stable example identifier |
| text | Unchanged input shared by both tools |
| gold_label | Author-assigned intended overall sentiment |
| category | Diagnostic group, not automatically detected language |
| language | Description assigned during dataset construction |
| meaning | English explanation of the intended reading |
| challenge | Expected linguistic difficulty, not proof of an observed model error |

Original examples are released under CC0-1.0. Package code and lexicons remain subject to their respective upstream licenses. See [VADER](https://github.com/cjhutto/vaderSentiment) and [TextBlob](https://github.com/sloria/TextBlob).
