"""
Formatter Module - FIXED VERSION
=================================
This module handles converting AI responses to HTML and plain text formats.

The HTML output is styled with a dark theme similar to the original n8n workflow.

FIXES APPLIED:
- Ensure Ang number displays correctly in title and content
- Better handling of empty transliteration
"""

import re
from datetime import datetime
from typing import Dict, Any


def markdown_to_html(text: str) -> str:
    """
    Convert Markdown-formatted text to HTML with styling.
    
    This function handles:
    - Headers (# ## ###)
    - Bold (**text**)
    - Italic (*text*)
    - Blockquotes (> text)
    - Tables (| col1 | col2 |)
    - Numbered lists (1. item)
    - Horizontal rules (---)
    
    Args:
        text: Markdown-formatted text
        
    Returns:
        str: HTML-formatted text with inline styles
    """
    if not text:
        return ""
    
    html = text
    
    # Convert headers (must be done before bold/italic to avoid conflicts)
    # ### Header 3
    html = re.sub(
        r'^### (.+)$',
        r'<h3 style="color: #a78bfa; margin-top: 25px; margin-bottom: 15px; font-size: 18px;">\1</h3>',
        html,
        flags=re.MULTILINE
    )
    
    # ## Header 2
    html = re.sub(
        r'^## (.+)$',
        r'<h2 style="color: #a78bfa; border-bottom: 2px solid #a78bfa; padding-bottom: 10px; margin-top: 30px; margin-bottom: 20px; font-size: 22px;">\1</h2>',
        html,
        flags=re.MULTILINE
    )
    
    # # Header 1
    html = re.sub(
        r'^# (.+)$',
        r'<h1 style="color: #a78bfa; font-size: 26px;">\1</h1>',
        html,
        flags=re.MULTILINE
    )
    
    # Convert bold text: **text** -> <strong>text</strong>
    html = re.sub(
        r'\*\*(.+?)\*\*',
        r'<strong style="color: #e2e8f0;">\1</strong>',
        html
    )
    
    # Convert italic text: *text* -> <em>text</em>
    html = re.sub(
        r'\*(.+?)\*',
        r'<em style="color: #cbd5e1;">\1</em>',
        html
    )
    
    # Convert blockquotes: > text
    html = re.sub(
        r'^> (.+)$',
        r'<blockquote style="border-left: 4px solid #a78bfa; margin: 20px 0; padding: 15px 25px; background: #1e1e2e; color: #e2e8f0; border-radius: 0 8px 8px 0;">\1</blockquote>',
        html,
        flags=re.MULTILINE
    )
    
    # Convert horizontal rules: ---
    html = re.sub(
        r'^---$',
        r'<hr style="border: none; border-top: 2px solid #374151; margin: 30px 0;">',
        html,
        flags=re.MULTILINE
    )
    
    # Convert numbered lists: 1. item
    html = re.sub(
        r'^\d+\.\s+(.+)$',
        r'<li style="margin: 10px 0; color: #e2e8f0;">\1</li>',
        html,
        flags=re.MULTILINE
    )
    
    # Convert tables (basic support)
    html = convert_tables_to_html(html)
    
    # Convert line breaks
    html = html.replace('\n\n', '</p><p style="margin: 18px 0; color: #e2e8f0;">')
    html = html.replace('\n', '<br>')
    
    return html


def convert_tables_to_html(text: str) -> str:
    """
    Convert Markdown tables to HTML tables.
    
    Markdown table format:
    | Header 1 | Header 2 |
    |----------|----------|
    | Cell 1   | Cell 2   |
    
    Args:
        text: Text potentially containing Markdown tables
        
    Returns:
        str: Text with tables converted to HTML
    """
    lines = text.split('\n')
    result = []
    in_table = False
    table_rows = []
    
    for line in lines:
        stripped = line.strip()
        
        # Check if this line is part of a table (starts and ends with |)
        if stripped.startswith('|') and stripped.endswith('|'):
            # Skip separator rows (like |---|---|)
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue
            
            if not in_table:
                in_table = True
                table_rows = []
            
            table_rows.append(stripped)
        else:
            # If we were in a table, finalize it
            if in_table:
                result.append(build_table_html(table_rows))
                in_table = False
                table_rows = []
            result.append(line)
    
    # Handle table at end of text
    if in_table and table_rows:
        result.append(build_table_html(table_rows))
    
    return '\n'.join(result)


