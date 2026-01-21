"""
Gurbani API Module - FIXED VERSION
===================================
This module fetches Gurbani data from the BaniDB API.

BaniDB is a free, open-source API that provides access to:
- Sri Guru Granth Sahib Ji
- Various translations
- Transliterations
- Metadata (Raag, Writer, etc.)

API Documentation: https://api.banidb.com/

FIXES APPLIED:
- Fixed Ang number extraction (was showing 0)
- Fixed transliteration extraction (was empty)
- Better error handling
"""

import requests
from typing import Optional, Dict, Any
from datetime import datetime

# Import our configuration
import config


def fetch_ang_data(ang_number: int) -> Optional[Dict[str, Any]]:
    """
    Fetch data for a specific Ang (page) from the Gurbani API.
    
    This function makes an HTTP GET request to the BaniDB API to retrieve:
    - All verses on that Ang
    - Gurmukhi text
    - Unicode text
    - Transliterations
    - English translations
    - Metadata (Raag, Writer)
    
    Args:
        ang_number: The Ang number to fetch (1 to 1430)
        
    Returns:
        dict or None: The API response data, or None if failed
    """
    # Construct the API URL
    # The '1' at the end specifies the source (1 = Sri Guru Granth Sahib Ji)
    api_url = f"{config.GURBANI_API_BASE_URL}/angs/{ang_number}/1"
    
    print(f"🌐 Fetching Ang {ang_number} from BaniDB API...")
    print(f"   URL: {api_url}")
    
    try:
        # Make the HTTP GET request
        # timeout prevents the request from hanging indefinitely
        response = requests.get(api_url, timeout=30)
        
        # Check if the request was successful (status code 200)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Add the requested ang_number to the response for reference
        # This ensures we always have the correct Ang number
        data['_requested_ang'] = ang_number
        
        print(f"✅ Successfully fetched Ang {ang_number}")
        return data
        
    except requests.exceptions.Timeout:
        # Handle timeout errors
        print(f"❌ Timeout: API took too long to respond for Ang {ang_number}")
        return None
        
    except requests.exceptions.ConnectionError:
        # Handle connection errors (no internet, API down, etc.)
        print(f"❌ Connection Error: Could not reach the Gurbani API")
        print("   Check your internet connection")
        return None
        
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (404, 500, etc.)
        print(f"❌ HTTP Error: {e}")
        return None
        
    except Exception as e:
        # Handle any other unexpected errors
        print(f"❌ Unexpected error fetching Ang {ang_number}: {e}")
        return None


def extract_transliteration(verse: Dict[str, Any]) -> str:
    """
    Extract transliteration from a verse object.
    
    The BaniDB API has transliteration in a nested structure:
    verse["transliteration"]["english"] or verse["transliteration"]["en"]
    
    This function safely extracts it.
    
    Args:
        verse: A verse object from the API response
        
    Returns:
        str: The English transliteration, or empty string if not found
    """
    # Get the transliteration object
    trans_obj = verse.get("transliteration", {})
    
    # If transliteration is a string (old API format), return it directly
    if isinstance(trans_obj, str):
        return trans_obj
    
    # If it's a dictionary (new API format), get the English version
    if isinstance(trans_obj, dict):
        # Try 'english' first, then 'en' as fallback
        transliteration = trans_obj.get("english", "") or trans_obj.get("en", "")
        return transliteration
    
    return ""


def extract_translation(verse: Dict[str, Any]) -> str:
    """
    Extract English translation from a verse object.
    
    The BaniDB API has multiple translation sources.
    We prefer 'bdb' (BaniDB's own translation).
    
    Args:
        verse: A verse object from the API response
        
    Returns:
        str: The English translation, or empty string if not found
    """
    # Get the translation object
    trans_obj = verse.get("translation", {})
    
    # Get English translations
    en_trans = trans_obj.get("en", {})
    
    # If en_trans is a string, return it
    if isinstance(en_trans, str):
        return en_trans
    
    # If it's a dict, try different sources in order of preference
    if isinstance(en_trans, dict):
        # Try bdb first (BaniDB), then ms (Manmohan Singh), then ssk
        return en_trans.get("bdb", "") or en_trans.get("ms", "") or en_trans.get("ssk", "")
    
    return ""


