# LinkedIn Job Connector Automation

Automate LinkedIn job applications and connections using Selenium and Python.

## Description

This script automates the process of connecting with job posters on LinkedIn. It reads job links from a CSV file, logs into LinkedIn, navigates to each job link, connects with the job poster, and sends a personalized message.

## Features

- Automated login to LinkedIn.
- Automated navigation to job postings.
- Automatically connects with job posters.
- Sends a predefined message to the new connection.
- Error handling to manage exceptions and continue the script.

## Prerequisites

- Python
- Selenium
- ChromeDriver
- Additional Python libraries: `random`, `time`, `yaml`, and `csv`

## Installation

Clone the repository:

```bash
git clone https://github.com/PrakashMahesh2729/LinkedIN-Apply-Connect-Bot/
```

Navigate to the project directory:

```bash
cd LinkedIN-Apply-Connect-Bot
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

**Note**: Ensure you create a `requirements.txt` file with the necessary packages (e.g., selenium, PyYAML, webdriver_manager).

## Configuration

Configure your LinkedIn credentials in the `config.yaml` file:

```yaml
username: [Your LinkedIn Username/Email]
password: [Your LinkedIn Password]
```

Ensure you replace the placeholder text with your actual LinkedIn credentials.

## Usage

Run the script:

```bash
python Job_connect.py
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
