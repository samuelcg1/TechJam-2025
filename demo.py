#!/usr/bin/env python3
"""
Demonstration script for the Geo-Compliance Analysis Tool

This script shows how to use the system programmatically and demonstrates
various features and capabilities.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from compliance_analyzer import ComplianceAnalyzer
import pandas as pd


def demo_single_feature_analysis():
    """Demonstrate single feature analysis."""
    print("🔍 Demo: Single Feature Analysis")
    print("=" * 50)
    
    # Note: This would require a real API key to work
    print("Note: This demo uses mocked responses for demonstration purposes.")
    print("In a real scenario, you would need a valid OpenAI API key.\n")
    
    # Example features to analyze
    features = [
        {
            'title': 'Age Verification System',
            'description': 'Implement age gates for users under 18 to comply with COPPA and state regulations',
            'documents': 'age_verification_specs.pdf'
        },
        {
            'title': 'Location-Based Content Filtering',
            'description': 'Block content based on user location to meet regional compliance requirements',
            'documents': 'geo_blocking_requirements.txt'
        },
        {
            'title': 'User Profile Management',
            'description': 'Basic user profile creation and management functionality',
            'documents': ''
        },
        {
            'title': 'Live Streaming Feature',
            'description': 'Allow users to stream live video content to their followers',
            'documents': 'live_streaming_policy.pdf'
        }
    ]
    
    print("Example features that would be analyzed:")
    for i, feature in enumerate(features, 1):
        print(f"\n{i}. {feature['title']}")
        print(f"   Description: {feature['description']}")
        if feature['documents']:
            print(f"   Documents: {feature['documents']}")
    
    print("\n" + "=" * 50)


def demo_csv_analysis():
    """Demonstrate CSV analysis workflow."""
    print("📊 Demo: CSV Analysis Workflow")
    print("=" * 50)
    
    # Create sample data
    sample_data = {
        'Title': [
            'Age Verification System',
            'Location-Based Content Filtering',
            'User Profile Management',
            'Live Streaming Feature',
            'E-commerce Integration'
        ],
        'Description': [
            'Implement age gates for users under 18 to comply with COPPA and state regulations',
            'Block content based on user location to meet regional compliance requirements',
            'Basic user profile creation and management functionality',
            'Allow users to stream live video content to their followers',
            'Enable users to purchase products directly through the platform'
        ],
        'Documents': [
            'age_verification_specs.pdf',
            'geo_blocking_requirements.txt',
            '',
            'live_streaming_policy.pdf',
            'ecommerce_compliance.pdf'
        ]
    }
    
    # Create sample CSV
    df = pd.DataFrame(sample_data)
    sample_csv_path = 'demo_features.csv'
    df.to_csv(sample_csv_path, index=False)
    
    print(f"✅ Created sample CSV file: {sample_csv_path}")
    print(f"📋 Contains {len(df)} features to analyze")
    
    print("\nExpected analysis workflow:")
    print("1. Read CSV file with feature data")
    print("2. Validate required columns (Title, Description)")
    print("3. Process each feature:")
    print("   - Extract text from PDF documents (if any)")
    print("   - Perform rule-based keyword analysis")
    print("   - Use LLM for intelligent compliance assessment")
    print("   - Combine results with reasoning")
    print("4. Output results to CSV with columns:")
    print("   - Title")
    print("   - Needs Geo-Compliance Logic?")
    print("   - Reasoning")
    print("   - Related Regulations")
    print("   - Rule-Based Keywords")
    print("   - Confidence")
    
    # Clean up
    if os.path.exists(sample_csv_path):
        os.remove(sample_csv_path)
    
    print("\n" + "=" * 50)


def demo_compliance_keywords():
    """Demonstrate compliance keyword categories."""
    print("🔑 Demo: Compliance Keyword Categories")
    print("=" * 50)
    
    # This would normally come from the analyzer instance
    compliance_keywords = {
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
    
    print("The system uses keyword-based analysis to automatically flag features:")
    for category, keywords in compliance_keywords.items():
        print(f"\n📝 {category.replace('_', ' ').title()}:")
        print(f"   Keywords: {', '.join(keywords[:3])}{'...' if len(keywords) > 3 else ''}")
    
    print("\n" + "=" * 50)


def demo_regulations():
    """Demonstrate supported regulations."""
    print("📋 Demo: Supported Regulations")
    print("=" * 50)
    
    regulations = {
        'DSA': 'Digital Services Act (EU)',
        'COPPA': 'Children\'s Online Privacy Protection Act (US)',
        'GDPR': 'General Data Protection Regulation (EU)',
        'California_Protecting_Our_Kids': 'California Protecting Our Kids Act',
        'Florida_Online_Protections': 'Florida Online Protections for Minors',
        'Utah_Social_Media': 'Utah Social Media Regulation Act',
        'NCMEC': 'NCMEC reporting requirements',
        'CCPA': 'California Consumer Privacy Act'
    }
    
    print("The system analyzes features against these regulations:")
    for code, name in regulations.items():
        print(f"• {code}: {name}")
    
    print("\n" + "=" * 50)


def demo_usage_examples():
    """Show usage examples."""
    print("💻 Demo: Usage Examples")
    print("=" * 50)
    
    print("1. Command Line Interface:")
    print("   python main.py analyze features.csv")
    print("   python main.py analyze features.csv --output results.csv")
    print("   python main.py analyze features.csv --verbose")
    print("   python main.py demo")
    print("   python main.py create-sample")
    
    print("\n2. Python API:")
    print("   from src.compliance_analyzer import ComplianceAnalyzer")
    print("   analyzer = ComplianceAnalyzer(api_key='your_key')")
    print("   result = analyzer.analyze_feature(title, description, documents)")
    print("   results_df = analyzer.analyze_csv('input.csv', 'output.csv')")
    
    print("\n3. Web Interface:")
    print("   python main.py demo")
    print("   # Then open http://localhost:8501 in your browser")
    
    print("\n" + "=" * 50)


def main():
    """Run all demonstrations."""
    print("🌍 Geo-Compliance Analysis Tool - Demonstration")
    print("=" * 60)
    print("This demonstration shows the capabilities of the system\n")
    
    demo_single_feature_analysis()
    demo_csv_analysis()
    demo_compliance_keywords()
    demo_regulations()
    demo_usage_examples()
    
    print("🎉 Demonstration Complete!")
    print("\nTo get started:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your_key'")
    print("2. Run the web demo: python main.py demo")
    print("3. Or analyze a CSV: python main.py analyze sample_data/sample_features.csv")
    print("\nFor more information, see the README.md file.")


if __name__ == "__main__":
    main()