def build_table_html(rows: list) -> str:
    """
    Build an HTML table from parsed rows.
    
    Args:
        rows: List of table row strings (| col1 | col2 |)
        
    Returns:
        str: HTML table string
    """
    table_html = '''<table style="border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 14px; background: #1e1e2e; border-radius: 8px; overflow: hidden;">'''
    
    for row_index, row in enumerate(rows):
        # Split the row by | and filter empty cells
        cells = [cell.strip() for cell in row.split('|') if cell.strip()]
        
        table_html += '<tr>'
        
        for cell in cells:
            if row_index == 0:
                # First row is header
                table_html += f'''<th style="border: 1px solid #374151; padding: 14px; background: #7c3aed; color: white; text-align: left; font-weight: 600;">{cell}</th>'''
            else:
                # Alternate row colors for readability
                bg_color = '#252536' if row_index % 2 == 0 else '#1e1e2e'
                table_html += f'''<td style="border: 1px solid #374151; padding: 12px; background: {bg_color}; color: #e2e8f0;">{cell}</td>'''
        
        table_html += '</tr>'
    
    table_html += '</table>'
    return table_html


def format_to_html(gurbani_data: Dict[str, Any], ai_response: str, include_thinking: bool = True) -> str:
    """
    Create the full HTML page for the Gurbani meaning.
    
    This function generates a complete, styled HTML page that includes:
    - Header with Ik Onkar symbol
    - Gurmukhi verse
    - Transliteration
    - Raag and Writer info
    - AI-generated meaning
    - Footer with links
    
    FIXED: Ang number now displays correctly
    
    Args:
        gurbani_data: Parsed Gurbani data
        ai_response: The AI-generated meaning
        include_thinking: Whether to include AI's thinking process
        
    Returns:
        str: Complete HTML page
    """
    # Extract data safely with proper fallbacks
    ang_number = gurbani_data.get("angNumber", 0)
    
    # Ensure ang_number is valid
    if not ang_number or ang_number == 0:
        print("   ⚠️ Warning: Ang number is 0 or missing in formatter")
    
    date = gurbani_data.get("date", datetime.now().strftime("%B %d, %Y"))
    main_verse = gurbani_data.get("mainVerse", {})
    metadata = gurbani_data.get("metadata", {})
    
    # Get verse content
    gurmukhi = main_verse.get("unicode", "") or main_verse.get("gurmukhi", "")
    transliteration = main_verse.get("transliteration", "")
    raag = metadata.get("raag", "Unknown")
    writer = metadata.get("writer", "Unknown")
    
    # Handle empty transliteration
    if not transliteration or transliteration.strip() == "":
        transliteration_html = '<em style="color: #666;">Transliteration not available for this Ang</em>'
    else:
        transliteration_html = transliteration
    
    # Convert AI response to HTML
    ai_response_html = markdown_to_html(ai_response)
    
    # Build the complete HTML page
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gurbani Wisdom - Ang {ang_number}</title>
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; color: #e2e8f0; margin: 0; padding: 0; background: #0f0f1a;">
    
    <div style="max-width: 680px; margin: 0 auto; padding: 20px;">
        
        <!-- HEADER -->
        <div style="background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 50%, #7c3aed 100%); color: white; padding: 40px 35px; text-align: center; border-radius: 16px 16px 0 0;">
            <div style="font-size: 60px; margin-bottom: 15px; text-shadow: 0 4px 15px rgba(0,0,0,0.3);">ੴ</div>
            <h1 style="margin: 12px 0; font-size: 28px; font-weight: 600; letter-spacing: 1px;">Daily Gurbani Wisdom</h1>
            <p style="margin: 6px 0; opacity: 0.95; font-size: 15px;">{date}</p>
            <p style="margin: 6px 0; opacity: 0.95; font-size: 15px;">Ang {ang_number} of 1430</p>
        </div>
        
        <!-- CONTENT -->
        <div style="background: #1a1a2e; padding: 40px; border-radius: 0 0 16px 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.4);">
            
            <!-- GURMUKHI BOX - BLACK WITH WHITE TEXT -->
            <div style="font-size: 24px; text-align: center; background: #000000; color: #ffffff; padding: 35px 30px; border-left: 6px solid #a78bfa; border-right: 6px solid #a78bfa; margin: 25px 0; line-height: 2.2; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); letter-spacing: 1px; white-space: pre-wrap;">
{gurmukhi}
            </div>
            
            <!-- TRANSLITERATION -->
            <div style="font-style: italic; color: #a1a1aa; text-align: center; margin: 20px 0; padding: 20px; background: #252536; border-radius: 10px; font-size: 16px; line-height: 1.8; white-space: pre-wrap;">
{transliteration_html}
            </div>
            
            <!-- RAAG AND WRITER -->
            <table style="width: 100%; margin: 30px 0; padding: 25px 0; background: #252536; border-radius: 12px; border: 1px solid #374151; border-collapse: collapse;">
                <tr>
                    <!-- RAAG - LEFT -->
                    <td style="text-align: left; padding: 20px 30px; width: 50%; vertical-align: top;">
                        <div style="font-size: 11px; color: #a78bfa; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-bottom: 8px;">Raag</div>
                        <div style="font-size: 18px; color: #ffffff; font-weight: 600;">{raag}</div>
                    </td>
                    
                    <!-- WRITER - RIGHT -->
                    <td style="text-align: right; padding: 20px 30px; width: 50%; vertical-align: top;">
                        <div style="font-size: 11px; color: #a78bfa; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-bottom: 8px;">Writer</div>
                        <div style="font-size: 18px; color: #ffffff; font-weight: 600;">{writer}</div>
                    </td>
                </tr>
            </table>
            
            <!-- DIVIDER -->
            <div style="height: 4px; background: linear-gradient(to right, #7c3aed, #a78bfa, #7c3aed); margin: 35px 0; border-radius: 2px;"></div>
            
            <!-- AI RESPONSE -->
            <div style="background: #16162a; padding: 35px; border-radius: 14px; margin-top: 30px; border: 1px solid #374151; color: #e2e8f0;">
                <p style="margin: 18px 0; color: #e2e8f0;">
                {ai_response_html}
                </p>
            </div>
            
            <!-- FOOTER -->
            <div style="text-align: center; margin-top: 35px; padding: 30px; color: #a1a1aa; font-size: 14px; background: #252536; border-radius: 12px;">
                <p style="font-size: 16px; color: #e2e8f0; margin: 10px 0;">🙏 Waheguru Ji Ka Khalsa, Waheguru Ji Ki Fateh 🙏</p>
                <p style="margin: 15px 0;">
                    <a href="https://www.sikhitothemax.org/ang?ang={ang_number}&source=G" style="color: #a78bfa; text-decoration: none; font-weight: 600;">📖 View on SikhiToTheMax</a>
                </p>
            </div>
            
        </div>
        
    </div>
    
