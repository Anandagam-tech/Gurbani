#!/usr/bin/env python3
"""
Gurbani Wisdom - Main Script
============================
Enhanced with Sach Khoj Academy style deep analysis.

Usage:
    python main.py              # Process next Ang with deep analysis
    python main.py --quick      # Quick analysis (faster, less detailed)
    python main.py --ang 1      # Process specific Ang
    python main.py --reset      # Reset progress
"""

import sys
import argparse
from datetime import datetime

import config
import storage
import gurbani_api
import ollama_client
import formatter

# Try to import prompts module for specialized prompts
try:
    import prompts
    HAS_PROMPTS = True
except ImportError:
    HAS_PROMPTS = False


def print_banner():
    """Print welcome banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║                    ੴ GURBANI WISDOM ੴ                        ║
    ║                                                               ║
    ║         ਸੱਚ ਖੋਜ ਅਕੈਡਮੀ Style Deep Analysis                    ║
    ║                                                               ║
    ║         Daily Meanings from Sri Guru Granth Sahib Ji          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def process_ang(ang_number: int, update_progress: bool = True, quick_mode: bool = False) -> bool:
    """
    Process a single Ang with deep scholarly analysis.
    
    Args:
        ang_number: The Ang number (1-1430)
        update_progress: Whether to update progress tracker
        quick_mode: If True, use faster, simpler analysis
        
    Returns:
        bool: True if successful
    """
    print(f"\n{'='*70}")
    print(f"📖 Processing Ang {ang_number} of {config.TOTAL_ANGS}")
    if quick_mode:
        print("   ⚡ Quick mode enabled")
    else:
        print("   📚 Deep Sach Khoj style analysis")
    print(f"{'='*70}")
    
    # Step 1: Fetch Gurbani
    print("\n📥 Step 1: Fetching Gurbani from BaniDB...")
    gurbani_data = gurbani_api.get_ang(ang_number)
    
    if gurbani_data is None:
        print("❌ Failed to fetch Gurbani data.")
        return False
    
    # Ensure Ang number is set
    if gurbani_data.get("angNumber", 0) == 0:
        gurbani_data["angNumber"] = ang_number
    
    # Show what we got
    print(f"   ✅ Ang: {gurbani_data['angNumber']}")
    print(f"   📜 Raag: {gurbani_data['metadata']['raag']}")
    print(f"   ✍️  Writer: {gurbani_data['metadata']['writer']}")
    print(f"   📝 Verses: {len(gurbani_data.get('allVerses', []))}")
    
    # Check transliteration
    trans = gurbani_data['mainVerse'].get('transliteration', '')
    if trans:
        print(f"   🔤 Transliteration: ✅ Available")
    else:
        print("   🔤 Transliteration: ⚠️ Not available")
    
    # Step 2: Generate AI meaning
    print("\n🤖 Step 2: Generating Scholarly Analysis...")
    
    if quick_mode:
        # Use simpler, faster analysis
        ai_response = ollama_client.generate_simple_meaning(gurbani_data)
    else:
        # Use full Sach Khoj style analysis
        print("   🧘 Entering deep vichar mode...")
        print("   ⏳ This may take 5-15 minutes for thorough analysis...")
        
        ai_result = ollama_client.generate_meaning_with_thinking(gurbani_data)
        ai_response = ai_result.get("full_response", "") or ai_result.get("response", "")
    
    if not ai_response:
        print("❌ Failed to generate AI meaning.")
        return False
    
    print(f"   ✅ Analysis complete!")
    print(f"   📄 Response: {len(ai_response)} characters")
    
    # Step 3: Format output
    print("\n📝 Step 3: Formatting output...")
    
    html_output = formatter.format_to_html(gurbani_data, ai_response)
    text_output = formatter.format_to_text(gurbani_data, ai_response)
    
    print("   ✅ Formatting complete!")
    
    # Step 4: Save files
    print("\n💾 Step 4: Saving files...")
    
    saved_files = storage.save_output(ang_number, html_output, text_output)
    
    # Step 5: Update progress
    if update_progress:
        print("\n📊 Step 5: Updating progress...")
        storage.mark_ang_as_processed(ang_number)
    
    # Success summary
    print(f"\n{'='*70}")
    print("✅ ਸਫਲ! SUCCESS! Ang processed and saved.")
    print(f"{'='*70}")
    
    print("\n📋 Summary:")
    print(f"   • Ang Number: {ang_number}")
    print(f"   • Raag: {gurbani_data['metadata']['raag']}")
    print(f"   • Writer: {gurbani_data['metadata']['writer']}")
    
    if saved_files.get("html"):
        print(f"   • HTML: {saved_files['html']}")
    if saved_files.get("text"):
        print(f"   • Text: {saved_files['text']}")
    
    return True


def main():
    """Main entry point."""
    print_banner()
    
    # Argument parser
    parser = argparse.ArgumentParser(
        description="Generate Sach Khoj Academy style Gurbani analysis"
    )
    
    parser.add_argument('--reset', action='store_true',
                        help='Reset progress to Ang 1')
    parser.add_argument('--ang', type=int,
                        help='Process specific Ang (1-1430)')
    parser.add_argument('--check', action='store_true',
                        help='Check Ollama connection only')
    parser.add_argument('--test-api', action='store_true',
                        help='Test Gurbani API only')
    parser.add_argument('--batch', type=int,
                        help='Process multiple Angs')
    parser.add_argument('--quick', action='store_true',
                        help='Quick mode - faster, simpler analysis')
    
    args = parser.parse_args()
    
    # Handle --test-api
    if args.test_api:
        print("🧪 Testing Gurbani API...")
        data = gurbani_api.get_ang(1)
        if data:
            print("✅ API working!")
            print(f"   Ang: {data['angNumber']}")
            print(f"   Verses: {len(data.get('allVerses', []))}")
        else:
            print("❌ API test failed")
        return
    
    # Handle --reset
    if args.reset:
        print("🔄 Resetting progress...")
        storage.reset_progress()
        print("✅ Progress reset. Run again to start from Ang 1.")
        return
    
    # Check Ollama
    print("🔌 Checking Ollama connection...")
    if not ollama_client.check_ollama_connection():
        print("\n❌ Cannot proceed without Ollama.")
        print(f"   Start Ollama: ollama serve")
        print(f"   Pull model: ollama pull {config.OLLAMA_MODEL}")
        sys.exit(1)
    
    # Handle --check
    if args.check:
        print("\n✅ All checks passed!")
        return
    
    # Ensure output directory
    storage.ensure_output_directory_exists()
    
    # Process Ang(s)
    if args.ang:
        # Specific Ang
        if args.ang < 1 or args.ang > config.TOTAL_ANGS:
            print(f"❌ Invalid Ang: {args.ang}. Must be 1-{config.TOTAL_ANGS}")
            sys.exit(1)
        process_ang(args.ang, update_progress=False, quick_mode=args.quick)
    
    elif args.batch:
        # Batch mode
        print(f"\n📚 Batch processing {args.batch} Angs...")
        for i in range(args.batch):
            next_ang = storage.get_next_ang()
            if next_ang is None:
                print("🎉 All Angs processed!")
                break
            print(f"\n[{i+1}/{args.batch}] Processing Ang {next_ang}...")
            if not process_ang(next_ang, update_progress=True, quick_mode=args.quick):
                print(f"⚠️ Failed at Ang {next_ang}. Stopping.")
                break
        print("\n✅ Batch complete!")
    
    else:
        # Normal mode - next Ang
        next_ang = storage.get_next_ang()
        if next_ang is None:
            print("🎉 All 1430 Angs have been processed!")
            print("   Use --reset to start over")
            return
        process_ang(next_ang, update_progress=True, quick_mode=args.quick)
    
    print("\n🙏 ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖ਼ਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫ਼ਤਹਿ 🙏")


if __name__ == "__main__":
    main()