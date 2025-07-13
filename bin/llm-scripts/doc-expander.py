#!/usr/bin/env python3
"""
Memory Expander Tool

Specialized tool for expanding LLM memory documents with deeper analysis, 
connections, and actionable insights. Designed specifically for the 
structured markdown files in ~/llm-memories/.
"""

import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Import required packages
try:
    from groq import Groq
except ImportError:
    print("Error: The 'groq' package is required. Please install it with: pip install groq")
    sys.exit(1)

try:
    from pydantic import (
        BaseModel,
        ConfigDict,
        Field,
        ValidationError,
        field_validator,
        model_validator,
    )
except ImportError:
    print("Error: The 'pydantic' package is required. Please install it with: pip install pydantic")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: The 'python-dotenv' package is required. Please install it with: pip install python-dotenv")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Initialize Groq client
try:
    GROQ_CLIENT = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    print("Please ensure GROQ_API_KEY is set in your environment or .env file")
    sys.exit(1)

# Constants
MEMORIES_DIR = Path(os.getenv("MEMORIES_DIR", "~/llm-memories")).expanduser().resolve()
DEFAULT_MODEL = "llama3-70b-8192"  # Default model to use for expansionalytical tasks
MEMORIES_DIR = Path.home() / "llm-memories"

# --- Models ---
class MemoryExpansion(BaseModel):
    """Structured representation of an expanded memory with enhanced insights."""
    # Core memory content
    original_text: str = Field(..., description="The original memory content")
    expanded_insights: str = Field(..., description="Deeper analysis and expansion of the memory")
    
    # Core analysis
    key_lessons: List[Dict[str, str]] = Field(
        ...,
        description="Key lessons learned, each with 'lesson' and 'implications'"
    )
    
    # Practical applications
    action_items: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Actionable items with 'action' and 'rationale'"
    )
    
    # Related patterns
    related_patterns: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Related behavioral or system patterns with 'pattern' and 'connection'"
    )
    
    # Counter-examples and anti-patterns
    anti_patterns: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Common mistakes to avoid with 'mistake' and 'better_approach'"
    )
    
    # Cross-references
    cross_references: List[Dict[str, str]] = Field(
        default_factory=list,
        description="References to other memories or concepts with 'reference' and 'relation'"
    )
    
    # Meta information
    confidence_level: str = Field(
        "medium",
        description="Confidence in the expansion (high/medium/low)"
    )
    
    last_updated: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="When this expansion was generated"
    )

