"""
Geo-Compliance Analysis Engine

This module provides the core functionality for analyzing features and determining
whether they require geo-specific compliance logic based on various regulations.
"""

import os
import re
import logging
from typing import Dict, List, Optional, Tuple
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class ComplianceAnalyzer:
    """
    Main class for analyzing feature compliance requirements.
    
    This class handles the analysis of features to determine if they require
    geo-specific compliance logic based on various regulations and keywords.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the compliance analyzer.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from environment.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Define compliance-related keywords that should trigger flags
        self.compliance_keywords = {
            'age_gate': ['age gate', 'age verification', 'age check', 'under 18', 'under 13', 'minors'],
            'location_blocking': ['location-based blocking', 'geo-blocking', 'geographic restriction', 'country-specific'],
            'data_localization': ['data localization', 'data residency', 'local data storage', 'regional data'],
            'privacy': ['privacy policy', 'data protection', 'personal information', 'user data'],
            'content_moderation': ['content moderation', 'harmful content', 'inappropriate content', 'reporting'],
            'monetization': ['advertising', 'monetization', 'revenue', 'sponsored content', 'influencer'],
            'social_features': ['social media', 'user-generated content', 'comments', 'sharing', 'messaging'],
            'algorithm': ['recommendation algorithm', 'content recommendation', 'personalized content'],
            'live_streaming': ['live streaming', 'live video', 'broadcasting', 'real-time content'],
            'ecommerce': ['shopping', 'e-commerce', 'purchases', 'transactions', 'payments']
        }
        
        # Define regulations to check for
        self.regulations = {
            'DSA': 'Digital Services Act (EU)',
            'COPPA': 'Children\'s Online Privacy Protection Act (US)',
            'GDPR': 'General Data Protection Regulation (EU)',
            'California_Protecting_Our_Kids': 'California Protecting Our Kids Act',
            'Florida_Online_Protections': 'Florida Online Protections for Minors',
            'Utah_Social_Media': 'Utah Social Media Regulation Act',
            'NCMEC': 'NCMEC reporting requirements',
            'CCPA': 'California Consumer Privacy Act'
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.warning(f"Failed to extract text from PDF {pdf_path}: {e}")
            return ""
    
    def rule_based_analysis(self, title: str, description: str, documents: str = "") -> Dict:
        """
        Perform rule-based analysis using keyword matching.
        
        Args:
            title: Feature title
            description: Feature description
            documents: Additional document content
            
        Returns:
            Dictionary with rule-based analysis results
        """
        # Combine all text for analysis
        combined_text = f"{title} {description} {documents}".lower()
        
        # Check for compliance keywords
        found_keywords = {}
        for category, keywords in self.compliance_keywords.items():
            found = [keyword for keyword in keywords if keyword.lower() in combined_text]
            if found:
                found_keywords[category] = found
        
        # Determine if rule-based analysis suggests compliance is needed
        high_priority_categories = ['age_gate', 'location_blocking', 'data_localization', 'content_moderation']
        needs_compliance = any(cat in found_keywords for cat in high_priority_categories)
        
        return {
            'needs_compliance': needs_compliance,
            'found_keywords': found_keywords,
            'confidence': 'high' if needs_compliance else 'low'
        }
    
    def llm_analysis(self, title: str, description: str, documents: str = "") -> Dict:
        """
        Perform LLM-based analysis to determine compliance requirements.
        
        Args:
            title: Feature title
            description: Feature description
            documents: Additional document content
            
        Returns:
            Dictionary with LLM analysis results
        """
        try:
            # Prepare the prompt for the LLM
            prompt = self._create_analysis_prompt(title, description, documents)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in digital compliance and regulations. Analyze features to determine if they require geo-specific compliance logic."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse the response
            result = self._parse_llm_response(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return {
                'needs_compliance': 'Needs Review',
                'reasoning': f'Analysis failed due to error: {str(e)}',
                'related_regulations': [],
                'confidence': 'low'
            }
    
    def _create_analysis_prompt(self, title: str, description: str, documents: str) -> str:
        """
        Create the analysis prompt for the LLM.
        
        Args:
            title: Feature title
            description: Feature description
            documents: Additional document content
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
Analyze the following feature to determine if it requires geo-specific compliance logic:

Title: {title}
Description: {description}
Additional Documents: {documents if documents else "None provided"}

Please provide your analysis in the following JSON format:
{{
    "needs_compliance": "Yes/No/Needs Review",
    "reasoning": "Clear explanation of your decision",
    "related_regulations": ["List of relevant regulations"],
    "confidence": "high/medium/low"
}}

