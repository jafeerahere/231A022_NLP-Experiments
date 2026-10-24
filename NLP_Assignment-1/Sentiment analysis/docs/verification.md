# Verification record

Verified locally on 24 October 2026 with Python 3.12.14.

- `python -m scripts.evaluate` ran VADER 3.3.2 and TextBlob 0.20.1 on all 36 original inputs.
- `python -m pytest -q` passed all 33 checks after adding Hindi/Hinglish scoring and simplifying the result screen.
- `python -m scripts.evaluate_hindi` passed all 12 illustrative Hindi/Hinglish checks; outputs and the dictionary checksum are saved separately from the original benchmark.
- `python -m scripts.build_notebook` executed all seven code cells without saved error outputs.
- `python -m scripts.build_report` generated the updated Markdown report and nine-page PDF, including a Rizvi College of Engineering cover, department heading, college logo, and the Hindi adapter screenshot and scoring method.
- The PDF was rendered with Poppler and visually checked after the update.
- The provenance checksum matches the input CSV.
- The app was opened in the browser. EN01 and DV01 were run, and input/output screenshots were captured. The comparison dashboard was also captured. After the update, the supplied Hindi complaint returned negative at -0.7579 using the separately labeled Hindi adapter, and a new screenshot was captured.
- Existing experiment notebooks were retained. The root README was updated and a scoped GitHub Actions workflow was added.
- `git diff --check` passed for the prepared changes.

These checks verify execution and consistency. The reference annotations and general accuracy on real-world Hindi or social-media data need broader validation. Remote test runs are available in the repository's GitHub Actions page.
