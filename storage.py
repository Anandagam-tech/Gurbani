"""
Storage Module for Gurbani Wisdom Project
==========================================
This module handles:
1. Tracking which Ang we're on (so we don't repeat)
2. Saving output files (HTML and text)
3. Creating necessary directories
"""

import os
import json
from datetime import datetime
from typing import Optional

# Import our configuration settings
import config


def ensure_output_directory_exists() -> None:
    """
    Create the output directory if it doesn't exist.
    
    This function checks if the output folder exists, and creates it if not.
    It's called at the start of the script to ensure we have a place to save files.
    
    Returns:
        None
    """
    # os.makedirs creates the directory and any parent directories needed
    # exist_ok=True means don't raise an error if directory already exists
    if not os.path.exists(config.OUTPUT_DIRECTORY):
        os.makedirs(config.OUTPUT_DIRECTORY, exist_ok=True)
        print(f"✅ Created output directory: {config.OUTPUT_DIRECTORY}")


def load_progress() -> dict:
    """
    Load the current progress from the progress file.
    
    The progress file is a JSON file that stores:
    - current_ang: The next Ang number to process
    - last_processed: Timestamp of last processing
    - total_processed: How many Angs we've done
    
    Returns:
        dict: Progress data with current_ang and other info
    """
    # Check if progress file exists
    if os.path.exists(config.PROGRESS_FILE):
        try:
            # Open the file and read the JSON data
            with open(config.PROGRESS_FILE, 'r', encoding='utf-8') as file:
                progress = json.load(file)
                print(f"📖 Loaded progress: Currently on Ang {progress.get('current_ang', config.STARTING_ANG)}")
                return progress
        except json.JSONDecodeError:
            # If the file is corrupted, start fresh
            print("⚠️ Progress file corrupted, starting fresh")
    
    # If no progress file exists, create initial progress
    initial_progress = {
        "current_ang": config.STARTING_ANG,  # Start from the configured starting Ang
        "last_processed": None,               # No processing done yet
        "total_processed": 0,                 # Counter for total Angs processed
        "started_at": datetime.now().isoformat()  # When we started
    }
    
    print(f"🆕 Starting fresh from Ang {config.STARTING_ANG}")
    return initial_progress


def save_progress(progress: dict) -> None:
    """
    Save the current progress to the progress file.
    
    This is called after successfully processing each Ang to remember our position.
    
    Args:
        progress: Dictionary containing current progress data
        
    Returns:
        None
    """
    # Write the progress data as JSON to the file
    with open(config.PROGRESS_FILE, 'w', encoding='utf-8') as file:
        # indent=2 makes the JSON file human-readable
        json.dump(progress, file, indent=2, ensure_ascii=False)
    
    print(f"💾 Progress saved: Next Ang will be {progress.get('current_ang', 'unknown')}")


def get_next_ang() -> Optional[int]:
    """
    Get the next Ang number to process.
    
    This function:
    1. Loads the current progress
    2. Returns the next Ang number to process
    3. Returns None if we've processed all 1430 Angs
    
    Returns:
        int or None: The next Ang number, or None if finished
    """
    progress = load_progress()
    current_ang = progress.get("current_ang", config.STARTING_ANG)
    
    # Check if we've finished all Angs
    if current_ang > config.TOTAL_ANGS:
        print("🎉 All 1430 Angs have been processed!")
        return None
    
    return current_ang


def mark_ang_as_processed(ang_number: int) -> None:
    """
    Mark an Ang as processed and update progress.
    
    This function:
    1. Loads current progress
    2. Increments the Ang counter
    3. Updates timestamps
    4. Saves the updated progress
    
    Args:
        ang_number: The Ang number that was just processed
        
    Returns:
        None
    """
    # Load current progress
    progress = load_progress()
    
    # Update the progress data
    progress["current_ang"] = ang_number + 1  # Move to next Ang
    progress["last_processed"] = datetime.now().isoformat()  # Record timestamp
    progress["total_processed"] = progress.get("total_processed", 0) + 1  # Increment counter
    progress["last_ang_done"] = ang_number  # Remember which Ang we just did
    
    # Save the updated progress
    save_progress(progress)


def save_output(ang_number: int, html_content: str, text_content: str) -> dict:
    """
    Save the generated meaning to files.
    
    This function saves both HTML and text versions of the output.
    
    Args:
        ang_number: The Ang number (used in filename)
        html_content: The formatted HTML content
        text_content: The plain text content
        
    Returns:
        dict: Paths to the saved files
    """
    # Ensure output directory exists
    ensure_output_directory_exists()
    
    # Create filenames with zero-padded Ang numbers for proper sorting
    # e.g., ang_001.html, ang_099.html, ang_1430.html
    base_filename = f"ang_{ang_number:04d}"  # :04d means 4 digits with leading zeros
    
    saved_files = {}
    
    # Save HTML version if enabled
    if config.SAVE_HTML:
        html_path = os.path.join(config.OUTPUT_DIRECTORY, f"{base_filename}.html")
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        saved_files["html"] = html_path
        print(f"📄 Saved HTML: {html_path}")
    
    # Save text version if enabled
    if config.SAVE_TEXT:
        text_path = os.path.join(config.OUTPUT_DIRECTORY, f"{base_filename}.txt")
        with open(text_path, 'w', encoding='utf-8') as file:
            file.write(text_content)
        saved_files["text"] = text_path
        print(f"📄 Saved Text: {text_path}")
    
    return saved_files


def reset_progress() -> None:
    """
    Reset progress to start from the beginning.
    
    Use this if you want to reprocess all Angs from the start.
    
    Returns:
        None
    """
    if os.path.exists(config.PROGRESS_FILE):
        os.remove(config.PROGRESS_FILE)
        print("🔄 Progress reset! Will start from Ang 1 on next run.")
    else:
        print("ℹ️ No progress file found. Already at start.")