class MemoryExpander:
    """Handles expansion and enhancement of LLM memory documents."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Groq(api_key=api_key)
        self.other_memories = self._load_other_memories()
    
    def _load_other_memories(self) -> Dict[str, str]:
        """Load all other memories for context and cross-referencing."""
        memories = {}
        if MEMORIES_DIR.exists():
            for mem_file in MEMORIES_DIR.glob("*.md"):
                try:
                    with open(mem_file, 'r', encoding='utf-8') as f:
                        memories[mem_file.stem] = f.read()
                except Exception as e:
                    print(f"Warning: Could not read memory {mem_file}: {e}")
        return memories
    
    def get_system_prompt(self) -> str:
        """Generate a comprehensive system prompt for in-depth memory expansion."""
        return """You are a senior systems architect and behavioral psychologist with expertise in analyzing and expanding technical memories. 
        Your task is to perform a deep, multi-faceted analysis of the provided memory document, expanding it into a comprehensive reference.
        
        ## RESPONSE FORMAT
        You MUST respond with a JSON object containing the following fields:
        
        {
            "expanded_insights": "Detailed analysis (500-700 words) covering technical background, psychological factors, and system implications",
            "key_lessons": [
                {
                    "lesson": "Clear, concise lesson title",
                    "implications": "Detailed explanation of why this matters and its impact"
                }
            ],
            "action_items": [
                {
                    "action": "Specific, actionable step",
                    "rationale": "Explanation of why this action is important"
                }
            ],
            "related_patterns": [
                {
                    "pattern": "Name of related pattern or concept",
                    "connection": "How this relates to the current memory"
                }
            ],
            "anti_patterns": [
                {
                    "mistake": "Description of common mistake",
                    "better_approach": "Better way to handle this situation"
                }
            ],
            "cross_references": [
                {
                    "reference": "Name of related memory or concept",
                    "relation": "How this relates to the current memory"
                }
            ],
            "confidence_level": "high/medium/low"
        }
        
        ## ANALYSIS INSTRUCTIONS
        For EACH major point in the original memory, analyze:
        
        1. **Technical Depth**
           - System architecture implications
           - Performance considerations
           - Security aspects
           - Integration points
           
        2. **Behavioral Analysis**
           - Cognitive biases at play
           - Common pitfalls and mistakes
           - Best practices and patterns
           - Lessons learned
           
        3. **Practical Application**
           - Step-by-step implementation guidance
           - Code examples and CLI commands
           - Testing and verification steps
           - Troubleshooting tips
           
        Be thorough, specific, and provide concrete examples. The goal is to create a standalone reference document that's immediately useful for engineers.
        """
        
    def _get_memory_context(self, current_memory: str) -> str:
        """Create a rich context string from other relevant memories with semantic analysis."""
        context = []
        memory_connections = []
        
        # Basic keyword matching to find related memories
        keywords = ['pattern', 'system', 'change', 'verify', 'modification', 'error']
        
        for title, content in self.other_memories.items():
            # Skip if it's the current memory
            if content == current_memory:
                continue
                
            # Simple relevance scoring
            relevance = sum(1 for kw in keywords if kw.lower() in content.lower())
            if relevance > 0:
                # Take first 100 words for context
                preview = ' '.join(content.split()[:100])
                memory_connections.append({
                    'title': title,
                    'relevance': relevance,
                    'preview': preview
                })
        
        # Sort by relevance and take top 5
        memory_connections.sort(key=lambda x: x['relevance'], reverse=True)
        
        # Build context string
        context_parts = []
        for i, mem in enumerate(memory_connections[:5], 1):
            context_parts.append(f"### Related Memory {i}: {mem['title']} (Relevance: {mem['relevance']})\n{mem['preview']}...\n")
        
        if context_parts:
            return "## Related Memories for Context\n\n" + "\n---\n\n".join(context_parts)
        return "No strongly related memories found."
    
    def expand_memory(self, memory_content: str) -> MemoryExpansion:
        """Expand a single memory with deeper insights and connections."""
        # Skip processing if content is empty or just contains placeholders
        if not memory_content.strip() or "<details><summary>View original memory</summary>" in memory_content:
            # Return a minimal valid MemoryExpansion object
            return MemoryExpansion(
                original_text=memory_content,
                expanded_insights="No meaningful content to expand",
                key_lessons=[],
                action_items=[],
                related_patterns=[],
                anti_patterns=[],
                cross_references=[],
                confidence_level="low"
            )
            
        try:
            # Create context from other memories
            context = self._get_memory_context(memory_content)
            
            # Get the system prompt
            system_prompt = self.get_system_prompt()
            
            # Create the expansion prompt with proper formatting and explicit JSON structure
            expansion_prompt = f"""
            # MEMORY EXPANSION TASK

            ## ORIGINAL MEMORY:
            {memory_content}

            ## TASK:
            Analyze this memory and expand it into a comprehensive technical reference.
            Focus on extracting key insights, lessons, and actionable items.

            ## RESPONSE FORMAT:
            Return a JSON object with exactly these fields:
            {{
                "expanded_insights": "Detailed analysis (500-700 words) covering technical and behavioral aspects",
                "key_lessons": [
                    {{"lesson": "Lesson 1", "implications": "Why this matters"}},
                    ...
                ],
                "action_items": [
                    {{"action": "Specific action to take", "rationale": "Why this helps"}},
                    ...
                ],
                "related_patterns": [
                    {{"pattern": "Pattern name", "connection": "How it relates"}},
                    ...
                ],
                "anti_patterns": [
                    {{"mistake": "Common mistake", "better_approach": "Better way"}},
                    ...
                ],
                "cross_references": [
                    {{"reference": "Related item", "relation": "How it connects"}},
                    ...
                ],
                "confidence_level": "high/medium/low"
            }}

            ## INSTRUCTIONS:
            1. Be specific and technical
            2. Include concrete examples where relevant
            3. Focus on practical applications
            4. Maintain a professional, informative tone
            """
            
            try:
                response = self.client.chat.completions.create(
                    model=DEFAULT_MODEL,  # Use the global constant
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": expansion_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000,
                    response_format={"type": "json_object"}
                )
                
                # Process the response
                try:
                    if not hasattr(response, 'choices') or not response.choices:
                        raise ValueError("No choices in API response")
                        
                    print("\n=== DEBUG: Response Structure ===", file=sys.stderr)
                    print(f"Response type: {type(response)}", file=sys.stderr)
                    print(f"Choices count: {len(response.choices) if hasattr(response, 'choices') else 0}", file=sys.stderr)
                    
                    if hasattr(response, 'choices') and response.choices:
                        print(f"First choice type: {type(response.choices[0])}", file=sys.stderr)
                        if hasattr(response.choices[0], 'message'):
                            print("Message attribute exists in choice", file=sys.stderr)
                            if hasattr(response.choices[0].message, 'content'):
                                print("Content attribute exists in message", file=sys.stderr)
                    
                    message_content = response.choices[0].message.content
                    if not message_content:
                        raise ValueError("Empty response from API")
                        
                    print(f"\n=== DEBUG: Message Content ===\nType: {type(message_content)}\nContent:\n{message_content}\n{'='*40}\n", file=sys.stderr)
                    
                except Exception as e:
                    print(f"\n=== ERROR: Failed to process response ===\n{str(e)}\n{'='*40}\n", file=sys.stderr)
                    raise
                    
                # Debug: Print raw response structure
                print("\n=== DEBUG: Raw Response Structure ===", file=sys.stderr)
                print(f"Type of message_content: {type(message_content)}", file=sys.stderr)
                if hasattr(message_content, '__dict__'):
                    print("Message content has __dict__:", file=sys.stderr)
                    for k, v in message_content.__dict__.items():
                        print(f"  {k}: {type(v)} - {str(v)[:200]}..." if len(str(v)) > 200 else f"  {k}: {v}", file=sys.stderr)
                print("=================================\n", file=sys.stderr)
                
                # Parse the JSON response
                try:
                    debug_info = [
                        "\n=== DEBUG: API Response ===",
                        f"Type: {type(message_content)}",
                        "Content:",
                        str(message_content)[:1000],
                        "\n=== Attempting to parse JSON ==="
                    ]
                    print("\n".join(debug_info), file=sys.stderr)
                    
                    if isinstance(message_content, str):
                        response_data = json.loads(message_content)
                    else:
                        response_data = dict(message_content)  # Convert to dict if it's an object
                        
                    print("\n=== Successfully Parsed Response ===", file=sys.stderr)
                    print(json.dumps(response_data, indent=2), file=sys.stderr)
                    print("=================================\n", file=sys.stderr)
                    
                    # Ensure all required fields are present
                    required_fields = {
                        'expanded_insights': '',
                        'key_lessons': [],
                        'action_items': [],
                        'related_patterns': [],
                        'anti_patterns': [],
                        'cross_references': [],
                        'confidence_level': 'medium'
                    }
                    
                    # Merge with defaults to ensure all fields exist
                    for field, default in required_fields.items():
                        response_data[field] = response_data.get(field, default)
                    
                    # Ensure lists contain properly formatted dictionaries
                    for list_field in ['key_lessons', 'action_items', 'related_patterns', 
                                     'anti_patterns', 'cross_references']:
                        if not isinstance(response_data[list_field], list):
                            response_data[list_field] = []
                        else:
                            # Ensure each item is a dictionary
                            response_data[list_field] = [
                                item if isinstance(item, dict) else {}
                                for item in response_data[list_field]
                            ]
                return MemoryExpansion(
                    original_text=memory_content,
                    expanded_insights=response_data['expanded_insights'],
                    key_lessons=response_data['key_lessons'],
                    action_items=response_data['action_items'],
                    related_patterns=response_data['related_patterns'],
                    anti_patterns=response_data['anti_patterns'],
                    cross_references=response_data['cross_references'],
                    confidence_level=response_data['confidence_level']
                )
                
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error parsing JSON response: {e}")
                print(f"Response content: {message_content[:500]}...")  # Print first 500 chars of response
                
                # Return a minimal valid response with the error
                return MemoryExpansion(
                    original_text=memory_content,
                    expanded_insights=f"Error parsing response: {str(e)}\n\nRaw response (truncated):\n{message_content[:500]}...",
                    key_lessons=[],
                    action_items=[],
                    related_patterns=[],
                    anti_patterns=[],
                    cross_references=[],
                    confidence_level="low"
            return MemoryExpansion(
                original_text=memory_content,
                expanded_insights=response_data['expanded_insights'],
                key_lessons=response_data['key_lessons'],
                action_items=response_data['action_items'],
                related_patterns=response_data['related_patterns'],
                anti_patterns=response_data['anti_patterns'],
                cross_references=response_data['cross_references'],
                confidence_level=response_data['confidence_level']
            )
            
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response content: {message_content[:500]}...")  # Print first 500 chars of response
            
            # Return a minimal valid response with the error
            return MemoryExpansion(
                original_text=memory_content,
                expanded_insights=f"Error parsing response: {str(e)}\n\nRaw response (truncated):\n{message_content[:500]}...",
                key_lessons=[],
                action_items=[],
                related_patterns=[],
                anti_patterns=[],
                cross_references=[],
                confidence_level="low"
            )
            
        
    except Exception as e:
        print(f"Error during memory expansion: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        
        # Create a helpful error message
        error_msg = f"""## Error Expanding Memory

