# Implements an OOO approach to effeciently build selenium web scrapers.

# Features
  1. Leverages Python3.8 (e.g. function types and the newly introduced walrus `:=` operator).
  2. Uses chromedriver (and not Firefox).
  3. Extends and customizes standard wait functions from the selenium library.
  4. Uses `isort` and `black` linters in pre-commit hooks to organize imports and Python code respectively to adhere to PEP 8 standards (i.e. runs linter before each commit to Github). 
  5. Runs `pytest` before each push to Github.
  6. Ensures JSON logging to stdout.

# Setup
  1. Create virtual environment: `mkvirtualenv -p /usr/local/bin/python3.8 selenium-aws-scraper`. Note: this program does take advantage of features introduced in Python 3.8.
  2. Download relevant dependencies: `pip install -r requirements/dev-requirements.txt`.
  3. Download chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads. Ensure that you are downloading the version that matches your Google Chrome version. Store the path of the download chromedriver to the env variable: `CHROMEDRIVER_PATH`.
  4. Ensure you have executable permissions on the chromedriver: `chmod +x $(CHROMEDRIVER_PATH)`.
  5. Run `pre-commit install` to ensure your pre-commit hooks are installed locally. Ensure `--config` in your `.git/hooks/pre-commit` is pointing to `config/.pre-commit-config.yaml`.
  6. Add `pytest` to your `.git/hooks/pre-push`.
