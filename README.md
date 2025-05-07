# Conversational Data Analyst (Powered by Gemini)

A Streamlit web application that mimics Google Looker Conversational Analytics using the Google Gemini API. This application allows users to upload data files and ask questions about their data in natural language.

## Features

- File upload support for .csv, .xlsx, and .xls files
- Natural language data analysis using Gemini API
- Automatic visualization generation
- Safe code execution environment
- Chat history tracking
- Interactive data exploration

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd conversational-data-analyst
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Upload your data file (.csv, .xlsx, or .xls)

4. Ask questions about your data in natural language, for example:
   - "Show me the distribution of sales by region"
   - "What is the average customer age?"
   - "Create a line chart of revenue over time"

## Security Features

- Safe code execution environment
- Limited access to Python built-ins
- Input validation and sanitization
- Session-based data storage

## Example Use Cases

1. Customer Data Analysis:
   - Upload customer acquisition data
   - Ask: "How many customers were acquired over time?"
   - Get automatic visualization of monthly acquisition trends

2. Sales Analysis:
   - Upload sales data
   - Ask: "What are the top 5 products by revenue?"
   - Get a bar chart and detailed analysis

3. Financial Analysis:
   - Upload financial statements
   - Ask: "Show me the trend of operating expenses"
   - Get a line chart and trend analysis

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 