An error occurred while expanding this memory:

```
{str(e)}
```

### Recommended Actions:
1. Check if the memory contains valid content
2. Verify your API key and internet connection
3. Try again with the `--force` flag to regenerate
4. If the issue persists, check the error logs for more details
"""
        
        return MemoryExpansion(
            original_text=memory_content,
            expanded_insights=error_msg,
            key_lessons=[],
            action_items=[{
                "action": "Check error details and try again",
                "rationale": "The memory expansion failed and needs attention"
            }],
            related_patterns=[],
            anti_patterns=[{
                "mistake": "Skipping error checking",
                "better_approach": "Always validate input and handle errors gracefully"
            }],
            cross_references=[],
            confidence_level="low"
        )

class MemoryExpansion(BaseModel):
    """Model for the expanded memory output with flexible field handling."""
    model_config = ConfigDict(
        extra="ignore",  # Ignore extra fields in the input
        arbitrary_types_allowed=True,  # Allow arbitrary types in Dict values
        validate_default=True
    )
    
    original_text: str = Field(
        default="",
        description="The original memory content. Will be extracted from the input if not provided."
    )
    expanded_insights: Union[str, Dict[str, Any]] = Field(
        default="",
        description="Detailed expansion of the original content. Can be a string or structured data."
    )
    key_lessons: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of key lessons learned with optional metadata"
    )
    action_items: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of actionable items with optional metadata"
    )
    related_patterns: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Related patterns or concepts with optional metadata"
    )
    anti_patterns: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Common mistakes or anti-patterns to avoid with optional metadata"
    )
    cross_references: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="References to related memories or resources with optional metadata"
    )
    confidence_level: str = Field(
        default="medium",
        description="Confidence level of the expansion (low/medium/high)"
    )
    last_updated: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp of when this expansion was created"
    )

    @model_validator(mode='before')
    @classmethod
    def ensure_proper_types(cls, data: Any) -> Any:
        """Ensure all field values have the correct types."""
        if not isinstance(data, dict):
            return data
            
        # Handle expanded_insights
        if 'expanded_insights' in data:
            v = data['expanded_insights']
            if not isinstance(v, (str, dict)):
                data['expanded_insights'] = str(v) if v is not None else ""
        
        return data

    @field_validator('key_lessons', 'action_items', 'related_patterns', 'anti_patterns', 'cross_references', mode='before')
    @classmethod
    def validate_list_items(cls, v: Any) -> List[Dict[str, Any]]:
        """Ensure list items are properly formatted dictionaries with string values."""
        if v is None:
            return []

        if not isinstance(v, list):
            try:
                v = [v]  # Try to convert single item to list
            except (TypeError, ValueError):
                return []

        validated = []
        for item in v:
            if item is None:
                continue

            if not isinstance(item, dict):
                # Convert non-dict items to dict with a default key
                item = {"content": str(item) if item is not None else ""}

            # Ensure all values are strings or can be converted to strings
            validated_item = {}
            for key, value in item.items():
                if value is None:
                    continue

                # Convert key to string if needed
                if not isinstance(key, str):
                    key = str(key)

                # Handle different value types
                if isinstance(value, (str, int, float, bool)):
                    validated_item[key] = str(value)
                elif isinstance(value, (list, dict)):
                    # Convert complex values to JSON string
                    try:
                        validated_item[key] = json.dumps(value, ensure_ascii=False)
                    except (TypeError, ValueError):
                        validated_item[key] = str(value)
                else:
                    validated_item[key] = str(value)

            if validated_item:  # Only add non-empty items
                validated.append(validated_item)

        return validated

    @field_validator('confidence_level')
    @classmethod
    def validate_confidence_level(cls, v: Any) -> str:
        """Ensure confidence level is one of the allowed values."""
        if not isinstance(v, str):
            return "medium"

        v = v.lower().strip()
        if v not in {'low', 'medium', 'high'}:
            return "medium"
        return v

def get_api_key() -> str:
    """Get API key from environment or .env file."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable not found. "
            "Please set it in your environment or .env file."
        )
    return api_key

