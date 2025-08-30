"""
Unit tests for the ComplianceAnalyzer class.

This module contains comprehensive tests to ensure the geo-compliance
analysis system works correctly and handles edge cases properly.
"""

import unittest
import tempfile
import os
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from compliance_analyzer import ComplianceAnalyzer


class TestComplianceAnalyzer(unittest.TestCase):
    """Test cases for the ComplianceAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock API key for testing
        self.mock_api_key = "test_api_key_12345"
        
        # Create a mock OpenAI client
        self.mock_client = Mock()
        self.mock_response = Mock()
        self.mock_choice = Mock()
        self.mock_message = Mock()
        
        # Set up the mock response structure
        self.mock_message.content = '{"needs_compliance": "Yes", "reasoning": "Test reasoning", "related_regulations": ["DSA", "GDPR"], "confidence": "high"}'
        self.mock_choice.message = self.mock_message
        self.mock_response.choices = [self.mock_choice]
        self.mock_client.chat.completions.create.return_value = self.mock_response
        
        # Create analyzer with mocked client
        with patch('compliance_analyzer.OpenAI') as mock_openai:
            mock_openai.return_value = self.mock_client
            self.analyzer = ComplianceAnalyzer(api_key=self.mock_api_key)
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        with patch('compliance_analyzer.OpenAI') as mock_openai:
            mock_openai.return_value = self.mock_client
            analyzer = ComplianceAnalyzer(api_key="test_key")
            self.assertEqual(analyzer.api_key, "test_key")
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                ComplianceAnalyzer()
    
    def test_init_with_env_api_key(self):
        """Test initialization with API key from environment."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'env_test_key'}):
            with patch('compliance_analyzer.OpenAI') as mock_openai:
                mock_openai.return_value = self.mock_client
                analyzer = ComplianceAnalyzer()
                self.assertEqual(analyzer.api_key, "env_test_key")
    
    def test_extract_text_from_pdf_success(self):
        """Test successful PDF text extraction."""
        # Create a temporary PDF file with some content
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            # This is a minimal PDF structure - in real tests you'd use a proper PDF
            tmp_file.write(b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n')
            tmp_file_path = tmp_file.name
        
        try:
            # Test extraction (this will likely fail with our minimal PDF, but tests the method structure)
            result = self.analyzer.extract_text_from_pdf(tmp_file_path)
            # The result should be a string (even if empty due to minimal PDF)
            self.assertIsInstance(result, str)
        finally:
            os.unlink(tmp_file_path)
    
    def test_extract_text_from_pdf_file_not_found(self):
        """Test PDF extraction with non-existent file."""
        result = self.analyzer.extract_text_from_pdf("nonexistent.pdf")
        self.assertEqual(result, "")
    
    def test_rule_based_analysis_with_compliance_keywords(self):
        """Test rule-based analysis with compliance keywords."""
        title = "Age Verification System"
        description = "Implement age gates for users under 18"
        
        result = self.analyzer.rule_based_analysis(title, description)
        
        self.assertTrue(result['needs_compliance'])
        self.assertIn('age_gate', result['found_keywords'])
        self.assertEqual(result['confidence'], 'high')
    
    def test_rule_based_analysis_without_compliance_keywords(self):
        """Test rule-based analysis without compliance keywords."""
        title = "Simple Calculator"
        description = "Basic mathematical operations"
        
        result = self.analyzer.rule_based_analysis(title, description)
        
        self.assertFalse(result['needs_compliance'])
        self.assertEqual(len(result['found_keywords']), 0)
        self.assertEqual(result['confidence'], 'low')
    
    def test_rule_based_analysis_with_mixed_keywords(self):
        """Test rule-based analysis with mixed compliance and non-compliance keywords."""
        title = "User Profile Management"
        description = "Basic profile creation with some user data collection"
        
        result = self.analyzer.rule_based_analysis(title, description)
        
        # Should detect privacy-related keywords
        self.assertIn('privacy', result['found_keywords'])
        # But shouldn't trigger high-priority compliance
        self.assertFalse(result['needs_compliance'])
    
    def test_llm_analysis_success(self):
        """Test successful LLM analysis."""
        title = "Test Feature"
        description = "Test description"
        
        result = self.analyzer.llm_analysis(title, description)
        
        self.assertEqual(result['needs_compliance'], 'Yes')
        self.assertEqual(result['reasoning'], 'Test reasoning')
        self.assertEqual(result['related_regulations'], ['DSA', 'GDPR'])
        self.assertEqual(result['confidence'], 'high')
    
    def test_llm_analysis_failure(self):
        """Test LLM analysis failure handling."""
        # Make the API call fail
        self.mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        title = "Test Feature"
        description = "Test description"
        
        result = self.analyzer.llm_analysis(title, description)
        
        self.assertEqual(result['needs_compliance'], 'Needs Review')
        self.assertIn('Analysis failed due to error', result['reasoning'])
        self.assertEqual(result['confidence'], 'low')
    
    def test_parse_llm_response_valid_json(self):
        """Test parsing valid JSON response from LLM."""
        valid_response = '{"needs_compliance": "No", "reasoning": "No compliance needed", "related_regulations": [], "confidence": "high"}'
        
        result = self.analyzer._parse_llm_response(valid_response)
        
        self.assertEqual(result['needs_compliance'], 'No')
        self.assertEqual(result['reasoning'], 'No compliance needed')
        self.assertEqual(result['related_regulations'], [])
        self.assertEqual(result['confidence'], 'high')
    
    def test_parse_llm_response_invalid_json(self):
        """Test parsing invalid JSON response from LLM."""
        invalid_response = "This is not JSON"
        
        result = self.analyzer._parse_llm_response(invalid_response)
        
        self.assertEqual(result['needs_compliance'], 'Needs Review')
        self.assertEqual(result['reasoning'], invalid_response)
        self.assertEqual(result['confidence'], 'low')
    
    def test_analyze_feature_combined_analysis(self):
        """Test combined analysis of a single feature."""
        title = "Age Verification System"
        description = "Implement age gates for users under 18"
        
        result = self.analyzer.analyze_feature(title, description)
        
        self.assertEqual(result['title'], title)
        self.assertEqual(result['needs_compliance'], 'Yes')
        self.assertIn('reasoning', result)
        self.assertIn('related_regulations', result)
        self.assertIn('rule_based_keywords', result)
        self.assertIn('confidence', result)
    
    def test_analyze_feature_with_pdf_documents(self):
        """Test feature analysis with PDF document paths."""
        title = "Test Feature"
        description = "Test description"
        documents = "test_document.pdf"
        
        # Mock PDF extraction
        with patch.object(self.analyzer, 'extract_text_from_pdf', return_value="Extracted PDF content"):
            result = self.analyzer.analyze_feature(title, description, documents)
        
        self.assertEqual(result['title'], title)
        self.assertIsInstance(result, dict)
    
    def test_analyze_feature_with_text_documents(self):
        """Test feature analysis with text documents."""
        title = "Test Feature"
        description = "Test description"
        documents = "Additional compliance requirements for EU users"
        
        result = self.analyzer.analyze_feature(title, description, documents)
        
        self.assertEqual(result['title'], title)
        self.assertIsInstance(result, dict)
    
    def test_analyze_csv_success(self):
        """Test successful CSV analysis."""
        # Create temporary CSV file
        test_data = {
            'Title': ['Feature 1', 'Feature 2'],
            'Description': ['Description 1', 'Description 2'],
            'Documents': ['', '']
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            df = pd.DataFrame(test_data)
            df.to_csv(tmp_file.name, index=False)
            csv_path = tmp_file.name
        
        try:
            # Analyze the CSV
            result_df = self.analyzer.analyze_csv(csv_path)
            
            # Check results
            self.assertEqual(len(result_df), 2)
            self.assertIn('Title', result_df.columns)
            self.assertIn('Needs Geo-Compliance Logic?', result_df.columns)
            self.assertIn('Reasoning', result_df.columns)
            self.assertIn('Related Regulations', result_df.columns)
            
        finally:
            os.unlink(csv_path)
    
    def test_analyze_csv_missing_columns(self):
        """Test CSV analysis with missing required columns."""
        # Create CSV with missing columns
        test_data = {
            'Title': ['Feature 1'],
            'WrongColumn': ['Wrong data']
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            df = pd.DataFrame(test_data)
            df.to_csv(tmp_file.name, index=False)
            csv_path = tmp_file.name
        
        try:
            with self.assertRaises(ValueError):
                self.analyzer.analyze_csv(csv_path)
        finally:
            os.unlink(csv_path)
    
    def test_analyze_csv_empty_file(self):
        """Test CSV analysis with empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            tmp_file.write('Title,Description\n')
            csv_path = tmp_file.name
        
        try:
            result_df = self.analyzer.analyze_csv(csv_path)
            self.assertEqual(len(result_df), 0)
        finally:
            os.unlink(csv_path)
    
    def test_analyze_csv_with_output_path(self):
        """Test CSV analysis with output file path."""
        # Create input CSV
        test_data = {
            'Title': ['Feature 1'],
            'Description': ['Description 1'],
            'Documents': ['']
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as input_file:
            df = pd.DataFrame(test_data)
            df.to_csv(input_file.name, index=False)
            input_path = input_file.name
        
        # Create output path
        output_path = tempfile.mktemp(suffix='.csv')
        
        try:
            # Analyze with output path
            result_df = self.analyzer.analyze_csv(input_path, output_path)
            
            # Check that output file was created
            self.assertTrue(os.path.exists(output_path))
            
            # Check that output file contains expected data
            output_df = pd.read_csv(output_path)
            self.assertEqual(len(output_df), 1)
            self.assertIn('Title', output_df.columns)
            
        finally:
            os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_analyze_csv_skip_empty_rows(self):
        """Test that empty rows are skipped during analysis."""
        # Create CSV with empty rows
        test_data = {
            'Title': ['Feature 1', '   ', 'Feature 3'],  # Row 2 has whitespace-only title
            'Description': ['Description 1', 'Description 2', 'Description 3'],
            'Documents': ['', '', '']
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            df = pd.DataFrame(test_data)
            df.to_csv(tmp_file.name, index=False)
            csv_path = tmp_file.name
        
        try:
            result_df = self.analyzer.analyze_csv(csv_path)
            # Should process Feature 1 and Feature 3 (row 2 has whitespace-only title which gets stripped to empty)
            self.assertEqual(len(result_df), 2)
            self.assertEqual(result_df.iloc[0]['Title'], 'Feature 1')
            self.assertEqual(result_df.iloc[1]['Title'], 'Feature 3')
        finally:
            os.unlink(csv_path)
    
    def test_compliance_keywords_structure(self):
        """Test that compliance keywords are properly structured."""
        expected_categories = [
            'age_gate', 'location_blocking', 'data_localization', 'privacy',
            'content_moderation', 'monetization', 'social_features', 'algorithm',
            'live_streaming', 'ecommerce'
        ]
        
        for category in expected_categories:
            self.assertIn(category, self.analyzer.compliance_keywords)
            self.assertIsInstance(self.analyzer.compliance_keywords[category], list)
            self.assertGreater(len(self.analyzer.compliance_keywords[category]), 0)
    
    def test_regulations_structure(self):
        """Test that regulations are properly structured."""
        expected_regulations = [
            'DSA', 'COPPA', 'GDPR', 'California_Protecting_Our_Kids',
            'Florida_Online_Protections', 'Utah_Social_Media', 'NCMEC', 'CCPA'
        ]
        
        for regulation in expected_regulations:
            self.assertIn(regulation, self.analyzer.regulations)
            self.assertIsInstance(self.analyzer.regulations[regulation], str)
            self.assertGreater(len(self.analyzer.regulations[regulation]), 0)


if __name__ == '__main__':
    unittest.main()
