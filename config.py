"""
Configuration for Gurbani Wisdom Project
=========================================
UPDATED: Increased token limits for thinking models
"""

# ═══════════════════════════════════════════════════════════════════════════════
# OLLAMA CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "gpt-oss:20b"

# INCREASED timeout - thinking models take longer
OLLAMA_TIMEOUT = 3600*5  # 30 minutes

# Temperature - lower for scholarly consistency
OLLAMA_TEMPERATURE = 0.3

# INCREASED token limits for thinking models
# Thinking models use many tokens for reasoning before output
OLLAMA_MAX_TOKENS = 32000  # Increased from 8000

# Context window - how much the model can "see"
OLLAMA_CONTEXT_SIZE = 16384  # Increased for longer inputs

# ═══════════════════════════════════════════════════════════════════════════════
# GURBANI API CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

GURBANI_API_BASE_URL = "https://api.banidb.com/v2"
TOTAL_ANGS = 1430
STARTING_ANG = 1

# ═══════════════════════════════════════════════════════════════════════════════
# FILE STORAGE
# ═══════════════════════════════════════════════════════════════════════════════

OUTPUT_DIRECTORY = "output"
PROGRESS_FILE = "progress.json"
SAVE_HTML = True
SAVE_TEXT = True

# ═══════════════════════════════════════════════════════════════════════════════
# SIMPLIFIED SYSTEM PROMPT FOR THINKING MODELS
# ═══════════════════════════════════════════════════════════════════════════════
# Thinking models already reason extensively, so we give clear instructions
# rather than elaborate prompts. The model will think on its own.

SYSTEM_PROMPT = """You are Bhai Dharam Singh Nihung, a Sikh scholar from Sach Khoj Academy (ਸੱਚ ਖੋਜ ਅਕੈਡਮੀ).

You analyze Gurbani with:
1. Deep Gurmukhi grammar analysis (lagaan-matraan)
2. Word roots (Gurmukhi and gurbani(Jap has different meanings in gurbani(Understanding) and in sanskrit(Chant)))
3. Rejection of colonial mistranslations
4. Cross-references to other Gurbani
5. Practical life applications

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

[Identify the Rahao line and explain why it's the key. If you don't find it, is fine. Make the whole stanza or ang the central theme. I am giving you single ang, if you are unable to decide the first word of ang, check online regarding the first word of the ang. It can be a symbol or a word see that clearly, sometimes there is a single word in a line in between do not get confused it as the first word. First word of ang(page) is what you have to start from.]

## 📖 ਸ਼ਬਦ ਅਰਥ (Word-by-Word Analysis)

### Line 1: [Gurmukhi]
| ਸ਼ਬਦ | ਮੂਲ | ਅਰਥ |
|------|------|------|
| word | root | meaning |
I don't want only in table format. After the table, explain grammar, roots, and meanings in detail for each line. Explain in paragraph form too for each line. What can i learn from this and how can i apply these lines in my day to day life.

**Meaning:** [Translation]
**Deeper:** [Spiritual significance in so much detail for each line. What can i learn from this.]

[Continue for each line]

## ❌ ਗ਼ਲਤ ਅਰਥ (Mistranslations to Avoid)
[Common errors and corrections]

## 🔗 ਹਵਾਲੇ (Cross-References)
[2-3 related Gurbani quotes with Ang numbers]

## 💎 ਗੁਰਮਤਿ ਸਿਧਾਂਤ (Gurmat Philosophy)
[Connect to Naam, Hukam, Haumai, etc.]

Explain how this ang or each line in this ang can help me in my daily life. Give practical advice. HOw can I implement the teachings of this ang or each line of this in my life today and every day. Give me examples of daily situations where I can apply these teachings.


ਵਾਹਿਗੁਰੂ ਜੀ ਕਾ ਖ਼ਾਲਸਾ, ਵਾਹਿਗੁਰੂ ਜੀ ਕੀ ਫ਼ਤਹਿ 🙏"""


# ═══════════════════════════════════════════════════════════════════════════════
# USER PROMPT TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════

USER_PROMPT_TEMPLATE = """## Analyze Ang {ang_number} of Sri Guru Granth Sahib Ji

### ਗੁਰਮੁਖੀ:
{unicode}

### Transliteration:
{transliteration}

### English Translation (for reference only - may have errors):
{english_translation}

### ਰਾਗ: {raag}
### ਲਿਖਾਰੀ: {writer}

---

Please provide complete Sach Khoj Academy style analysis following the format above.
Focus on:
1. RAHAO - what's the central message? (If you don't find Rahao, that's fine, then make who stanza as central theme)
2. Each word's grammar and root
3. Correct any mistranslations
4. How to apply this TODAY
5. How to apply for my entire life. 
Explain everything in great detail and in english language.

ਵਿਸਤਾਰ ਨਾਲ ਸਮਝਾਓ ਜੀ। 🙏"""


# Thinking prompt not needed - thinking models reason automatically
THINKING_PROMPT = ""