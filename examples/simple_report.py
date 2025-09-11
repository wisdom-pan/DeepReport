#!/usr/bin/env python3
"""
Simple example of generating a DeepReport
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import DeepReportApp

async def generate_simple_report():
    """Generate a simple financial report"""
    
    # Initialize the app
    app = DeepReportApp()
    
    # Define research parameters
    research_topic = "Tesla Inc. (TSLA) Q4 2023 Financial Performance Analysis"
    requirements = """
    Analyze Tesla's Q4 2023 financial performance
    Compare with previous quarters
    Identify key growth drivers
    Assess market position and competition
    Provide investment outlook
    """
    
    print("🚀 Starting DeepReport generation...")
    print(f"📊 Research Topic: {research_topic}")
    print(f"📋 Requirements: {requirements.strip()}")
    
    try:
        # Generate the report
        result = await app.generate_report(
            research_topic=research_topic,
            requirements=requirements,
            output_format="html",
            model="gpt-4o"
        )
        
        if result["success"]:
            print("✅ Report generated successfully!")
            print(f"📄 Report saved to: {result.get('report_path', 'Unknown')}")
            print(f"⏱️ Generation time: {result.get('generation_time', 'Unknown')}")
            print(f"📊 Charts included: {result.get('report_data', {}).get('charts_data', [])}")
            print(f"📚 Citations included: {len(result.get('report_data', {}).get('citations', []))}")
        else:
            print(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Run the example
    success = asyncio.run(generate_simple_report())
    
    if success:
        print("\n🎉 Example completed successfully!")
        print("Check the 'reports' directory for the generated HTML report.")
    else:
        print("\n💥 Example failed. Please check your configuration.")
        sys.exit(1)