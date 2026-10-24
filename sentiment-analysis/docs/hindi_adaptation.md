### Hindi support in the app

The app now routes Hindi and Hinglish inputs to **Hindi lexicon + negation**. The dictionary covers Devanagari words and common Romanized variants. It recognizes खराब as negative and अच्छा as positive, reverses sentiment for nearby negation, and strengthens sentiment for words such as बहुत. English sentiment words within mixed-language inputs use VADER's word lexicon.

For `यह सामान बहुत खराब है।`, the adapted result is **negative, -0.7579**. For `Product accha nahi hai`, it is negative. Factual inputs without sentiment words receive zero. The original VADER/TextBlob outputs remain available under Compare original English tools and in the unchanged 36-input benchmark.

The implementation is in `sentiment_lab/hindi.py` and `data/hindi_lexicon.json`. Token scores are summed and normalized as `s / sqrt(s*s + 15)`. Negation changes a matched term's sign with a 0.74 factor; intensifiers multiply it by 1.5. The selected label uses the same +/-0.05 boundaries.

All 12 coursework Hindi/Hinglish checks pass with this dictionary. Their words were available during development, so these are illustrative checks rather than an independent estimate of accuracy. Sarcasm, unfamiliar words and complex negation still need broader evaluation. Automatic routing uses script and dictionary matches; the language selector lets the user override it.

### Resources and their purpose

| Resource | Concrete use | Caveat |
|---|---|---|
| A consented, labeled Hindi and Hinglish review corpus | Supervised sentiment training and held-out evaluation | Build domain coverage; remove identifying details and duplicates |
| Hindi language corpus and a pretrained encoder such as [IndicBERT](https://indicnlp.ai4bharat.org/pages/indic-bert/) | Initialize a classifier before fine-tuning on sentiment labels | Specialize the encoder using sentiment-labeled examples |
| Hindi sentiment lexicon with native-speaker ratings | Transparent baseline covering अच्छा, खराब, पसंद and domain phrases | Context, negation and slang can reverse dictionary meanings |
| Token language identification and Unicode-aware tokenization | Preserve Hindi, English, emoji, URLs and punctuation separately | Script identification alone cannot recognize Romanized Hindi |
| Hindi POS tagging and dependency analysis | Optional error analysis of negation scope and modifiers | A transformer baseline does not require POS tagging |
| [IndicXlit](https://github.com/AI4Bharat/IndicXlit) | Candidate Roman-to-Devanagari normalization | Retain original text; transliteration is ambiguous |
| [IndicTrans2](https://github.com/AI4Bharat/IndicTrans2) | Optional translation-to-English baseline | Translation can change sentiment, idioms or sarcasm; evaluate separately |

### Steps for extending the implementation

1. Collect a proposed pilot of 3,000 consented reviews, targeting 1,000 each in Devanagari Hindi, Romanized Hindi and mixed Hindi-English. Include products, delivery, food and social posts. This is a collection target, not an existing dataset.
2. Write a sentiment annotation guide with positive, negative and neutral labels. Mark sarcasm, mixed aspects, regional expressions and ambiguous cases as separate attributes. Have two Hindi speakers independently label every item and a third adjudicate disagreements. Report agreement before adjudication.
3. Normalize Unicode to NFC, mask identifying details and retain negation, emoji, repeated letters and punctuation. Do not remove stopwords blindly: नहीं, मत and ना can change sentiment. Store both original and normalized forms.
4. Group near-duplicates, conversation threads and reviews from the same source before a stratified 70/15/15 training, validation and test split. Prevent leakage across groups. The 36 coursework examples remain diagnostic examples, not training data.
5. Extend and validate the implemented Hindi lexicon and negation rules. Fine-tune an IndicBERT sentiment classifier on the same training split. Compare optional transliteration and translation pipelines as separate experiments. Never replace the original-text test set with translated text.
6. Choose hyperparameters and any abstention threshold using validation data only. Freeze the test set. Evaluate accuracy, per-class precision/recall/F1, macro F1 and confusion matrices by script, dialect, domain and code-switching level.
7. Add human review for unsupported dialects, ambiguous mixed sentiment and uncertain predictions. Retain an audit trail of model version and preprocessing. Roll out only after native-speaker error review and validation against the baseline.

### Socio-linguistic challenges

| Challenge | Example or consequence | Proposed response |
|---|---|---|
| Romanized spellings | accha, achha, acha; nahi, nahin | Cover spelling variants and compare normalization against original text |
| Code-switching | Product accha nahi hai | Identify token language and learn Hindi negation over an English product noun |
| Regional and social variation | mast, zabardast, paisa vasool vary with usage | Include regional speakers and domain context in annotation and error review |
| Scripts and mixed scripts | Devanagari, Latin and mixtures | Tokenize Unicode safely and publish metrics for each script group |
| Sarcasm and politeness | Praise words may accompany a complaint | Annotate pragmatic intent and retain preceding conversational context where consent permits |
| Mixed aspects | Good camera but poor battery | Record aspect labels or flag a mixed judgement instead of hiding the tradeoff |
| Hindi varieties | Regional Hindi and contact varieties differ | Report subgroup sample sizes; avoid claiming coverage of every dialect |

### How improvement would be demonstrated

Compare all candidate pipelines on the same untouched test IDs, report subgroup support and confidence intervals, and inspect false neutrals in Hindi. A useful model must improve sentiment recall beyond an all-neutral baseline while preserving performance on factual inputs. The current adapter's measured illustrative checks are saved separately in `results/hindi_adapter.json`. A new held-out corpus is needed to assess broader accuracy.