def format_memory_expansion(expansion: MemoryExpansion) -> str:
    """Format the expanded memory into a well-structured markdown document."""
    output = []
    
    # Header with metadata
    output.append(f"# Memory Expansion\n")
    output.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  ")
    output.append(f"*Confidence: {expansion.confidence_level.capitalize()}*\n")
    
    # Original memory (collapsible)
    output.append("## 🔍 Original Memory\n")
    output.append(f"<details><summary>View original memory</summary>\n\n{expansion.original_text}\n</details>\n")
    
    # Expanded insights - handle both string and dict types
    output.append("## 💡 Expanded Insights\n")
    if isinstance(expansion.expanded_insights, dict):
        # Convert dict to formatted string
        insights = []
        for key, value in expansion.expanded_insights.items():
            if isinstance(value, (list, dict)):
                # Convert complex values to JSON string
                try:
                    value_str = json.dumps(value, indent=2, ensure_ascii=False)
                except (TypeError, ValueError):
                    value_str = str(value)
                insights.append(f"### {key}\n```json\n{value_str}\n```")
            else:
                insights.append(f"### {key}\n{value}")
        output.append("\n".join(insights))
    else:
        output.append(str(expansion.expanded_insights))
    output.append("\n---\n")
    
    # Helper function to format list items
    def format_list_items(items: List[Dict[str, Any]], title_field: str = 'title', 
                         description_field: str = 'description') -> List[str]:
        formatted = []
        for i, item in enumerate(items, 1):
            if not isinstance(item, dict):
                formatted.append(f"- {str(item)}")
                continue
                
            # Try to get title and description, fall back to other keys
            title = item.get(title_field, '')
            if not title and 'name' in item:
                title = item['name']
            if not title and 'key' in item:
                title = item['key']
                
            description = item.get(description_field, '')
            if not description and 'value' in item:
                description = item['value']
                
            if title and description:
                formatted.append(f"{i}. **{title}**: {description}")
            elif title:
                formatted.append(f"{i}. {title}")
            else:
                formatted.append(f"- {str(item)}")
        return formatted
    
    # Key Lessons
    if expansion.key_lessons:
        output.append("## 🎯 Key Lessons\n")
        output.extend(format_list_items(expansion.key_lessons, 'lesson', 'implications'))
        output.append("")  # Add empty line for better readability
    
    # Action Items
    if expansion.action_items:
        output.append("## ✅ Action Items\n")
        output.extend(format_list_items(expansion.action_items, 'action', 'rationale'))
        output.append("")  # Add empty line for better readability
    
    # Related Patterns
    if expansion.related_patterns:
        output.append("## 🔗 Related Patterns\n")
        output.extend(format_list_items(expansion.related_patterns, 'pattern', 'connection'))
        output.append("")  # Add empty line for better readability
    
    # Anti-Patterns
    if expansion.anti_patterns:
        output.append("## ⚠️ Anti-Patterns\n")
        output.extend(format_list_items(expansion.anti_patterns, 'mistake', 'better_approach'))
        output.append("")  # Add empty line for better readability
    
    # Cross References
    if expansion.cross_references:
        output.append("## 🔄 Cross-References\n")
        output.extend(format_list_items(expansion.cross_references, 'reference', 'relation'))
        output.append("")  # Add empty line for better readability
    
    return '\n'.join(output)