Consider the following regulations:
- DSA (Digital Services Act - EU)
- COPPA (Children's Online Privacy Protection Act - US)
- GDPR (General Data Protection Regulation - EU)
- California Protecting Our Kids Act
- Florida Online Protections for Minors
- Utah Social Media Regulation Act
- NCMEC reporting requirements
- CCPA (California Consumer Privacy Act)

Features that typically need geo-compliance logic include:
- Age verification or age-gating features
- Location-based content blocking or restrictions
- Data localization requirements
- Content moderation systems
- User-generated content platforms
- Advertising or monetization features
- Social media features
- Live streaming capabilities
- E-commerce or payment features

Respond only with the JSON analysis.
"""
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict:
        """
        Parse the LLM response to extract structured data.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed response dictionary
        """
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                import json
                parsed = json.loads(json_match.group())
                return {
                    'needs_compliance': parsed.get('needs_compliance', 'Needs Review'),
                    'reasoning': parsed.get('reasoning', 'No reasoning provided'),
                    'related_regulations': parsed.get('related_regulations', []),
                    'confidence': parsed.get('confidence', 'medium')
                }
            else:
                # Fallback parsing
                return {
                    'needs_compliance': 'Needs Review',
                    'reasoning': response,
                    'related_regulations': [],
                    'confidence': 'low'
                }
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return {
                'needs_compliance': 'Needs Review',
                'reasoning': f'Failed to parse response: {response}',
                'related_regulations': [],
                'confidence': 'low'
            }
    
    def analyze_feature(self, title: str, description: str, documents: str = "") -> Dict:
        """
        Analyze a single feature using both rule-based and LLM approaches.
        
        Args:
            title: Feature title
            description: Feature description
            documents: Additional document content or PDF paths
            
        Returns:
            Combined analysis results
        """
        # Extract text from documents if they're PDF paths
        document_text = ""
        if documents:
            if documents.lower().endswith('.pdf'):
                document_text = self.extract_text_from_pdf(documents)
            else:
                document_text = documents
        
        # Perform rule-based analysis
        rule_results = self.rule_based_analysis(title, description, document_text)
        
        # Perform LLM analysis
        llm_results = self.llm_analysis(title, description, document_text)
        
        # Combine results
        final_result = {
            'title': title,
            'needs_compliance': llm_results['needs_compliance'],
            'reasoning': llm_results['reasoning'],
            'related_regulations': llm_results['related_regulations'],
            'rule_based_keywords': rule_results['found_keywords'],
            'confidence': llm_results['confidence']
        }
        
        # If rule-based analysis strongly suggests compliance is needed, override LLM if it says "No"
        if (rule_results['needs_compliance'] and 
            rule_results['confidence'] == 'high' and 
            llm_results['needs_compliance'] == 'No'):
            final_result['needs_compliance'] = 'Yes'
            final_result['reasoning'] += f" (Overridden by rule-based analysis: found keywords {rule_results['found_keywords']})"
        
        return final_result
    
    def analyze_csv(self, csv_path: str, output_path: str = None) -> pd.DataFrame:
        """
        Analyze features from a CSV file and output results.
        
        Args:
            csv_path: Path to input CSV file
            output_path: Path to output CSV file (optional)
            
        Returns:
            DataFrame with analysis results
        """
        try:
            # Read input CSV
            df = pd.read_csv(csv_path)
            
            # Validate required columns
            required_columns = ['Title', 'Description']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Initialize results list
            results = []
            
            # Analyze each feature
            for index, row in df.iterrows():
                logger.info(f"Analyzing feature {index + 1}/{len(df)}: {row['Title']}")
                
                title = str(row['Title']).strip()
                description = str(row['Description']).strip()
                documents = str(row.get('Documents', '')).strip()
                
                # Skip empty rows
                if not title or not description:
                    logger.warning(f"Skipping row {index + 1}: missing title or description")
                    continue
                
                # Analyze the feature
                analysis = self.analyze_feature(title, description, documents)
                results.append(analysis)
            
            # Create results DataFrame
            results_df = pd.DataFrame(results)
            
            # Reorder columns for output
            output_columns = [
                'Title', 'Needs Geo-Compliance Logic?', 'Reasoning', 
                'Related Regulations', 'Rule-Based Keywords', 'Confidence'
            ]
            
            # Map internal column names to output names
            column_mapping = {
                'title': 'Title',
                'needs_compliance': 'Needs Geo-Compliance Logic?',
                'reasoning': 'Reasoning',
                'related_regulations': 'Related Regulations',
                'rule_based_keywords': 'Rule-Based Keywords',
                'confidence': 'Confidence'
            }
            
            results_df = results_df.rename(columns=column_mapping)
            
            # Ensure all required columns exist
            for col in output_columns:
                if col not in results_df.columns:
                    results_df[col] = ''
            
            # Select and reorder columns
            results_df = results_df[output_columns]
            
            # Save to CSV if output path provided
            if output_path:
                results_df.to_csv(output_path, index=False)
                logger.info(f"Results saved to {output_path}")
            
            return results_df
            
        except Exception as e:
            logger.error(f"Failed to analyze CSV: {e}")
            raise
