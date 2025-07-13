# Widget CSS to YAML Migration

**Branch:** feat/widget-css-to-yaml-migration
**Summary:** Extract hardcoded CSS values from widget classes to YAML configuration, enabling visual fine-tuning without code changes.
**Status:** Planning
**Created:** 2025-07-11
**Updated:** 2025-07-11

## Context

### Problem Statement
Widget styling and dimensions are hardcoded in CSS strings within Python classes, making visual adjustments require code modification instead of simple configuration changes.

**Current Issues**:
- CSS values embedded in widget `DEFAULT_CSS` strings
- Spacing, padding, margins hardcoded throughout widgets
- Border styles and colors not configurable
- Widget dimensions scattered across multiple files
- No central control over visual consistency

**Examples of Hardcoded CSS**:
```python
# live_block_widget.py:22-29
DEFAULT_CSS = """
LiveBlockWidget {
    border: round $primary;
    margin-bottom: 1;        # Hardcoded
    padding: 1;              # Hardcoded  
    height: auto;
    min-height: 0;           # Hardcoded
}
"""

# timeline.py:185-192
DEFAULT_CSS = """
TimelineBlockWidget {
    border: round $primary;  # Hardcoded border style
    margin-bottom: 1;        # Hardcoded margin
    padding: 0 1;            # Hardcoded padding
    width: 100%;
}
"""
```

### Success Criteria
- [ ] All widget dimensions configurable via YAML
- [ ] CSS template system for dynamic value injection
- [ ] Consistent spacing system across all widgets
- [ ] Theme-aware widget styling
- [ ] Visual changes possible without code modification

### Acceptance Criteria
- [ ] Widget spacing adjustable through configuration
- [ ] Border styles and colors configurable
- [ ] Responsive sizing behavior configurable
- [ ] Theme switching affects widget styling
- [ ] Hot-reload of visual changes during development

## User-Visible Behaviors

When this ledger is complete, users will see:

- **Widget spacing and sizing adjustable via YAML configuration**
- **Consistent visual spacing system across all widgets**
- **Theme changes affect widget borders and spacing**
- **Visual fine-tuning possible without code modification**
- **Responsive layout behavior configurable**

## Technical Approach

### Widget CSS Audit

**Files with Hardcoded CSS**:
1. `src/widgets/live_block_widget.py` - 80+ lines of CSS
2. `src/widgets/timeline.py` - 60+ lines of CSS 
3. `src/widgets/cognition_pipeline_widget.py` - 100+ lines of CSS
4. `src/widgets/prompt_input.py` - CSS styling values

**CSS Values to Extract**:
```yaml
# Target YAML configuration structure
ui:
  spacing:
    # Base spacing units
    unit: 1
    small: 0.5
    medium: 1  
    large: 2
    
  borders:
    style: "round"
    width: 1
    
  widget_sizing:
    live_block:
      margin_bottom: 1
      padding: 1
      min_height: 0
    timeline_block:
      margin_bottom: 1
      padding: [0, 1]
      width: "100%"
    cognition_pipeline:
      padding: 2
      margin: [1, 0]
      
  responsive:
    auto_height: true
    min_height: 0
    max_height: "none"
```

### Implementation Strategy

#### Phase 1: CSS Template System

**Create CSS Template Engine**:
```python
# src/ui/css_template.py
from string import Template
from typing import Dict, Any
from src.config import config

class CSSTemplate:
    """Template system for injecting YAML values into CSS"""
    
    @staticmethod
    def render_widget_css(template: str, widget_type: str) -> str:
        """Render CSS template with YAML configuration values"""
        widget_config = config.ui.widget_sizing.get(widget_type, {})
        spacing_config = config.ui.spacing
        border_config = config.ui.borders
        
        # Create template variables
        template_vars = {
            # Spacing
            'spacing_unit': spacing_config.unit,
            'spacing_small': spacing_config.small,
            'spacing_medium': spacing_config.medium,
            'spacing_large': spacing_config.large,
            
            # Borders
            'border_style': border_config.style,
            'border_width': border_config.width,
            
            # Widget-specific
            **widget_config
        }
        
        return Template(template).substitute(template_vars)
```

