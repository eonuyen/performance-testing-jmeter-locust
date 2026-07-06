# Performance Testing with JMeter and Locust

A performance testing portfolio project demonstrating the same e-commerce search flow with two different load testing tools:

- Apache JMeter
- Locust

The project covers HTTP load generation, CSV-based test data, response validation, HTML content inspection, realistic wait times, and performance report generation.

## Project Scope

Both implementations currently target an e-commerce search flow.

### Tested Flow

1. Open the home page.
2. Verify that the server returns a successful response.
3. Search for a product keyword.
4. Verify that the search request is successful.
5. Validate that the search result page contains expected content.
6. Verify that product-related elements are present.

> This repository is intended for demonstration and portfolio purposes.  
> Do not execute high-volume tests against third-party or production systems without explicit authorization.

## Technology Stack

### JMeter

- Apache JMeter 5.6.3
- HTTP Request Samplers
- CSV Data Set Config
- HTTP Header Manager
- HTTP Cookie Manager
- Response Assertions
- CSS Selector Extractor
- JSR223 Assertion with Groovy
- Uniform Random Timer
- HTML dashboard reporting

### Locust

- Python
- Locust 2.43.4
- BeautifulSoup 4
- Gevent
- HTTP user simulation
- HTML content validation
- HTML and CSV reporting
  
## Project Structure

```text
performance-testing-jmeter-locust/
├── jmeter/
│   ├── data/
│   │   └── search-data.csv
│   ├── test-plans/
│   │   └── *.jmx
│   ├── results/
│   └── reports/
│       └── sample-report/
├── locust/
│   ├── locustfile.py
│   ├── requirements.txt
│   └── reports/
│       └── sample-report/
├── .gitignore
└── README.md
```

## JMeter Implementation

The JMeter test plan includes:

- HTTPS request configuration
- 10-second connection and response timeouts
- Browser-like HTTP headers
- Cookie management
- CSV-based search keywords
- Home page request executed once per virtual user
- Search request using the `/arama` endpoint
- HTTP status code validation
- Search keyword validation in the response body
- Product element extraction with a CSS selector
- Groovy assertion to verify that products were found
- Random wait time between requests
- Summary and result listeners

### Test Data

Search keywords are stored in:

jmeter/data/search-data.csv

Current examples:
telefon
laptop
kulaklık

The test plan reads each value into the `${keyword}` variable.

## Running the JMeter Test

### Prerequisites

Install:

- Java
- Apache JMeter 5.6.3

Verify the installation:

java -version
jmeter -v

### Run in JMeter GUI

Use the graphical interface only for reviewing or debugging the test plan:

```bash
TEST_PLAN=$(find jmeter/test-plans -name "*.jmx" | head -n 1)
jmeter -t "$TEST_PLAN"
```

### Run in Non-GUI Mode

Performance tests should normally be executed in non-GUI mode.

From the repository root:

```bash
rm -rf jmeter/results jmeter/reports/sample-report

mkdir -p jmeter/results
mkdir -p jmeter/reports/sample-report

TEST_PLAN=$(find jmeter/test-plans -name "*.jmx" | head -n 1)

jmeter \
  -n \
  -t "$TEST_PLAN" \
  -JcsvFile=jmeter/data/search-data.csv \
  -l jmeter/results/results.jtl \
  -e \
  -o jmeter/reports/sample-report
```

## Locust Implementation

The Locust scenario includes:

- An `HttpUser` implementation
- A configurable wait time between 1 and 3 seconds
- Browser-like request headers
- Home page execution in `on_start`
- URL-encoded product search requests
- HTTP status code inspection
- HTML parsing with BeautifulSoup
- Search keyword validation
- Search page indicator validation
- Product and listing element detection
- Single-user debug execution support

The current Locust scenario uses:

```python
host = "https://www.n11.com"
wait_time = between(1, 3)
```

## Running the Locust Test

### Create a Virtual Environment

From the repository root:

```bash
cd locust

python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run with the Web Interface

```bash
python -m locust -f locustfile.py
```

Then open:

```text
http://localhost:8089
```

### Run in Headless Mode

The following command runs a low-volume sample execution and generates HTML and CSV reports:

```bash
mkdir -p reports/sample-report

python -m locust \
  -f locustfile.py \
  --headless \
  --users 1 \
  --spawn-rate 1 \
  --run-time 30s \
  --html reports/sample-report/report.html \
  --csv reports/sample-report/locust
```

## Running a Single Locust User for Debugging

The `locustfile.py` file supports direct single-user debugging:

```bash
python locustfile.py
```

This mode prints request status codes, response samples, and search page validation results.

## Reports

Generated execution data is ignored by Git by default.

Only files placed under the following folders are intended to be committed as portfolio examples:

```text
jmeter/reports/sample-report/
locust/reports/sample-report/
```

This prevents local execution reports from unnecessarily increasing the repository size.

## Responsible Usage

Load and performance tests can generate significant traffic.
Before running a test:

- Obtain authorization from the system owner.
- Prefer a staging, test, mock, or locally controlled environment.
- Start with a very small number of users.
- Define acceptable traffic and duration limits.
- Stop the test if the target system becomes unstable.
- Never use this project to disrupt a third-party service.

## Planned Improvements

- Move the target host to an external configuration
- Add configurable user count and run duration
- Mark Locust content validation failures in Locust statistics
- Add response-time and failure-rate thresholds
- Add automated performance smoke tests
- Add GitHub Actions integration
- Add Docker-based execution
- Add distributed Locust execution
- Add additional positive and negative test scenarios