</body>
</html>'''
    
    return html


def format_to_text(gurbani_data: Dict[str, Any], ai_response: str) -> str:
    """
    Create a plain text version of the Gurbani meaning.
    
    This is useful for:
    - Telegram messages
    - Console output
    - Simple text file storage
    
    Args:
        gurbani_data: Parsed Gurbani data
        ai_response: The AI-generated meaning
        
    Returns:
        str: Plain text formatted output
    """
    # Extract data safely
    ang_number = gurbani_data.get("angNumber", 0)
    date = gurbani_data.get("date", datetime.now().strftime("%B %d, %Y"))
    main_verse = gurbani_data.get("mainVerse", {})
    metadata = gurbani_data.get("metadata", {})
    
    gurmukhi = main_verse.get("unicode", "") or main_verse.get("gurmukhi", "")
    transliteration = main_verse.get("transliteration", "")
    raag = metadata.get("raag", "Unknown")
    writer = metadata.get("writer", "Unknown")
    
    # Handle empty transliteration
    if not transliteration or transliteration.strip() == "":
        transliteration = "(Transliteration not available)"
    
    # Build plain text output
    text = f'''ੴ Daily Gurbani Wisdom 🙏

📅 {date}
📖 Ang {ang_number}/1430

═══════════════════════════════════════════

Gurmukhi:
{gurmukhi}

Transliteration:
{transliteration}

Raag: {raag}
Writer: {writer}

═══════════════════════════════════════════

{ai_response}

═══════════════════════════════════════════

🔗 sikhitothemax.org/ang?ang={ang_number}&source=G

🙏 Waheguru Ji Ka Khalsa, Waheguru Ji Ki Fateh 🙏'''
    
    return text


# Test function
if __name__ == "__main__":
    print("Testing formatter...")
    
    # Test with sample data
    test_data = {
        "angNumber": 1,  # Should show as 1, not 0
        "date": "January 6, 2026",
        "mainVerse": {
            "unicode": "ੴ ਸਤਿ ਨਾਮੁ",
            "transliteration": "Ik Oankaar Sat Naam"
        },
        "metadata": {
            "raag": "ਜਪ",
            "writer": "Guru Nanak Dev Ji"
        }
    }
    
    test_response = """## Word-by-Word Meanings
| Word | Meaning |
|------|---------|
| ੴ | One Universal Creator |
| ਸਤਿ | Truth |

## Spiritual Meaning
This is a **test** of the *formatting* system."""
    
    html = format_to_html(test_data, test_response)
    
    # Check if Ang 1 appears correctly
    if "Ang 1 of 1430" in html:
        print("✅ Ang number displays correctly!")
    else:
        print("❌ Ang number not displaying correctly")
    
    print(f"HTML length: {len(html)} characters")