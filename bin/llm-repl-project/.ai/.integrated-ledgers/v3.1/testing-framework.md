
# Ledger: Testing Framework

**Goal:** To establish a robust and comprehensive testing framework that ensures the application's functionality, visual fidelity, and stability through end-to-end (E2E) and snapshot testing.

## 1. Core Philosophy

- **End-to-End Validation:** Simulate real user interactions to validate the complete application flow.
- **Visual Fidelity:** Catch visual and layout regressions by comparing terminal output snapshots.
- **Robustness:** Ensure tests are deterministic, reliable, and provide clear feedback on failures.

## 2. Core Functionality

### 2.1. End-to-End (E2E) Testing Framework

#### Feature

- Establish a robust E2E testing framework using Textual's `App.run_test()` and related APIs to simulate user interactions and inspect application state.

#### Implementation Details

1.  **Test Directory:** Create a `tests/e2e/` directory for E2E test files.
2.  **Base Test Class:** Implement a base E2E test class or utility functions leveraging `textual.app.App.run_test()`.
3.  **Interaction Simulation:** Provide capabilities to simulate key presses, text input, and clicks.
4.  **State Inspection:** Allow querying and inspecting widget properties.
5.  **Idle State Waiting:** Implement mechanisms to wait for application idle states.

### 2.2. E2E Snapshot Testing

#### Feature

- Implement snapshot testing for Textual E2E tests to catch visual and layout regressions by comparing terminal output snapshots.

#### Implementation Details

1.  **Snapshot Storage:** New `tests/snapshots/` directory to store baseline snapshots.
2.  **Snapshot Capture:** Integrate `pytest-snapshot` or custom snapshot comparison logic to capture textual snapshots of the terminal output (e.g., using `app.save_screenshot()` or `app.screen.get_screenshot().render(plain=True)`).
3.  **Automated Comparison:** Automated comparison of current snapshots against baselines, with tests failing on mismatches.
4.  **Snapshot Updates:** Clear process for updating baseline snapshots when changes are intentional.

## 3. Advanced Features

-   **Test Reporting:** Generate comprehensive test reports.
-   **CI/CD Integration:** Integrate testing into the continuous integration/continuous deployment pipeline for automated checks.
-   **Performance Testing:** Incorporate performance metrics into E2E tests to track regressions.
-   **User Journey Tests:** Develop comprehensive tests for critical user journeys.
