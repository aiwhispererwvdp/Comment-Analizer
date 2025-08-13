# Professional Theme System

This theme system provides consistent styling and visual components for the Personal Paraguay Comments Analysis Platform.

## Overview

The theme system centralizes all CSS styling and HTML components to ensure:
- **Consistency**: Uniform appearance across all pages
- **Maintainability**: Single source of truth for all styling
- **Professional Design**: Enterprise-grade visual design
- **Responsiveness**: Mobile and desktop optimization

## Components

### ProfessionalTheme Class

Central theme configuration with:
- **Color Palette**: Primary, secondary, text, background, and status colors
- **Typography**: Font families, sizes, weights, and line heights
- **Spacing**: Consistent margins, padding, and border radius values
- **Component Templates**: Reusable HTML component generators

### Available Components

#### 1. Header Component
```python
theme.get_component_html("header", "Title", "Subtitle")
```
Creates the main page header with gradient background.

#### 2. Info Card
```python
theme.get_component_html("info_card", "Title", "Content", icon="🔬")
```
Professional card layout with optional icons.

#### 3. Metric Card
```python
theme.get_component_html("metric_card", "", "", value="123", subtitle="Total Items")
```
Displays metrics with large numbers and descriptions.

#### 4. Status Indicator
```python
theme.get_component_html("status_indicator", "Status", "Details", status="healthy")
```
Color-coded status badges (healthy, warning, error).

#### 5. Upload Section
```python
theme.get_component_html("upload_section", "Upload Title", "Description")
```
Styled file upload areas with dashed borders.

#### 6. Success Alert
```python
theme.get_component_html("success_alert", "Success Title", "Success message")
```
Green success notification boxes.

## Color Scheme

### Primary Colors
- **Primary Dark**: #1e3a8a (Deep blue)
- **Primary Medium**: #3b82f6 (Medium blue)
- **Primary Light**: #60a5fa (Light blue)

### Text Colors
- **Primary Text**: #1f2937 (Dark gray)
- **Secondary Text**: #374151 (Medium gray)
- **Muted Text**: #64748b (Light gray)

### Status Colors
- **Success**: #16a34a (Green)
- **Warning**: #d97706 (Orange) 
- **Error**: #dc2626 (Red)

## Typography

- **Font Family**: Inter (Google Fonts)
- **Sizes**: XL (2.5rem), LG (1.5rem), MD (1.1rem), SM (0.9rem), XS (0.85rem)
- **Weights**: Light (300), Normal (400), Medium (500), Semibold (600), Bold (700)

## Usage Examples

### Basic Page Setup
```python
from theme import theme

# Apply theme CSS
st.markdown(theme.get_main_css(), unsafe_allow_html=True)

# Add header
st.markdown(
    theme.get_component_html("header", "Page Title", "Page description"),
    unsafe_allow_html=True
)
```

### Creating Info Cards
```python
# Simple info card
st.markdown(
    theme.get_component_html(
        "info_card",
        "📊 Data Analysis",
        "Upload your data files for analysis"
    ),
    unsafe_allow_html=True
)
```

### Metric Display
```python
# Display metrics
st.markdown(
    theme.get_component_html(
        "metric_card",
        "",
        "",
        value="1,234",
        subtitle="Total Comments"
    ),
    unsafe_allow_html=True
)
```

## Mobile Responsiveness

The theme includes responsive design for mobile devices:
- Adjusted padding and margins for smaller screens
- Responsive font sizes
- Optimized card layouts

## Customization

To modify the theme:

1. **Colors**: Edit the `COLORS` dictionary in `ProfessionalTheme`
2. **Typography**: Update the `TYPOGRAPHY` dictionary
3. **Spacing**: Modify the `SPACING` dictionary
4. **New Components**: Add new component types to `get_component_html()`

## Browser Support

Tested and optimized for:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- Minimal CSS overhead
- Optimized for fast rendering
- Cached component generation
- No external dependencies beyond Google Fonts