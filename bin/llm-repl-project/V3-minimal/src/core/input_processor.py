"""Input processing component following Sacred Timeline architecture

Handles user input processing and coordinates the Sacred Turn Structure:
[User] → [Cognition] → [Assistant]
"""

from typing import TYPE_CHECKING

from ..config import TimelineConfig

if TYPE_CHECKING:
    from ..sacred_timeline import SacredTimeline
    from .response_generator import ResponseGenerator


class InputProcessor:
    """Processes user input following Sacred Timeline patterns

    Responsibilities:
    - Validate and sanitize user input
    - Add user blocks to Sacred Timeline
    - Coordinate cognition processing
    - Trigger assistant response generation
    """

    def __init__(
        self, timeline: "SacredTimeline", response_generator: "ResponseGenerator"
    ):
        self.timeline = timeline
        self.response_generator = response_generator

    def process_user_input(self, user_input: str) -> None:
        """Process user input through the Sacred Turn Structure

        Args:
            user_input: Raw user input text

        Sacred Turn Structure:
        1. Add user block to timeline
        2. Generate and add cognition block
        3. Generate and add assistant response block
        """
        user_input = user_input.strip()

        if not user_input:
            return

        # Step 1: Add user message to Sacred Timeline
        self.timeline.add_block(role="user", content=user_input)

        # Step 2: Generate cognition processing block
        self._add_cognition_block(user_input)

        # Step 3: Generate assistant response
        response = self.response_generator.generate_response(user_input)
        self.timeline.add_block(role="assistant", content=response)

    def _add_cognition_block(self, user_input: str) -> None:
        """Add cognition processing block to timeline

        Args:
            user_input: User input being processed
        """
        # Create preview of user input for cognition display
        preview = self._create_input_preview(user_input)
        cognition_content = (
            f"{TimelineConfig.COGNITION_PREVIEW_PREFIX}"
            f"{preview}"
            f"{TimelineConfig.COGNITION_PREVIEW_SUFFIX}"
        )

        self.timeline.add_block(role="cognition", content=cognition_content)

    def _create_input_preview(self, user_input: str) -> str:
        """Create a preview of user input for cognition display

        Args:
            user_input: Full user input text

        Returns:
            Truncated preview if input exceeds max length
        """
        max_length = TimelineConfig.MAX_CONTENT_PREVIEW
        if len(user_input) > max_length:
            return user_input[:max_length]
        return user_input
