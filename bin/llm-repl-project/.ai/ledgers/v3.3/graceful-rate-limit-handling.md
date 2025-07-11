# Ledger: Graceful Rate Limit Handling

**Goal:** To implement a robust mechanism for handling API rate limits gracefully, ensuring context preservation and seamless resumption of LLM operations without loss of progress or user frustration.

## 1. Core Principles

-   **Context Preservation:** Never lose the current operational context or LLM's internal state when a rate limit is encountered.
-   **Intelligent Backoff:** Implement adaptive retry strategies to avoid exacerbating rate limit issues.
-   **Transparency & User Notification:** Clearly communicate rate limit events and recovery plans to the user.
-   **Seamless Resumption:** Enable the LLM to pick up exactly where it left off once the rate limit is lifted.

## 2. Implementation Details

### 2.1. Rate Limit Detection

#### Feature

-   Identify when an API rate limit has been hit.

#### Implementation Details

-   Monitor API responses for specific HTTP status codes (e.g., 429 Too Many Requests) or error messages indicating rate limits.
-   Parse `Retry-After` headers if provided by the API to determine the waiting period.

### 2.2. Context Checkpointing and Buffering

#### Feature

-   Before initiating a retry, save the current state of the LLM's operation.

#### Implementation Details

-   **Leverage Long-Running Work Ledger:** Integrate with the existing long-running work ledger system. The current task's ledger file should be updated with the precise point of interruption, including:
    -   The last successfully processed step.
    -   The full prompt that was sent or was about to be sent.
    -   Any partial responses received.
    -   The LLM's internal thought process or state leading up to the rate limit.
-   **Input Buffering:** If user input was pending or received during the rate limit, ensure it is buffered and associated with the interrupted task.

### 2.3. Adaptive Backoff Strategy

#### Feature

-   Implement a retry mechanism that respects API rate limit policies.

#### Implementation Details

-   **Exponential Backoff:** Use an exponential backoff algorithm with jitter to space out retry attempts, preventing a thundering herd problem.
-   **`Retry-After` Header Compliance:** Prioritize waiting for the duration specified in the `Retry-After` header if available.
-   **Maximum Retries/Wait Time:** Define a sensible maximum number of retries or a maximum total wait time before escalating the issue (e.g., notifying the user for manual intervention).

### 2.4. User Notification and Feedback

#### Feature

-   Inform the user about the rate limit and the system's recovery actions.

#### Implementation Details

-   Display a clear, non-blocking message in the UI indicating that a rate limit has been encountered.
-   Include information about the estimated wait time (if known) and that the operation will automatically resume.
-   Provide an option for the user to manually cancel the operation if they don't wish to wait.

### 2.5. Seamless Resumption

#### Feature

-   Automatically resume the LLM's operation from the exact point of interruption.

#### Implementation Details

-   Once the backoff period is over, the LLM will read its corresponding ledger file to restore its context and state.
-   The LLM will then re-initiate the API call or continue processing from the saved interruption point, using the buffered input if applicable.
-   Ensure that the resumed operation is idempotent where possible to prevent unintended side effects from retries.
