#!/usr/bin/env python3
"""
Command-line interface for Geo-Compliance Analysis Tool

This script provides a command-line interface for analyzing features
and determining geo-specific compliance requirements.
"""

import argparse
import os
import sys
from pathlib import Path
import pandas as pd

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from compliance_analyzer import ComplianceAnalyzer


def main():
    """
    Main command-line interface function.
    """
    parser = argparse.ArgumentParser(
        description="Geo-Compliance Analysis Tool - Analyze features for geo-specific compliance requirements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py analyze features.csv
  python main.py analyze features.csv --output results.csv
  python main.py analyze features.csv --api-key YOUR_API_KEY
  python main.py demo
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze features from CSV file')
    analyze_parser.add_argument('input_file', help='Input CSV file path')
    analyze_parser.add_argument('--output', '-o', help='Output CSV file path (optional)')
    analyze_parser.add_argument('--api-key', help='OpenAI API key (optional, can use environment variable)')
    analyze_parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run interactive demo')
    demo_parser.add_argument('--port', type=int, default=8501, help='Port for Streamlit app (default: 8501)')
    
    # Create sample command
    sample_parser = subparsers.add_parser('create-sample', help='Create a sample CSV file')
    sample_parser.add_argument('--output', '-o', default='sample_features.csv', help='Output file path (default: sample_features.csv)')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        analyze_features(args)
    elif args.command == 'demo':
        run_demo(args)
    elif args.command == 'create-sample':
        create_sample_csv(args)
    else:
        parser.print_help()


def analyze_features(args):
    """
    Analyze features from CSV file.
    
    Args:
        args: Command line arguments
    """
    try:
        # Check if input file exists
        if not os.path.exists(args.input_file):
            print(f"❌ Error: Input file '{args.input_file}' not found.")
            sys.exit(1)
        
        # Initialize analyzer
        try:
            analyzer = ComplianceAnalyzer(api_key=args.api_key)
        except ValueError as e:
            print(f"❌ Error: {e}")
            print("💡 Set your OpenAI API key using --api-key or OPENAI_API_KEY environment variable.")
            sys.exit(1)
        
        print(f"🔍 Analyzing features from '{args.input_file}'...")
        
        # Analyze the CSV
        results_df = analyzer.analyze_csv(args.input_file, args.output)
        
        # Print summary
        print("\n📊 Analysis Summary:")
        print(f"Total features analyzed: {len(results_df)}")
        
        yes_count = len(results_df[results_df['Needs Geo-Compliance Logic?'] == 'Yes'])
        no_count = len(results_df[results_df['Needs Geo-Compliance Logic?'] == 'No'])
        review_count = len(results_df[results_df['Needs Geo-Compliance Logic?'] == 'Needs Review'])
        
        print(f"Features needing compliance: {yes_count}")
        print(f"Features not needing compliance: {no_count}")
        print(f"Features needing review: {review_count}")
        
        if args.output:
            print(f"\n✅ Results saved to '{args.output}'")
        else:
            print("\n📋 Results:")
            print(results_df.to_string(index=False))
        
        # Show detailed results if verbose
        if args.verbose:
            print("\n🔍 Detailed Results:")
            for _, row in results_df.iterrows():
                print(f"\n📝 {row['Title']}")
                print(f"   Needs Compliance: {row['Needs Geo-Compliance Logic?']}")
                print(f"   Reasoning: {row['Reasoning']}")
                if row['Related Regulations']:
                    regs = eval(row['Related Regulations']) if isinstance(row['Related Regulations'], str) else row['Related Regulations']
                    print(f"   Related Regulations: {', '.join(regs)}")
                if row['Rule-Based Keywords']:
                    print(f"   Keywords Found: {row['Rule-Based Keywords']}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)


def run_demo(args):
    """
    Run the Streamlit demo application.
    
    Args:
        args: Command line arguments
    """
    try:
        import streamlit.web.cli as stcli
        import sys
        
        # Set up Streamlit arguments
        sys.argv = [
            "streamlit", "run", 
            str(Path(__file__).parent / "src" / "streamlit_app.py"),
            "--server.port", str(args.port),
            "--server.headless", "true"
        ]
        
        print(f"🚀 Starting Streamlit demo on port {args.port}...")
        print(f"🌐 Open your browser and go to: http://localhost:{args.port}")
        print("💡 Press Ctrl+C to stop the server")
        
        # Run Streamlit
        stcli.main()
        
    except ImportError:
        print("❌ Error: Streamlit is not installed.")
        print("💡 Install it with: pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting demo: {e}")
        sys.exit(1)


def create_sample_csv(args):
    """
    Create a sample CSV file with example features.
    
    Args:
        args: Command line arguments
    """
    try:
        # Sample data
        sample_data = {
            'Title': [
                'Age Verification System',
                'Location-Based Content Filtering',
                'User Profile Management',
                'Live Streaming Feature',
                'E-commerce Integration',
                'Content Recommendation Algorithm',
                'User-Generated Content Platform',
                'Advertising System',
                'Data Analytics Dashboard',
                'Social Media Sharing'
            ],
            'Description': [
                'Implement age gates for users under 18 to comply with COPPA and state regulations',
                'Block content based on user location to meet regional compliance requirements',
                'Basic user profile creation and management functionality',
                'Allow users to stream live video content to their followers',
                'Enable users to purchase products directly through the platform',
                'AI-powered content recommendation system that personalizes user experience',
                'Platform for users to upload and share their own content',
                'Targeted advertising system with user data analysis',
                'Analytics dashboard for tracking user behavior and platform metrics',
                'Social media integration allowing users to share content across platforms'
            ],
            'Documents': [
                'age_verification_specs.pdf',
                'geo_blocking_requirements.txt',
                '',
                'live_streaming_policy.pdf',
                'ecommerce_compliance.pdf',
                'algorithm_transparency_report.pdf',
                'ugc_guidelines.pdf',
                'advertising_policy.pdf',
                'analytics_privacy_policy.pdf',
                'social_sharing_terms.pdf'
            ]
        }
        
        # Create DataFrame and save
        df = pd.DataFrame(sample_data)
        df.to_csv(args.output, index=False)
        
        print(f"✅ Sample CSV file created: '{args.output}'")
        print(f"📋 Contains {len(df)} example features")
        print("\n💡 You can now use this file with the analyze command:")
        print(f"   python main.py analyze {args.output}")
        
    except Exception as e:
        print(f"❌ Error creating sample file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
