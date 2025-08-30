# 🌍 Geo-Compliance Analysis Tool

A production-ready AI-powered system for flagging features that require geo-specific compliance logic, built for TikTok TechJam 2025.

## 🎯 Overview

This tool analyzes feature artifacts to determine whether they require geo-specific compliance logic based on various regulations including:

- **DSA** (Digital Services Act - EU)
- **COPPA** (Children's Online Privacy Protection Act - US)
- **GDPR** (General Data Protection Regulation - EU)
- **California Protecting Our Kids Act**
- **Florida Online Protections for Minors**
- **Utah Social Media Regulation Act**
- **NCMEC** reporting requirements
- **CCPA** (California Consumer Privacy Act)

## ✨ Features

- **AI-Powered Analysis**: Uses OpenAI GPT models for intelligent compliance assessment
- **Rule-Based Augmentation**: Keyword-based analysis for automatic flagging
- **PDF Document Support**: Extracts and analyzes text from PDF documents
- **Interactive Web Interface**: Beautiful Streamlit-based demo application
- **Command-Line Interface**: Batch processing capabilities
- **Comprehensive Testing**: Full test suite ensuring reliability
- **Edge Case Handling**: Graceful handling of missing data, empty files, and errors

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TechJam-2025
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   # Option 1: Environment variable
   export OPENAI_API_KEY="your_api_key_here"
   
   # Option 2: Create .env file
   cp env_example.txt .env
   # Edit .env and add your API key
   ```

### Usage

#### 🖥️ Interactive Web Demo

```bash
python main.py demo
```

Then open your browser to `http://localhost:8501`

#### 📊 Command Line Analysis

```bash
# Analyze a CSV file
python main.py analyze sample_data/sample_features.csv

# Save results to file
python main.py analyze sample_data/sample_features.csv --output results.csv

# Verbose output
python main.py analyze sample_data/sample_features.csv --verbose

# Create sample data
python main.py create-sample --output my_features.csv
```

#### 🐍 Python API

```python
from src.compliance_analyzer import ComplianceAnalyzer

# Initialize analyzer
analyzer = ComplianceAnalyzer(api_key="your_api_key")

# Analyze single feature
result = analyzer.analyze_feature(
    title="Age Verification System",
    description="Implement age gates for users under 18",
    documents="age_verification_specs.pdf"
)

# Analyze CSV file
results_df = analyzer.analyze_csv("features.csv", "results.csv")
```

## 📁 Project Structure

```
TechJam-2025/
├── src/
│   ├── __init__.py
│   ├── compliance_analyzer.py    # Core analysis engine
│   └── streamlit_app.py         # Web interface
├── tests/
│   ├── __init__.py
│   └── test_compliance_analyzer.py  # Unit tests
├── sample_data/
│   └── sample_features.csv      # Example data
├── main.py                      # CLI interface
├── requirements.txt             # Dependencies
├── env_example.txt             # Environment template
└── README.md                   # This file
```

## 📊 Input Format

The system expects a CSV file with the following columns:

| Column | Required | Description |
|--------|----------|-------------|
| `Title` | ✅ | Feature name |
| `Description` | ✅ | Detailed feature description |
| `Documents` | ❌ | Path to PDF files or additional text |

### Example CSV

```csv
Title,Description,Documents
Age Verification System,Implement age gates for users under 18 to comply with COPPA and state regulations,age_verification_specs.pdf
Location-Based Content Filtering,Block content based on user location to meet regional compliance requirements,geo_blocking_requirements.txt
User Profile Management,Basic user profile creation and management functionality,
```

## 📈 Output Format

The system outputs a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| `Title` | Original feature title |
| `Needs Geo-Compliance Logic?` | Yes/No/Needs Review |
| `Reasoning` | Clear explanation of the decision |
| `Related Regulations` | List of relevant regulations |
| `Rule-Based Keywords` | Keywords that triggered rule-based analysis |
| `Confidence` | Confidence level of the analysis |

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: gpt-4)
- `LOG_LEVEL`: Logging level (default: INFO)

### Analysis Options

The system uses a hybrid approach:

1. **Rule-Based Analysis**: Keyword matching for automatic flagging
2. **LLM Analysis**: AI-powered assessment with reasoning
3. **Combined Results**: Intelligent merging of both approaches

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_compliance_analyzer

# Run with verbose output
python -m unittest tests.test_compliance_analyzer -v
```

## 🛠️ Development

### Adding New Compliance Keywords

Edit `src/compliance_analyzer.py` and add keywords to the `compliance_keywords` dictionary:

```python
self.compliance_keywords = {
    'new_category': ['keyword1', 'keyword2', 'keyword3'],
    # ... existing categories
}
```

### Adding New Regulations

Add regulations to the `regulations` dictionary:

```python
self.regulations = {
    'NEW_REG': 'New Regulation Name',
    # ... existing regulations
}
```

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover tests -v
```

## 🚨 Error Handling

The system handles various edge cases gracefully:

- **Missing API Key**: Clear error message with setup instructions
- **Invalid CSV Format**: Validation with helpful error messages
- **Empty Files**: Skips empty rows and provides warnings
- **PDF Extraction Failures**: Continues analysis with available text
- **API Failures**: Falls back to rule-based analysis
- **Network Issues**: Retry logic and graceful degradation

## 📋 Supported Regulations

| Regulation | Region | Focus |
|------------|--------|-------|
| **DSA** | EU | Digital services, content moderation |
| **COPPA** | US | Children's privacy (under 13) |
| **GDPR** | EU | Data protection and privacy |
| **California Protecting Our Kids Act** | California | Social media for minors |
| **Florida Online Protections** | Florida | Minors' online safety |
| **Utah Social Media Regulation** | Utah | Social media restrictions |
| **NCMEC** | US | Child exploitation reporting |
| **CCPA** | California | Consumer privacy rights |

## 🔍 Analysis Categories

The system analyzes features across these categories:

- **Age Verification**: Age gates, verification systems
- **Location Blocking**: Geographic restrictions, geo-blocking
- **Data Localization**: Regional data storage requirements
- **Privacy**: Data protection, personal information
- **Content Moderation**: Harmful content, inappropriate material
- **Monetization**: Advertising, revenue generation
- **Social Features**: User-generated content, social media
- **Algorithms**: Recommendation systems, personalization
- **Live Streaming**: Real-time content broadcasting
- **E-commerce**: Shopping, payments, transactions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is built for TikTok TechJam 2025.

## 🆘 Support

For issues and questions:

1. Check the documentation above
2. Review the test cases for usage examples
3. Run the demo to see the system in action
4. Check the logs for detailed error information

## 🎉 Acknowledgments

Built for TikTok TechJam 2025 using:
- OpenAI GPT models for intelligent analysis
- Streamlit for beautiful web interfaces
- Pandas for data processing
- PyPDF2 for document analysis
- Comprehensive testing for reliability