#### Phase 2: Widget CSS Templates

**Convert Hardcoded CSS to Templates**:

```python
# Before: Hardcoded CSS in live_block_widget.py
DEFAULT_CSS = """
LiveBlockWidget {
    border: round $primary;
    margin-bottom: 1;
    padding: 1;
    height: auto;
    min-height: 0;
}
"""

# After: Template with YAML injection
DEFAULT_CSS_TEMPLATE = """
LiveBlockWidget {
    border: $border_style $primary;
    margin-bottom: $margin_bottom;
    padding: $padding;
    height: auto;
    min-height: $min_height;
}
"""

class LiveBlockWidget(Vertical):
    def __init__(self, live_block: LiveBlock, **kwargs):
        # Render CSS from template with YAML values
        self.DEFAULT_CSS = CSSTemplate.render_widget_css(
            self.DEFAULT_CSS_TEMPLATE, 
            'live_block'
        )
        super().__init__(**kwargs)
```

#### Phase 3: Configuration Schema

**Enhanced YAML Configuration**:
```yaml
# config.yaml - UI section expansion
ui:
  spacing:
    unit: 1
    small: 0.5
    medium: 1
    large: 2
    extra_large: 3
    
  borders:
    style: "round"        # round, solid, dashed, dotted
    width: 1
    
  widget_sizing:
    live_block:
      margin_bottom: ${spacing.medium}
      padding: ${spacing.medium}
      min_height: 0
      max_height: "none"
      
    timeline_block:
      margin_bottom: ${spacing.medium}  
      padding_horizontal: ${spacing.medium}
      padding_vertical: 0
      width: "100%"
      
    cognition_pipeline:
      padding: ${spacing.large}
      margin_vertical: ${spacing.medium}
      margin_horizontal: 0
      
    prompt_input:
      min_height: 3
      max_height: 10
      padding: ${spacing.small}
      
  responsive:
    auto_height: true
    auto_width: true
    content_align: "top left"
    
  visual_effects:
    live_block_animation: true
    transition_duration: 0.3
    hover_effects: true
```

### Specific Widget Migrations

#### LiveBlockWidget Migration
```python
class LiveBlockWidget(Vertical):
    DEFAULT_CSS_TEMPLATE = """
    LiveBlockWidget {
        border: $border_style $primary;
        margin-bottom: $margin_bottom;
        padding: $padding;
        height: auto;
        min-height: $min_height;
        max-height: $max_height;
        content-align: $content_align;
        width: $width;
    }
    
    LiveBlockWidget > * {
        height: auto;
        min-height: $min_height;
        max-height: $max_height;
        width: $width;
    }
    
    .live-block {
        border: $border_style $success;
        background: $success 10%;
    }
    
    .transitioning-block {
        border: $border_style $warning;
        background: $warning 20%;
    }
    
    .inscribed-block {
        border: $border_style $primary;
        background: $surface;
    }
    """
    
    def __init__(self, live_block: LiveBlock, **kwargs):
        self.DEFAULT_CSS = CSSTemplate.render_widget_css(
            self.DEFAULT_CSS_TEMPLATE,
            'live_block'
        )
        super().__init__(**kwargs)
```

#### TimelineBlockWidget Migration
```python
class TimelineBlockWidget(Vertical):
    DEFAULT_CSS_TEMPLATE = """
    TimelineBlockWidget {
        border: $border_style $primary;
        margin-bottom: $margin_bottom;
        padding: $padding_vertical $padding_horizontal;
        height: auto;
        min-height: $min_height;
        width: $width;
    }

    TimelineBlockWidget.timeline-block-cognition {
        border: $border_style $secondary;
    }

    .sub-block {
        border: $border_style $accent;
        width: 90%;
        margin: $spacing_medium $spacing_large;
        padding: $padding_vertical $padding_horizontal;
        height: auto;
        min-height: $min_height;
    }
    """
```

### Implementation Plan

#### Step 1: CSS Template Infrastructure
- Create `CSSTemplate` class with YAML integration
- Add UI configuration schema to YAML
- Implement template variable substitution system

