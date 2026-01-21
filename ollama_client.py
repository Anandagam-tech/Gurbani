"""
Ollama Client Module - FIXED FOR THINKING MODELS
=================================================
Fixed to handle models like gpt-oss that put content in 'thinking' field.
"""

import requests
import re
import json
from typing import Optional, Dict, Any

import config


def check_ollama_connection() -> bool:
    """Check if Ollama server is running."""
    try:
        response = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=10)
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            print(f"✅ Connected to Ollama")
            print(f"   📦 Available models: {model_names}")
            
            if any(config.OLLAMA_MODEL in name for name in model_names):
                print(f"   ✅ Model '{config.OLLAMA_MODEL}' is ready")
            else:
                print(f"   ⚠️ Model '{config.OLLAMA_MODEL}' not found!")
            
            return True
        return False
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Ollama at {config.OLLAMA_BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def build_full_prompt(gurbani_data: Dict[str, Any]) -> str:
    """Build the complete prompt for deep Gurbani analysis."""
    
    user_prompt = config.USER_PROMPT_TEMPLATE.format(
        ang_number=gurbani_data.get("angNumber", "?"),
        unicode=gurbani_data["mainVerse"].get("unicode", "N/A"),
        transliteration=gurbani_data["mainVerse"].get("transliteration", "Not available"),
        english_translation=gurbani_data["mainVerse"]["translation"].get("english", "Not available"),
        raag=gurbani_data["metadata"].get("raag", "Unknown"),
        writer=gurbani_data["metadata"].get("writer", "Unknown")
    )
    
    # For thinking models, we want a cleaner prompt
    # The model will think on its own, we just need to ask clearly
    full_prompt = f"""{config.SYSTEM_PROMPT}

---

{user_prompt}

Please provide your complete analysis now."""
    
    return full_prompt


def extract_response_from_thinking_model(result: Dict[str, Any]) -> str:
    """
    Extract response from a thinking/reasoning model.
    
    These models (like gpt-oss, DeepSeek R1, QwQ) put their output in:
    - 'thinking' field (the reasoning process)
    - 'response' field (the final answer - often empty or partial)
    
    We combine both for the full output.
    
    Args:
        result: The JSON response from Ollama
        
    Returns:
        str: The combined thinking + response text
    """
    thinking = result.get("thinking", "")
    response = result.get("response", "")
    
    # If thinking has content, use it (possibly with response)
    if thinking:
        if response:
            # Both have content - combine them
            return f"{thinking}\n\n---\n\n{response}"
        else:
            # Only thinking has content
            return thinking
    
    # Fallback to response if no thinking
    if response:
        return response
    
    # Try other common fields
    for field in ["content", "text", "output", "message", "generated_text"]:
        if field in result and result[field]:
            value = result[field]
            if isinstance(value, str) and value:
                return value
            if isinstance(value, dict) and "content" in value:
                return value["content"]
    
    return ""


def generate_meaning_with_thinking(gurbani_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate deep scholarly meaning for the Gurbani.
    
    Optimized for thinking/reasoning models that use the 'thinking' field.
    """
    
    full_prompt = build_full_prompt(gurbani_data)
    
    print(f"\n🤖 Sending to Ollama ({config.OLLAMA_MODEL})...")
    print("   📚 Requesting Sach Khoj Academy style deep vichar...")
    print("   🧠 Using thinking/reasoning model - this takes time...")
    print("   ⏳ Please wait for thorough analysis...")
    
    # For thinking models, we need MORE tokens
    # The model spends a lot of tokens on reasoning
    payload = {
        "model": config.OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": config.OLLAMA_TEMPERATURE,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 16000,  # INCREASED for thinking models
            "repeat_penalty": 1.1,
            "num_ctx": 16384,      # INCREASED context window
        }
    }
    
    try:
        response = requests.post(
            f"{config.OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=config.OLLAMA_TIMEOUT
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Get timing stats
        total_duration = result.get("total_duration", 0) / 1e9
        eval_count = result.get("eval_count", 0)
        done_reason = result.get("done_reason", "unknown")
        
        print(f"\n   ⏱️ Time: {total_duration:.1f}s ({total_duration/60:.1f} min)")
        print(f"   📝 Tokens: {eval_count}")
        print(f"   🏁 Done reason: {done_reason}")
        
        # Check if we hit token limit
        if done_reason == "length":
            print("   ⚠️ Warning: Hit token limit! Response may be incomplete.")
            print("   💡 Consider increasing num_predict in the code.")
        
        # Extract content from thinking model format
        thinking_content = result.get("thinking", "")
        response_content = result.get("response", "")
        
        print(f"   🧠 Thinking length: {len(thinking_content)} chars")
        print(f"   💬 Response length: {len(response_content)} chars")
        
        # Combine thinking and response
        generated_text = extract_response_from_thinking_model(result)
        
        print(f"   📄 Total extracted: {len(generated_text)} chars")
        
        if not generated_text:
            print("\n   ❌ No content extracted!")
            # Save debug file
            with open("debug_response.json", 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            print("   📁 Saved debug to: debug_response.json")
            return {"thinking": "", "response": "", "full_response": ""}
        
        print(f"\n   ✅ Vichar complete!")
        
        # Show preview
        preview = generated_text[:200].replace('\n', ' ')
        print(f"   👀 Preview: {preview}...")
        
        return {
            "thinking": thinking_content,
            "response": response_content,
            "full_response": generated_text
        }
        
    except requests.exceptions.Timeout:
        print(f"\n❌ Timeout after {config.OLLAMA_TIMEOUT} seconds")
        print("   Increase OLLAMA_TIMEOUT in config.py")
        return {"thinking": "", "response": "", "full_response": ""}
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Lost connection to Ollama")
        return {"thinking": "", "response": "", "full_response": ""}
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return {"thinking": "", "response": "", "full_response": ""}


# ═══════════════════════════════════════════════════════════════════════════════
# Test function
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 TESTING OLLAMA WITH THINKING MODEL")
    print("=" * 70)
    
    if not check_ollama_connection():
        exit(1)
    
    print("\n📝 Testing with simple prompt...")
    
    payload = {
        "model": config.OLLAMA_MODEL,
        "prompt": "What is 2+2? Give me just the number.",
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 500  # Enough for simple response
        }
    }
    
    try:
        response = requests.post(
            f"{config.OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=120
        )
        
        result = response.json()
        
        print(f"\n🔑 Response keys: {list(result.keys())}")
        
        thinking = result.get("thinking", "")
        resp = result.get("response", "")
        done_reason = result.get("done_reason", "")
        
        print(f"\n🧠 Thinking ({len(thinking)} chars):")
        print(f"   {thinking[:300]}..." if len(thinking) > 300 else f"   {thinking}")
        
        print(f"\n💬 Response ({len(resp)} chars):")
        print(f"   {resp[:300]}..." if len(resp) > 300 else f"   {resp}")
        
        print(f"\n🏁 Done reason: {done_reason}")
        
        # Extract using our function
        extracted = extract_response_from_thinking_model(result)
        print(f"\n✅ Extracted text ({len(extracted)} chars):")
        print(f"   {extracted[:300]}..." if len(extracted) > 300 else f"   {extracted}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)