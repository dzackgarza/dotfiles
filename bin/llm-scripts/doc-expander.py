#!/usr/bin/env python3
"""
Memory Expander Tool

Specialized tool for expanding LLM memory documents with deeper analysis, 
connections, and actionable insights. Designed specifically for the 
structured markdown files in ~/llm-memories/.
"""

import os
import sys
import json
import time
import uuid
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any, Union
from datetime import datetime

# Import required packages
try:
    import groq
    from groq import Groq
    from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error: {e}. Please install required packages with: pip install groq pydantic python-dotenv")
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
        try:
            # Create context from other memories
            context = self._get_memory_context(memory_content)
            
            # IN-DEPTH MEMORY EXPANSION TASK\n\n            ## ORIGINAL MEMORY CONTENT:\n            {memory_content}\n\n            ## CONTEXT FROM RELATED MEMORIES:\n            {context}\n\n            ## YOUR TASK:\n            Expand this memory into a comprehensive technical reference document. For EACH point in the original content:\n\n            1. **Deep Analysis** (100-150 words per major point):\n               - Technical background and context\n               - Psychological and cognitive factors\n               - System architecture implications\n               - Real-world examples and case studies\n\n            2. **Practical Implementation** (5-7 specific steps):\n               ```bash\n               # Example command structure\n               # Step 1: Verify current state\n               $ command_to_check_state\n               \n               # Step 2: Make atomic change\n               $ command_to_make_change\n               ```\n\n            3. **Pattern Recognition** (3-5 patterns per section):\n               - Name and description of pattern\n               - When to use/not use\n               - Relation to known design patterns\n               - Visual diagram if helpful (describe in text)\n\n            4. **Common Pitfalls** (with solutions):\n               ```\n               // Anti-pattern example\n               function doThingsBadly() {{\n                   // Don't do this\n                   if (condition) {{\n                       return true;\n                   }}\n               }}\n               \n               // Better approach\n               function doThingsWell() {{\n                   // Do this instead\n                   return condition;\n               }}\n               ```\n\n            5. **Verification Steps** (specific, testable actions):\n               1. How to verify the solution works\n               2. Expected outputs/behaviors\n               3. Metrics for success\n               4. Common failure modes\n\n            ## REQUIRED SECTIONS:\n            - Detailed technical analysis of each point\n            - Multiple concrete examples (code/CLI)\n            - Cross-references to related concepts\n            - Actionable checklists and procedures\n            - Troubleshooting guide\n\n            ## WORD COUNT TARGET: 700-1000 words\n\n            Remember: This should be a standalone technical reference that's immediately useful for engineers.\n            Include specific commands, code snippets, and detailed explanations.\n            """
            
            # Get the expanded content
            # First, get the system prompt
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
                    model=MODEL_NAME,
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
                    
                    # Add original text and ensure it's a string
                    response_data['original_text'] = str(memory_content)
                    
                    # Validate confidence level
                    if response_data['confidence_level'] not in ['high', 'medium', 'low']:
                        response_data['confidence_level'] = 'medium'
                    
                    return MemoryExpansion(**response_data)
                    
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"Error parsing JSON response: {e}")
                    print(f"Response content: {message_content}")
                    # Fall back to a basic response with the raw content
                    return MemoryExpansion(
                        original_text=str(memory_content),
                        expanded_insights=f"Error parsing response: {e}\n\nRaw response:\n{message_content}",
                        key_lessons=[],
                        action_items=[],
                        related_patterns=[],
                        anti_patterns=[],
                        cross_references=[],
                        confidence_level="low"
                    )
                    
            except Exception as e:
                print(f"Error during API call: {e}", file=sys.stderr)
                # Return a basic error response
                return MemoryExpansion(
                    original_text=str(memory_content),
                    expanded_insights=f"Error expanding memory: {str(e)}\n\nPlease check the error message and try again.",
                    key_lessons=[],
                    action_items=[{
                        "action": "Check the error message and try again",
                        "rationale": "The memory expansion failed and needs to be retried"
                    }],
                    related_patterns=[],
                    anti_patterns=[],
                    cross_references=[],
                    confidence_level="low"
                )
            
        except Exception as e:
            print(f"Error during memory expansion: {e}", file=sys.stderr)
            # Fallback to a basic expansion if the structured approach fails
            return MemoryExpansion(
                original_text=memory_content,
                expanded_insights=f"[Error in expansion: {str(e)}]",
                key_lessons=[],
                action_items=[],
                related_patterns=[],
                anti_patterns=[],
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
                
            # Skip if file is empty
            if not content.strip():
                print(f"Skipping {input_path} - file is empty")
                return False
                
            # Create a memory expander
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
            if attempt >= max_attempts:
                print(f"Error processing {input_path} after {attempt} attempts: {e}", file=sys.stderr)
                return False
                
            # Exponential backoff before retry
            wait_time = 2 ** attempt
            print(f"Attempt {attempt} failed for {input_path}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    return False

def main():
    """Main entry point for the memory expander."""
    parser = argparse.ArgumentParser(description="Expand LLM memory documents with deeper analysis.")
    parser.add_argument("input", nargs="+", help="Input file(s) or directory(ies)")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process directories recursively")
    parser.add_argument("-i", "--in-place", action="store_true", help="Modify files in place")
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
            
        print(f"Found {len(input_paths)} file(s) to process...\n")
        
        # Process each file
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