def parse_ang_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and structure the raw API response into a cleaner format.
    
    The BaniDB API returns a lot of data. This function extracts
    the parts we need and organizes them nicely.
    
    FIXED: Now correctly extracts:
    - Ang number (from _requested_ang or pageinfo.pageno)
    - Transliteration (from transliteration.english)
    - All other fields
    
    Args:
        raw_data: The raw JSON response from the API
        
    Returns:
        dict: Structured data with verse, translations, and metadata
    """
    # Initialize our structured data container
    parsed_data = {
        "angNumber": None,
        "date": None,
        "mainVerse": {
            "gurmukhi": "",
            "unicode": "",
            "transliteration": "",
            "translation": {
                "english": ""
            }
        },
        "metadata": {
            "raag": "Unknown",
            "writer": "Unknown"
        },
        "allVerses": []  # Store all verses from the Ang
    }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FIX 1: Get the Ang number correctly
    # ═══════════════════════════════════════════════════════════════════════════
    # First try to use the requested Ang number (most reliable)
    # Then fall back to pageinfo.pageno
    page_info = raw_data.get("pageinfo", {})
    
    # Use _requested_ang if available (we added this in fetch_ang_data)
    requested_ang = raw_data.get("_requested_ang")
    api_pageno = page_info.get("pageno") or page_info.get("page")
    
    # Use requested_ang first, then api_pageno, default to 0
    if requested_ang:
        parsed_data["angNumber"] = requested_ang
    elif api_pageno:
        parsed_data["angNumber"] = api_pageno
    else:
        parsed_data["angNumber"] = 0
        print("   ⚠️ Warning: Could not determine Ang number from API")
    
    # Add current date
    parsed_data["date"] = datetime.now().strftime("%B %d, %Y")
    
    # Get all verses from this Ang
    verses = raw_data.get("page", [])
    
    if not verses:
        print("   ⚠️ Warning: No verses found in API response")
        return parsed_data
    
    print(f"   📜 Found {len(verses)} verses on this Ang")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FIX 2: Process each verse and extract transliteration correctly
    # ═══════════════════════════════════════════════════════════════════════════
    for verse in verses:
        # Get the verse object (contains gurmukhi, unicode)
        verse_obj = verse.get("verse", {})
        
        # Extract transliteration using our helper function
        transliteration = extract_transliteration(verse)
        
        # Extract translation using our helper function
        translation = extract_translation(verse)
        
        # Build verse data
        verse_data = {
            "gurmukhi": verse_obj.get("gurmukhi", ""),
            "unicode": verse_obj.get("unicode", ""),
            "transliteration": transliteration,  # Now correctly extracted!
            "translation_english": translation,
            "raag": verse.get("raag", {}).get("unicode", "") or verse.get("raag", {}).get("english", "Unknown"),
            "writer": verse.get("writer", {}).get("english", "Unknown")
        }
        
        parsed_data["allVerses"].append(verse_data)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Set metadata from first verse
    # ═══════════════════════════════════════════════════════════════════════════
    if parsed_data["allVerses"]:
        first_verse_data = parsed_data["allVerses"][0]
        parsed_data["metadata"]["raag"] = first_verse_data["raag"]
        parsed_data["metadata"]["writer"] = first_verse_data["writer"]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Combine all verses into main verse (for complete Ang context)
    # ═══════════════════════════════════════════════════════════════════════════
    # Combine Unicode (Gurmukhi script)
    combined_unicode = "\n".join([
        v["unicode"] for v in parsed_data["allVerses"] if v["unicode"]
    ])
    
    # Combine Transliteration - NOW SHOULD WORK!
    combined_transliteration = "\n".join([
        v["transliteration"] for v in parsed_data["allVerses"] if v["transliteration"]
    ])
    
    # Combine English translations
    combined_english = "\n".join([
        v["translation_english"] for v in parsed_data["allVerses"] if v["translation_english"]
    ])
    
    # Set the combined values
    parsed_data["mainVerse"]["unicode"] = combined_unicode
    parsed_data["mainVerse"]["gurmukhi"] = combined_unicode  # Use unicode as fallback
    parsed_data["mainVerse"]["transliteration"] = combined_transliteration
    parsed_data["mainVerse"]["translation"]["english"] = combined_english
    
    # Debug output to verify transliteration
    if combined_transliteration:
        print(f"   ✅ Transliteration extracted: {len(combined_transliteration)} characters")
    else:
        print("   ⚠️ Warning: No transliteration found in API response")
    
    return parsed_data


def get_ang(ang_number: int) -> Optional[Dict[str, Any]]:
    """
    Main function to get a parsed Ang.
    
    This is the function you'll call from the main script.
    It combines fetching and parsing in one step.
    
    Args:
        ang_number: The Ang number to fetch (1 to 1430)
        
    Returns:
        dict or None: Parsed Ang data, or None if failed
    """
    # First, fetch the raw data
    raw_data = fetch_ang_data(ang_number)
    
    if raw_data is None:
        return None
    
    # Then, parse it into our structured format
    parsed_data = parse_ang_data(raw_data)
    
    return parsed_data


# ═══════════════════════════════════════════════════════════════════════════════
# Debug/Test function - run this file directly to test the API
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Gurbani API - Fetching Ang 1")
    print("=" * 60)
    
    # Test fetching Ang 1 (the first page)
    test_ang = get_ang(1)
    
    if test_ang:
        print("\n📜 Test Results:")
        print(f"   Ang Number: {test_ang['angNumber']}")
        print(f"   Raag: {test_ang['metadata']['raag']}")
        print(f"   Writer: {test_ang['metadata']['writer']}")
        print(f"   Total Verses: {len(test_ang['allVerses'])}")
        
        print("\n📖 Unicode (first 200 chars):")
        print(f"   {test_ang['mainVerse']['unicode'][:200]}...")
        
        print("\n🔤 Transliteration (first 200 chars):")
        trans = test_ang['mainVerse']['transliteration']
        if trans:
            print(f"   {trans[:200]}...")
        else:
            print("   ⚠️ NO TRANSLITERATION FOUND!")
            
        print("\n📝 English Translation (first 200 chars):")
        print(f"   {test_ang['mainVerse']['translation']['english'][:200]}...")
        
        # Debug: Show raw structure of first verse
        print("\n🔍 Debug - First verse raw structure:")
        if test_ang['allVerses']:
            first = test_ang['allVerses'][0]
            print(f"   transliteration: '{first['transliteration'][:100] if first['transliteration'] else 'EMPTY'}'")
    else:
        print("❌ Test failed - could not fetch data")
    
    print("\n" + "=" * 60)  