#### Step 2: Widget-by-Widget Migration  
- Start with `LiveBlockWidget` (most complex CSS)
- Migrate `TimelineBlockWidget` and sub-components
- Update `CognitionPipelineWidget` styling
- Handle `PromptInput` widget CSS

#### Step 3: Configuration Validation
- Add CSS template validation
- Ensure required template variables exist
- Fallback values for missing configuration

#### Step 4: Hot-Reload Integration
- CSS regeneration on configuration change
- Widget refresh mechanism for live updates
- Development workflow optimization

### Testing Strategy

#### Unit Tests
```python
class TestCSSTemplateSystem:
    def test_template_variable_substitution(self):
        """Verify template variables properly substituted"""
        
    def test_missing_variable_handling(self):
        """Verify graceful handling of missing variables"""
        
    def test_yaml_configuration_integration(self):
        """Verify CSS templates use YAML configuration"""
        
    def test_widget_css_generation(self):
        """Verify widget CSS generated correctly"""
```

#### Integration Tests
```python
class TestWidgetStyling:
    def test_live_block_widget_styling(self):
        """Verify LiveBlockWidget uses configured styling"""
        
    def test_timeline_widget_styling(self):
        """Verify TimelineBlockWidget uses configured styling"""
        
    def test_configuration_changes_affect_styling(self):
        """Verify YAML changes affect widget appearance"""
```

#### Visual Regression Tests
```python
class TestVisualConsistency:
    def test_spacing_consistency_across_widgets(self):
        """Verify consistent spacing system usage"""
        
    def test_theme_integration_with_widget_styling(self):
        """Verify theme changes affect widget styling"""
        
    def test_responsive_behavior_configuration(self):
        """Verify responsive sizing follows configuration"""
```

### Migration Checklist

#### Pre-Migration
- [ ] Audit all widget CSS hardcoded values
- [ ] Design comprehensive UI configuration schema
- [ ] Create CSS template system infrastructure
- [ ] Establish visual baseline for comparison

#### Migration Process
- [ ] Implement CSS template engine
- [ ] Convert LiveBlockWidget to template system
- [ ] Convert TimelineBlockWidget to template system
- [ ] Convert remaining widgets to template system
- [ ] Add configuration validation

#### Post-Migration Validation
- [ ] Visual appearance identical to baseline
- [ ] Configuration changes affect widget styling
- [ ] No CSS generation errors
- [ ] Performance impact acceptable

### Risk Assessment

#### Low Risk Changes
- Adding CSS template infrastructure (additive)
- YAML configuration expansion (fallback to defaults)

#### Medium Risk Changes
- Widget CSS template conversion (visual changes possible)
- Template variable substitution (could break CSS)

#### High Risk Changes
- Hot-reload CSS regeneration (could affect performance)
- Complex responsive behavior configuration

### Performance Considerations

```python
class CSSTemplate:
    """Optimized CSS template system"""
    
    _template_cache: Dict[str, Template] = {}
    _rendered_cache: Dict[str, str] = {}
    
    @classmethod
    def render_widget_css(cls, template: str, widget_type: str) -> str:
        """Cached CSS rendering for performance"""
        cache_key = f"{widget_type}:{hash(template)}"
        
        if cache_key in cls._rendered_cache:
            return cls._rendered_cache[cache_key]
            
        # Generate and cache result
        rendered = cls._render_template(template, widget_type)
        cls._rendered_cache[cache_key] = rendered
        return rendered
```

## Completion Criteria

### Technical Requirements
- [ ] All widget CSS values configurable via YAML
- [ ] CSS template system functional and performant
- [ ] No hardcoded styling values in widget classes
- [ ] Configuration validation prevents invalid CSS

### Visual Requirements  
- [ ] Visual appearance identical with default configuration
- [ ] Configuration changes immediately affect widget styling
- [ ] Consistent spacing system across all widgets
- [ ] Theme integration with widget styling

### Developer Experience
- [ ] Hot-reload of CSS changes during development
- [ ] Clear error messages for invalid CSS configuration
- [ ] Documentation for all configurable CSS properties
- [ ] Easy addition of new configurable properties

---

*This ledger enables visual fine-tuning through configuration while maintaining code separation and visual consistency.*