def process_memory(input_path: Path, output_path: Path, api_key: str, force: bool = False, max_attempts: int = 3) -> bool:
    """Process a single memory file with backup.
    
    Args:
        input_path: Path to the input file
        output_path: Path to save the output
        api_key: Groq API key
        force: Whether to overwrite existing files
        max_attempts: Maximum number of attempts to process the file
        
    Returns:
        bool: True if processing was successful, False otherwise
    """
    # Skip files that are already expanded (have .expanded in their name)
    if '.expanded' in input_path.stem and input_path != output_path:
        print(f"Skipping {input_path} - appears to be an already expanded file")
        return True
        
    for attempt in range(1, max_attempts + 1):
        try:
            # Skip if output exists and we're not forcing
            if output_path.exists() and not force:
                print(f"Skipping {input_path} - output already exists")
                return True
                
            # Read the input file
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Skip if file is empty or contains only placeholders
            if not content.strip() or "<details><summary>View original memory</summary>" in content:
                print(f"Skipping {input_path} - file contains no meaningful content")
                # If this is an expanded file, clean it up
                if input_path != output_path and output_path.exists():
                    output_path.unlink()
                return False
                
            # Check if content is meaningful (not just placeholders)
            if not content.strip() or content.strip() == "## 🔍 Original Memory" or "<details><summary>View original memory</summary>" in content:
                print(f"Skipping {input_path} - no meaningful content to expand")
                return False
                
            # Create a memory expander
            try:
                expander = MemoryExpander(api_key)
                
                # Expand the memory
                expansion = expander.expand_memory(content)
                
                # Format the output
                formatted = format_memory_expansion(expansion)
                
                # Ensure output directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save with backup if in-place
                if str(input_path) == str(output_path):
                    expander.save_expanded_memory(output_path, formatted)
                else:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(formatted)
                        
                print(f"Expanded memory saved to: {output_path}")
                return True
                
            except Exception as e:
                print(f"Error expanding memory {input_path}: {e}")
                # Clean up any partial output
                if output_path.exists():
                    output_path.unlink()
                raise
            
        except Exception as e:
            if attempt >= max_attempts:
                print(f"Error processing {input_path} after {attempt} attempts: {e}", file=sys.stderr)
                return False
                
            # Exponential backoff before retry
            wait_time = 2 ** attempt
            print(f"Attempt {attempt} failed for {input_path}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    return False

def extract_themes(content: str, file_name: str, client: Any) -> Dict[str, Any]:
    """Extract themes and key content from a document."""
    system_prompt = """You are an expert analyst. Extract key themes, concepts, and their relationships from the following document. 
    Focus on identifying core ideas, technical details, and how they connect to form a comprehensive understanding."""
    
    user_prompt = f"""# THEME EXTRACTION TASK

## DOCUMENT: {file_name}

## INSTRUCTIONS:
1. Read the document carefully
2. Identify 3-5 main themes
3. For each theme, extract:
   - Key concepts and definitions
   - Important examples or code snippets
   - Relationships to other themes
   - Specific insights or patterns
4. Format as a JSON object with this structure:
{{
  "themes": [
    {{
      "name": "Theme name",
      "description": "Brief description",
      "key_concepts": ["concept1", "concept2"],
      "examples": ["quote or example", "another example"],
      "relationships": ["related to X in doc Y", "builds on concept Z"],
      "source_sections": ["relevant section text"]
    }}
  ]
}}

## DOCUMENT CONTENT:
{content}

## YOUR ANALYSIS:"""
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=4000,
            response_format={"type": "json_object"},
            stream=False,
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error extracting themes from {file_name}: {e}", file=sys.stderr)
        return {"themes": []}

def build_knowledge_graph(themes_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Combine themes from multiple documents into a knowledge graph."""
    # Group similar themes across documents
    theme_groups = {}
    
    for doc_themes in themes_list:
        for theme in doc_themes.get("themes", []):
            theme_name = theme["name"].lower()
            if theme_name not in theme_groups:
                theme_groups[theme_name] = {
                    "name": theme["name"],
                    "descriptions": set(),
                    "key_concepts": set(),
                    "examples": [],
                    "relationships": [],
                    "sources": []
                }
            
            # Add unique content
            theme_groups[theme_name]["descriptions"].add(theme.get("description", ""))
            theme_groups[theme_name]["key_concepts"].update(theme.get("key_concepts", []))
            theme_groups[theme_name]["examples"].extend(theme.get("examples", []))
            theme_groups[theme_name]["relationships"].extend(theme.get("relationships", []))
            theme_groups[theme_name]["sources"].extend(theme.get("source_sections", []))
    
    # Convert sets to lists for JSON serialization
    for theme in theme_groups.values():
        theme["descriptions"] = list(theme["descriptions"])
        theme["key_concepts"] = list(theme["key_concepts"])
    
    return {"themes": list(theme_groups.values())}

def generate_comprehensive_document(knowledge_graph: Dict[str, Any], client: Any) -> str:
    """Generate a comprehensive document from the knowledge graph."""
    system_prompt = """You are a senior technical writer. Create a comprehensive document that synthesizes information 
    from multiple sources. Focus on maintaining accuracy, depth, and clarity while organizing content thematically."""
    
    user_prompt = """# COMPREHENSIVE DOCUMENT CREATION TASK

## INSTRUCTIONS:
1. Review the following knowledge graph of themes and concepts
2. Create a well-structured document that:
   - Preserves all important details and examples
   - Shows relationships between concepts
   - Maintains technical accuracy
   - Uses clear, concise language
   - Includes specific examples and quotes

## KNOWLEDGE GRAPH:
{knowledge_graph}

## DOCUMENT STRUCTURE:
# Comprehensive Analysis

## Table of Contents
[Generate a detailed TOC]

## Executive Summary
[1-2 paragraph overview of key findings]

## Thematic Sections
[For each major theme, include:
- Clear definition and explanation
- Key concepts and their relationships
- Specific examples and quotes
- Connections to other themes]

## Cross-Cutting Insights
[Patterns and relationships across themes]

## Technical Reference
[Important technical details, code examples, etc.]

## Appendices
[Additional reference material]

## OUTPUT:"""
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=8000,
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating document: {e}", file=sys.stderr)
        return "# Error generating comprehensive document\n\n" + str(e)

def save_analysis(file_name: str, content: str, output_dir: Path) -> Path:
    """Save analysis to a file and return the path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{file_name}.analysis.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return output_path

def combine_analyses_batch(analysis_paths: List[Path], client: Any, batch_size: int = 3) -> str:
    """Combine analyses in batches to handle large document sets."""
    combined = []
    
    # Process in batches
    for i in range(0, len(analysis_paths), batch_size):
        batch = analysis_paths[i:i + batch_size]
        batch_content = []
        
        # Read batch content
        for path in batch:
            with open(path, 'r', encoding='utf-8') as f:
                batch_content.append(f"# {path.stem}\n\n{f.read()}")
        
        if not batch_content:
            continue
            
        # If it's the last batch and we have previous content, include a summary
        if i + batch_size >= len(analysis_paths) and combined:
            batch_content.insert(0, "# Summary of Previous Sections\n\n" + "\n\n".join(combined[-3:]))
        
        system_prompt = """You are a senior technical writer. Combine the following document analyses into 
        a coherent section. Focus on maintaining all important details while creating a smooth narrative."""
        
        user_prompt = f"""# DOCUMENT COMBINATION TASK

## INSTRUCTIONS:
1. Combine the following document analyses into a coherent section
2. Maintain all important details and technical information
3. Create smooth transitions between documents
4. Use clear section headers and markdown formatting
5. Preserve code examples and technical details

## DOCUMENTS TO COMBINE:
{"\n\n---\n\n".join(batch_content)}

## OUTPUT:
[Your combined analysis here]"""
        
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=8000,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                stream=False,
            )
            combined_section = response.choices[0].message.content
            combined.append(combined_section)
            
            # Add delay between API calls
            time.sleep(2)
            
        except Exception as e:
            print(f"Error combining batch {i//batch_size + 1}: {e}", file=sys.stderr)
            # Fallback to simple concatenation
            combined.append("\n\n".join(batch_content))
    
    # Final combination of all batches
    final_content = "\n\n---\n\n".join(combined)
    
    # Create final comprehensive document
    system_prompt = """You are a senior technical editor. Create a comprehensive, well-structured 
    document from the following sections. Ensure the document has a logical flow, consistent formatting,
    and includes all important details."""
    
    user_prompt = f"""# FINAL DOCUMENT ASSEMBLY TASK

## INSTRUCTIONS:
1. Combine the following sections into a single, well-structured document
2. Create a detailed table of contents
3. Add an executive summary
4. Organize content thematically
5. Ensure smooth transitions between sections
6. The final document should be comprehensive and detailed (400-500 lines)

## SECTIONS:
{final_content}

## OUTPUT FORMAT:
# Comprehensive Analysis

## Table of Contents
[Detailed TOC with section numbers]

## Executive Summary
[1-2 paragraph overview]

## [Thematic Sections]
[Organized content with subsections]

## Key Insights and Recommendations
[Actionable insights and next steps]"""
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=8000,
            top_p=0.9,
            frequency_penalty=0.2,
            presence_penalty=0.1,
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error creating final document: {e}", file=sys.stderr)
        return "# Comprehensive Analysis\n\n" + final_content

def summarize_memories(input_paths: List[Path], output_path: Path, api_key: str, force: bool = False) -> bool:
    """Create a comprehensive synthesis of multiple memory files.
    
    Args:
        input_paths: List of input files to analyze
        output_path: Path to save the comprehensive document
        api_key: Groq API key
        force: Whether to overwrite existing output file
        
    Returns:
        bool: True if synthesis was successful, False otherwise
    """
    if not force and output_path.exists():
        print(f"Skipping - output file {output_path} already exists (use --force to overwrite)")
        return False
    
    print(f"Analyzing {len(input_paths)} documents for thematic synthesis...")
    
    # Initialize the Groq client
    client = Groq(api_key=api_key)
    
    # Phase 1: Extract themes from each document
    all_themes = []
    for i, input_path in enumerate(input_paths, 1):
        try:
            print(f"Analyzing document {i}/{len(input_paths)}: {input_path.name}")
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    themes = extract_themes(content, input_path.name, client)
                    all_themes.append(themes)
                    # Add a small delay between API calls
                    time.sleep(1)
        except Exception as e:
            print(f"Error processing {input_path}: {e}", file=sys.stderr)
    
    if not all_themes:
        print("No content to analyze")
        return False
    
    # Phase 2: Build a knowledge graph from all themes
    print("\nBuilding knowledge graph from themes...")
    knowledge_graph = build_knowledge_graph(all_themes)
    
    # Save intermediate knowledge graph for debugging
    kg_path = output_path.with_suffix('.knowledge_graph.json')
    with open(kg_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_graph, f, indent=2)
    
    # Phase 3: Generate comprehensive document
    print("Generating comprehensive document...")
    final_document = generate_comprehensive_document(knowledge_graph, client)
    
    # Save the final document
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Comprehensive Analysis\n\n")
        f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(f"## Analysis of {len(input_paths)} Memory Documents\n\n")
        f.write(final_document)
    
    print(f"\nComprehensive analysis saved to: {output_path}")
    print(f"Knowledge graph saved to: {kg_path}")
    return True

def main():
    """Main entry point for the memory expander."""
    parser = argparse.ArgumentParser(description="Expand LLM memory documents with deeper analysis.")
    parser.add_argument("input", nargs="+", help="Input file(s) or directory(ies)")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process directories recursively")
    parser.add_argument("-i", "--in-place", action="store_true", help="Modify files in place")
    parser.add_argument("--summarize", action="store_true", help="Generate a summary of all input files")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    
    args = parser.parse_args()
    
    try:
        # Get API key
        api_key = get_api_key()
        
        # Process inputs
        input_paths = []
        for path in args.input:
            path = Path(path).expanduser().resolve()
            if not path.exists():
                print(f"Warning: {path} does not exist, skipping")
                continue
                
            if path.is_dir():
                # Add all .md files in the directory
                pattern = "**/*.md" if args.recursive else "*.md"
                input_paths.extend(path.glob(pattern))
            else:
                input_paths.append(path)
        
        if not input_paths:
            print("No matching files found.")
            return 1
            
        # Remove duplicate paths while preserving order
        seen = set()
        input_paths = [p for p in input_paths if not (p in seen or seen.add(p))]
        
        print(f"Found {len(input_paths)} file(s) to process...\n")
        
        # Handle summarization mode
        if args.summarize:
            # Determine output path for summary
            if args.output:
                output_path = Path(args.output).expanduser().resolve()
                if output_path.is_dir():
                    output_path = output_path / "memory_summary.md"
            else:
                output_path = Path.cwd() / "memory_summary.md"
            
            print(f"Generating summary of {len(input_paths)} files...")
            if summarize_memories(input_paths, output_path, api_key, args.force):
                print(f"\nSummary generated successfully: {output_path}")
                return 0
            else:
                print("\nFailed to generate summary.", file=sys.stderr)
                return 1
        
        # Normal processing mode
        success_count = 0
        for i, input_path in enumerate(input_paths, 1):
            try:
                print(f"\nProcessing: {input_path} ({i}/{len(input_paths)})")
                
                # Determine output path
                if args.in_place:
                    output_path = input_path
                elif args.output:
                    output_path = Path(args.output).expanduser().resolve()
                    if output_path.is_dir() or output_path.suffix.lower() != '.md':
                        output_path = output_path / input_path.name
                else:
                    output_path = input_path.with_stem(f"{input_path.stem}.expanded")
                
                # Process the file
                if process_memory(input_path, output_path, api_key, args.force):
                    success_count += 1
                
            except Exception as e:
                print(f"Error processing {input_path}: {e}", file=sys.stderr)
                if args.debug:
                    import traceback
                    traceback.print_exc()
                continue
        
        # Print summary
        print(f"\nProcessing complete. Successfully processed {success_count} of {len(input_paths)} files.")
        if success_count < len(input_paths):
            print("Some files were not processed successfully. Use --debug for more details.")
            return 1
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
        
    return 0

class MemoryExpander:
    def __init__(self, api_key: str = None):
        """Initialize the MemoryExpander with an optional API key."""
        self.client = GROQ_CLIENT  # Use the global client
        self.model = DEFAULT_MODEL
        
    def expand_memory(self, content: str) -> 'MemoryExpansion':
        """Expand the given memory content using the LLM."""
        try:
            # Prepare the system prompt
            system_prompt = (
                "You are a knowledge expansion assistant. Your task is to analyze and expand "
                "the provided memory with additional insights, connections, and actionable items. "
                "Return your response in the specified JSON format."
            )
            
            # Prepare the user prompt
            user_prompt = (
                f"Please expand the following memory with additional insights, connections, "
                f"and actionable items. Focus on adding depth, context, and practical value.\n\n"
                f"{content}"
            )
            
            # Call the LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            response_content = response.choices[0].message.content
            try:
                response_data = json.loads(response_content)
                return MemoryExpansion(**response_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing LLM response: {e}", file=sys.stderr)
                print(f"Response content: {response_content}", file=sys.stderr)
                raise ValueError("Failed to parse LLM response as JSON") from e
                
        except Exception as e:
            print(f"Error in expand_memory: {e}", file=sys.stderr)
            raise
        
    @staticmethod
    def create_backup(file_path: Path) -> None:
        """Create a hidden backup of the file if it exists."""
        if not file_path.exists():
            return
            
        backup_path = file_path.parent / f".{file_path.name}.bak"
        try:
            with open(file_path, 'r', encoding='utf-8') as src, \
                 open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            print(f"Created backup at: {backup_path}")
        except Exception as e:
            print(f"Warning: Could not create backup of {file_path}: {e}")
    
    def save_expanded_memory(self, memory_path: Path, content: str) -> Path:
        """Save the expanded memory to a file, creating a hidden backup of the original."""
        # Create output directory if it doesn't exist
        output_dir = memory_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create backup of original if it exists and we're not already working with an expanded file
        if memory_path.exists() and not memory_path.stem.endswith('.expanded'):
            self.create_backup(memory_path)
        
        # Save the expanded content to the original filename
        with open(memory_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Expanded memory saved to: {memory_path}")
        return memory_path

def get_api_key() -> str:
    """Get API key from environment or .env file."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable not found. "
            "Please set it in your environment or .env file."
        )
    return api_key

if __name__ == "__main__":
    sys.exit(main())
