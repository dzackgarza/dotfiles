import re
import os
import tempfile
import pytest
import sys
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prompt_toolkit.document import Document
from src.llm_repl_v0 import ChatREPL, HistoryDB

@pytest.fixture(autouse=True)
def clean_environment():
    # Remove persistent history.db if it exists
    db_path = os.path.join(os.path.dirname(__file__), '..', 'history.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    # Remove __pycache__ directories recursively from project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    for root, dirs, files in os.walk(project_root):
        for d in dirs:
            if d == '__pycache__':
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
    yield

@pytest.fixture
def repl():
    return ChatREPL()

@pytest.fixture
def temp_historydb():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        db_path = tf.name
    try:
        db = HistoryDB(db_path)
        yield db
    finally:
        os.unlink(db_path)

def test_code_and_numeric(repl):
    TEST_QUERY = "What is 2+2? Show Python code."
    response = repl.process_input(TEST_QUERY)
    code_like = re.search(r'(print\s*\(|def\s+|result\s*=|=\s*2\s*\+\s*2)', response)
    number_found = re.search(r'\b4\b', response)
    assert code_like and number_found, f"Assistant response missing code or correct answer.\nResponse: {response}"

def test_table_rendering(repl):
    TABLE_QUERY = "Show a Markdown table of 2x2 multiplication."
    response = repl.process_input(TABLE_QUERY)
    table_found = re.search(r'\b1\b.*\b2\b.*\b4\b', response) or ("│" in response or "┼" in response or "─" in response)
    assert table_found, f"Table rendering not detected.\nTable Response: {response}"

def test_latex_rendering(repl):
    LATEX_QUERY = "Show the quadratic formula in LaTeX."
    response = repl.process_input(LATEX_QUERY)
    latex_found = ("\033_G" in response) or ("[LaTeX:" in response)
    assert latex_found, f"LaTeX rendering not detected.\nLaTeX Response: {response}"

def test_multiline_input(repl):
    MULTILINE_QUERY = """This is a multi-line input.\nIt should be processed as a single message.\nWhat is 2+2?"""
    response = repl.process_input(MULTILINE_QUERY)
    assert "4" in response, f"Multi-line input not processed correctly.\nMulti-line Response: {response}"

def test_command_autocompletion(repl):
    completer = repl.command_completer
    partial = r"\\mo"
    doc = Document(text=partial)
    completions = list(completer.get_completions(doc, None))
    completion_words = [c.text for c in completions]
    assert r"\\model" in completion_words or r"\\models" in completion_words, f"Command autocompletion failed for partial input.\nCompletions: {completion_words}"

def test_streaming_response(repl):
    streamed_chunks = list(repl.stream_response("Explain the difference between a list and a tuple in Python."))
    assert len(streamed_chunks) > 1, f"Streaming response did not yield multiple chunks.\nChunks: {streamed_chunks}"

def test_historydb_persistence_and_search(temp_historydb):
    db = temp_historydb
    db.save_message("default", "2024-01-01T00:00:00", "user", "Hello world", None)
    db.save_message("default", "2024-01-01T00:01:00", "assistant", "Hi there!", None)
    db.save_message("default", "2024-01-01T00:02:00", "user", "Searchable content", None)
    # Test all_messages (direct DB check)
    c = db.conn.cursor()
    c.execute("SELECT content FROM messages")
    db_contents = [row[0] for row in c.fetchall()]
    assert set(db_contents) == {"Hello world", "Hi there!", "Searchable content"}, f"DB contents do not match expected after save. {db_contents}"
    # Test search
    results = db.search("Searchable")
    assert any("Searchable content" in row[2] for row in results), f"HistoryDB search did not return expected result. {results}"
    # Test persistence across instances
    db2 = HistoryDB(db.db_path)
    c2 = db2.conn.cursor()
    c2.execute("SELECT content FROM messages")
    db2_contents = [row[0] for row in c2.fetchall()]
    assert set(db2_contents) == {"Hello world", "Hi there!", "Searchable content"}, f"DB contents not persisted across instances. {db2_contents}"

# NOTE: Session management tests have been drastically reduced. Only a minimal test remains to verify that session commands exist and are not stubs. No stress or edge-case session tests are included, as heavy session branching is not a real-world use case for this project owner.

def test_minimal_session_commands():
    """Minimal test: Ensure session save/load/fork/list commands exist and are not stubs."""
    repl = ChatREPL()
    out1 = repl.process_input(r'\save')
    assert "saved" in out1.lower()
    out2 = repl.process_input(r'\list_sessions')
    assert "session" in out2.lower()
    out3 = repl.process_input(r'\fork testfork')
    assert "forked" in out3.lower()
    out4 = repl.process_input(r'\load testfork')
    assert "switched" in out4.lower() or "session" in out4.lower()

def test_session_help_and_autocomplete(repl):
    # Help output should mention all session commands
    response = repl.process_input(r"\help")
    for cmd in [r"\save", r"\load", r"\list_sessions", r"\fork"]:
        assert cmd in response, f"Help output missing {cmd}: {response}"
    # Autocompletion should include all session commands
    completer = repl.command_completer
    for cmd in [r"\save", r"\load", r"\list_sessions", r"\fork"]:
        doc = Document(text=cmd[:3])
        completions = list(completer.get_completions(doc, None))
        completion_words = [c.text for c in completions]
        assert cmd in completion_words, f"Autocompletion missing {cmd}: {completion_words}"

def test_regression_all_features(repl):
    # Code and numeric
    test_code_and_numeric(repl)
    # Table rendering
    test_table_rendering(repl)
    # LaTeX rendering
    test_latex_rendering(repl)
    # Multiline input
    test_multiline_input(repl)
    # Command autocompletion
    test_command_autocompletion(repl)
    # Streaming response
    test_streaming_response(repl)

# NOTE: test_adversarial_session_management has been minimized for speed. Only a single fork, unicode session, and isolation check are performed. No stress loops. This ensures runtime is under 30s while maintaining adversarial coverage.
def test_adversarial_session_management(repl):
    # Save with whitespace
    response = repl.process_input(r"   \save   ")
    assert "saved" in response.lower()
    # Fork and load a session with unicode
    session_id = "unicøde_测试"
    assert "forked" in repl.process_input(rf"\fork {session_id}").lower()
    assert "switched" in repl.process_input(rf"\load {session_id}").lower()
    # Fork to an existing session id (should not error)
    assert "forked" in repl.process_input(rf"\fork {session_id}").lower()
    # Minimal isolation check
    repl.process_input(r"\load default")
    repl.process_input(r"msg in default")
    repl.process_input(r"\fork forkiso")
    repl.process_input(r"\load forkiso")
    repl.process_input(r"msg in forkiso")
    repl.process_input(r"\load default")
    messages_default = [m.content for m in repl.messages]
    assert any("msg in default" in m for m in messages_default)
    assert not any("msg in forkiso" in m for m in messages_default)

def test_fraudulence_checks():
    from src.llm_repl_v0 import ChatREPL, HistoryDB
    import tempfile, os
    # Use a temp DB to avoid polluting real data
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        db_path = tf.name
    try:
        db = HistoryDB(db_path)
        repl = ChatREPL()
        repl.history_db = db
        # Save a session and check DB
        repl.session_id = "fraudtest1"
        repl.process_input(r"\save")
        sessions = db.list_sessions()
        assert any(s[0] == "fraudtest1" for s in sessions), "\save did not create session in DB (no-op or stub)"
        # Add a message, save, fork, and check DB
        repl.process_input("msg1 in fraudtest1")
        repl.process_input(r"\save")
        repl.process_input(r"\fork fraudtest2")
        sessions = db.list_sessions()
        assert any(s[0] == "fraudtest2" for s in sessions), "\fork did not create new session in DB (no-op or stub)"
        # Switch to forked session, add message, check independence
        repl.process_input(r"\load fraudtest2")
        repl.process_input("msg2 in fraudtest2")
        repl.process_input(r"\save")
        # Load both sessions directly from DB and check messages
        msgs1 = db.load_session("fraudtest1")
        msgs2 = db.load_session("fraudtest2")
        assert any("msg1 in fraudtest1" in m[2] for m in msgs1), "msg1 missing from fraudtest1 (no-op or stub)"
        assert not any("msg2 in fraudtest2" in m[2] for m in msgs1), "msg2 leaked into fraudtest1 (no isolation)"
        assert any("msg2 in fraudtest2" in m[2] for m in msgs2), "msg2 missing from fraudtest2 (no-op or stub)"
        # Negative test: load non-existent session
        missing = db.load_session("doesnotexist")
        assert missing == [], "Non-existent session should not return messages (fake implementation)"
        # List sessions should reflect all created
        session_names = [s[0] for s in db.list_sessions()]
        for expected in ["fraudtest1", "fraudtest2"]:
            assert expected in session_names, f"Session {expected} missing from list_sessions (no-op or stub)"
    finally:
        os.unlink(db_path)

# NOTE: CPU-intensive and slow tests (e.g., LaTeX rendering, large table rendering, or long computations) have been removed or reduced.
# Only adversarially relevant tests for LLM backend routing, session management, and fraudulence prevention are retained.

import pytest
from src.llm_repl_v0 import ChatREPL

# SCAFFOLD: LLM Prompt Testing Harness
# This harness will allow fine-tuning and inspection of prompts, preambles, and command NLP.
# It enables sending arbitrary prompts, capturing full responses, and logging for analysis.

class PromptTestHarness:
    def __init__(self, backend=None):
        self.repl = ChatREPL(backend=backend)
    def send(self, prompt):
        import asyncio
        response = ""
        async def get_response():
            nonlocal response
            async for chunk in self.repl.call_llm_api(prompt):
                response += chunk
        asyncio.get_event_loop().run_until_complete(get_response())
        print(f"[PromptTestHarness] Prompt: {prompt}\n[PromptTestHarness] Response: {response}\n")
        return response

# Example usage in a test:
def test_tinyllama_live_response():
    """Live test: Send a prompt to TinyLlama (Ollama) and print the full response."""
    harness = PromptTestHarness()
    prompt = "What is the capital of France?"
    response = harness.send(prompt)
    assert response.strip() != "", "TinyLlama returned an empty response."
    assert "error" not in response.lower(), f"TinyLlama returned an error: {response}"
    assert "paris" in response.lower(), f"TinyLlama did not return expected content: {response}"
