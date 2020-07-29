# Provides base class for selenium-based webscrapers to streamline development and deployment to AWS.

# Setup
  1. Create virtual environment: `mkvirtualenv -p /usr/local/bin/python3.8 selenium-aws-scraper`. Note: this program does take advantage of the walrus operation `:=`, which was introduced in Python 3.8.
  2. Run `pip install -r requirements/dev-requirements.txt`.
  3. Download chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads. Download version that matches your Google Chrome version. Store the path of the chromedriver to an env variable `CHROMEDRIVER_PATH`.
  4. Run `pre-commit install` to ensure your pre-commit hooks are installed locally.
  5. Add `pytest` to your `.git/hooks/pre-push`.
  4. Configure you AWS access key/secret key locally.
  4. Ensure user has role/policy to have lambda/s3 access.