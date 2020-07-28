# Provides base class for selenium-based webscrapers to streamline development and deployment to AWS.

# Setup
  1. Create virtual environment: `mkvirtualenv -p /usr/local/bin/python3.6 selenium-aws-scraper`
  2. Download requirements.txt.
  3. Download chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads. Download version that matches your Google Chrome version.
  4. Configure you AWS access key/secret key locally.
  4. Ensure user has role/policy to have lambda/s3 access.