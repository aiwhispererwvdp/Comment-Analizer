# Theme System Documentation

The Theme System provides comprehensive theming capabilities for the Personal Paraguay Fiber Comments Analysis System, enabling consistent visual design, dark/light mode support, and customizable branding.

## 🎯 Overview

This module implements a sophisticated theming system built on Streamlit's theming capabilities, providing consistent visual identity, accessibility features, and customizable design elements across the entire application.

### Core Capabilities
- **Multi-Theme Support** - Light, dark, and custom themes
- **Dynamic Theme Switching** - Real-time theme changes
- **Accessibility Features** - High contrast and color-blind friendly options
- **Brand Customization** - Corporate branding and color schemes
- **Component Consistency** - Unified styling across all components

## 🏗️ Theme Architecture

### Multi-Layer Theming Framework
```python
class ThemeSystemArchitecture:
    """
    Comprehensive theme system architecture
    """
    
    THEME_LAYERS = {
        'base': {
            'purpose': 'Core design tokens and foundations',
            'components': ['colors', 'typography', 'spacing', 'borders'],
            'scope': 'global'
        },
        'component': {
            'purpose': 'Component-specific styling',
            'components': ['buttons', 'cards', 'forms', 'charts'],
            'scope': 'component'
        },
        'layout': {
            'purpose': 'Layout and structure styling',
            'components': ['grid', 'containers', 'navigation', 'sidebar'],
            'scope': 'layout'
        },
        'semantic': {
            'purpose': 'Semantic and state-based styling',
            'components': ['success', 'warning', 'error', 'info'],
            'scope': 'contextual'
        }
    }
    
    THEME_VARIANTS = {
        'light': {
            'name': 'Light Theme',
            'description': 'Clean light interface for daytime use',
            'primary_color': '#1f4e79',
            'background': '#ffffff'
        },
        'dark': {
            'name': 'Dark Theme',
            'description': 'Dark interface for low-light environments',
            'primary_color': '#5b9bd5',
            'background': '#1e1e1e'
        },
        'corporate': {
            'name': 'Corporate Theme',
            'description': 'Professional corporate branding',
            'primary_color': '#2c3e50',
            'background': '#f8f9fa'
        },
        'high_contrast': {
            'name': 'High Contrast',
            'description': 'High contrast for accessibility',
            'primary_color': '#000000',
            'background': '#ffffff'
        }
    }
```

## 🎨 Core Theme Manager

### Master Theme Controller
```python
class ThemeManager:
    """
    Central theme management system for Streamlit application
    """
    
    def __init__(self):
        self.current_theme = 'light'
        self.theme_configs = self.load_theme_configurations()
        self.custom_css_manager = CustomCSSManager()
        self.color_palette_manager = ColorPaletteManager()
        self.typography_manager = TypographyManager()
        self.accessibility_manager = AccessibilityManager()
        
    def initialize_theme_system(self):
        """
        Initialize the complete theme system
        """
        # Load default theme
        self.load_theme(self.current_theme)
        
        # Apply base styling
        self.apply_base_styling()
        
        # Initialize component themes
        self.initialize_component_themes()
        
        # Setup theme switching functionality
        self.setup_theme_switching()
        
        # Apply accessibility features
        self.apply_accessibility_features()
    
    def load_theme(self, theme_name):
        """
        Load and apply a specific theme
        """
        if theme_name not in self.theme_configs:
            raise ValueError(f"Theme '{theme_name}' not found")
        
        theme_config = self.theme_configs[theme_name]
        
        # Apply Streamlit config
        self.apply_streamlit_config(theme_config)
        
        # Apply custom CSS
        self.apply_custom_css(theme_config)
        
        # Update component styles
        self.update_component_styles(theme_config)
        
        # Store current theme
        self.current_theme = theme_name
        
        return theme_config
    
    def apply_streamlit_config(self, theme_config):
        """
        Apply theme configuration to Streamlit
        """
        # Update Streamlit theme configuration
        streamlit_theme = {
            'primaryColor': theme_config['colors']['primary'],
            'backgroundColor': theme_config['colors']['background'],
            'secondaryBackgroundColor': theme_config['colors']['secondary_background'],
            'textColor': theme_config['colors']['text'],
            'font': theme_config['typography']['font_family']
        }
        
        # Apply to Streamlit (using st.config for runtime theme changes)
        for key, value in streamlit_theme.items():
            st.config.set_option(f'theme.{key}', value)
    
    def apply_custom_css(self, theme_config):
        """
        Apply custom CSS styling for advanced theming
        """
        css_rules = self.generate_theme_css(theme_config)
        
        # Inject CSS into Streamlit
        st.markdown(
            f"""
            <style>
            {css_rules}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    def generate_theme_css(self, theme_config):
        """
        Generate comprehensive CSS rules for the theme
        """
        colors = theme_config['colors']
        typography = theme_config['typography']
        spacing = theme_config['spacing']
        
        css_rules = f"""
        /* Root variables */
        :root {{
            --primary-color: {colors['primary']};
            --secondary-color: {colors['secondary']};
            --background-color: {colors['background']};
            --surface-color: {colors['surface']};
            --text-color: {colors['text']};
            --text-secondary: {colors['text_secondary']};
            --accent-color: {colors['accent']};
            --success-color: {colors['success']};
            --warning-color: {colors['warning']};
            --error-color: {colors['error']};
            --info-color: {colors['info']};
            
            --font-family: {typography['font_family']};
            --font-size-base: {typography['font_size_base']};
            --font-weight-normal: {typography['font_weight_normal']};
            --font-weight-bold: {typography['font_weight_bold']};
            
            --spacing-xs: {spacing['xs']};
            --spacing-sm: {spacing['sm']};
            --spacing-md: {spacing['md']};
            --spacing-lg: {spacing['lg']};
            --spacing-xl: {spacing['xl']};
        }}
        
        /* Main container styling */
        .main {{
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: var(--font-family);
        }}
        
        /* Sidebar styling */
        .css-1d391kg {{
            background-color: var(--surface-color);
            border-right: 1px solid var(--primary-color);
        }}
        
        /* Header styling */
        .css-18e3th9 {{
            padding-top: var(--spacing-md);
            padding-bottom: var(--spacing-md);
        }}
        
        /* Card styling */
        .card {{
            background-color: var(--surface-color);
            border: 1px solid var(--primary-color);
            border-radius: 8px;
            padding: var(--spacing-md);
            margin: var(--spacing-sm) 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Button styling */
        .stButton > button {{
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 4px;
            padding: var(--spacing-sm) var(--spacing-md);
            font-weight: var(--font-weight-bold);
            transition: background-color 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background-color: var(--secondary-color);
        }}
        
        /* Metric styling */
        .metric-container {{
            background-color: var(--surface-color);
            border-left: 4px solid var(--accent-color);
            padding: var(--spacing-md);
            margin: var(--spacing-sm) 0;
        }}
        
        /* Chart styling */
        .chart-container {{
            background-color: var(--surface-color);
            border-radius: 8px;
            padding: var(--spacing-md);
            margin: var(--spacing-md) 0;
        }}
        
        /* Alert styling */
        .alert-success {{
            background-color: var(--success-color);
            color: white;
            padding: var(--spacing-sm);
            border-radius: 4px;
            margin: var(--spacing-sm) 0;
        }}
        
        .alert-warning {{
            background-color: var(--warning-color);
            color: white;
            padding: var(--spacing-sm);
            border-radius: 4px;
            margin: var(--spacing-sm) 0;
        }}
        
        .alert-error {{
            background-color: var(--error-color);
            color: white;
            padding: var(--spacing-sm);
            border-radius: 4px;
            margin: var(--spacing-sm) 0;
        }}
        
        .alert-info {{
            background-color: var(--info-color);
            color: white;
            padding: var(--spacing-sm);
            border-radius: 4px;
            margin: var(--spacing-sm) 0;
        }}
        """
        
        return css_rules
```

## 🌈 Color System

### Advanced Color Palette Manager
```python
class ColorPaletteManager:
    """
    Manage color palettes and schemes across themes
    """
    
    def __init__(self):
        self.base_palettes = self.define_base_palettes()
        self.semantic_colors = self.define_semantic_colors()
        self.accessibility_colors = self.define_accessibility_colors()
        
    def define_base_palettes(self):
        """
        Define base color palettes for different themes
        """
        return {
            'light': {
                'primary': '#1f4e79',
                'secondary': '#5b9bd5',
                'accent': '#70ad47',
                'background': '#ffffff',
                'surface': '#f8f9fa',
                'text': '#2c3e50',
                'text_secondary': '#6c757d',
                'border': '#dee2e6'
            },
            'dark': {
                'primary': '#5b9bd5',
                'secondary': '#1f4e79',
                'accent': '#70ad47',
                'background': '#1e1e1e',
                'surface': '#2d2d2d',
                'text': '#ffffff',
                'text_secondary': '#b0b0b0',
                'border': '#404040'
            },
            'corporate': {
                'primary': '#2c3e50',
                'secondary': '#34495e',
                'accent': '#3498db',
                'background': '#f8f9fa',
                'surface': '#ffffff',
                'text': '#2c3e50',
                'text_secondary': '#7f8c8d',
                'border': '#bdc3c7'
            },
            'high_contrast': {
                'primary': '#000000',
                'secondary': '#333333',
                'accent': '#0066cc',
                'background': '#ffffff',
                'surface': '#f0f0f0',
                'text': '#000000',
                'text_secondary': '#333333',
                'border': '#000000'
            }
        }
    
    def define_semantic_colors(self):
        """
        Define semantic colors for different states and meanings
        """
        return {
            'success': '#28a745',
            'warning': '#ffc107',
            'error': '#dc3545',
            'info': '#17a2b8',
            'neutral': '#6c757d'
        }
    
    def generate_color_variations(self, base_color, variations=5):
        """
        Generate color variations from a base color
        """
        import colorsys
        
        # Convert hex to RGB
        rgb = tuple(int(base_color[i:i+2], 16) for i in (1, 3, 5))
        
        # Convert RGB to HSV
        hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        
        variations_list = []
        
        for i in range(variations):
            # Adjust saturation and value
            factor = 0.2 + (i * 0.2)  # 0.2 to 1.0
            new_s = hsv[1] * factor
            new_v = hsv[2] * (0.8 + factor * 0.2)
            
            # Convert back to RGB
            new_rgb = colorsys.hsv_to_rgb(hsv[0], new_s, new_v)
            
            # Convert to hex
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(new_rgb[0] * 255),
                int(new_rgb[1] * 255),
                int(new_rgb[2] * 255)
            )
            
            variations_list.append(hex_color)
        
        return variations_list
    
    def create_accessible_palette(self, base_palette):
        """
        Create accessibility-compliant color palette
        """
        accessible_palette = base_palette.copy()
        
        # Ensure sufficient contrast ratios
        contrast_adjustments = {
            'text_on_background': 4.5,  # WCAG AA standard
            'text_on_primary': 4.5,
            'text_on_secondary': 4.5
        }
        
        for adjustment, min_ratio in contrast_adjustments.items():
            adjusted_color = self.adjust_for_contrast(
                accessible_palette,
                adjustment,
                min_ratio
            )
            if adjusted_color:
                accessible_palette.update(adjusted_color)
        
        return accessible_palette
```

## 🔤 Typography System

### Typography Manager
```python
class TypographyManager:
    """
    Manage typography across themes and components
    """
    
    def __init__(self):
        self.font_stacks = self.define_font_stacks()
        self.type_scales = self.define_type_scales()
        self.text_styles = self.define_text_styles()
        
    def define_font_stacks(self):
        """
        Define font stacks for different themes
        """
        return {
            'system': [
                '-apple-system',
                'BlinkMacSystemFont',
                '"Segoe UI"',
                'Roboto',
                '"Helvetica Neue"',
                'Arial',
                'sans-serif'
            ],
            'professional': [
                '"Source Sans Pro"',
                '"Helvetica Neue"',
                'Helvetica',
                'Arial',
                'sans-serif'
            ],
            'modern': [
                '"Inter"',
                '"SF Pro Display"',
                'system-ui',
                'sans-serif'
            ],
            'accessible': [
                '"Open Sans"',
                'Verdana',
                'Arial',
                'sans-serif'
            ]
        }
    
    def define_type_scales(self):
        """
        Define typography scales for consistent sizing
        """
        return {
            'major_third': {
                'base': 16,
                'ratio': 1.25,
                'sizes': {
                    'xs': 10,
                    'sm': 12,
                    'base': 16,
                    'lg': 20,
                    'xl': 25,
                    '2xl': 31,
                    '3xl': 39,
                    '4xl': 49,
                    '5xl': 61
                }
            },
            'perfect_fourth': {
                'base': 16,
                'ratio': 1.333,
                'sizes': {
                    'xs': 9,
                    'sm': 12,
                    'base': 16,
                    'lg': 21,
                    'xl': 28,
                    '2xl': 37,
                    '3xl': 50,
                    '4xl': 67,
                    '5xl': 89
                }
            }
        }
    
    def define_text_styles(self):
        """
        Define text styles for different components
        """
        return {
            'heading_1': {
                'font_size': '5xl',
                'font_weight': 'bold',
                'line_height': 1.2,
                'margin_bottom': 'lg'
            },
            'heading_2': {
                'font_size': '4xl',
                'font_weight': 'bold',
                'line_height': 1.25,
                'margin_bottom': 'md'
            },
            'heading_3': {
                'font_size': '3xl',
                'font_weight': 'semibold',
                'line_height': 1.3,
                'margin_bottom': 'md'
            },
            'body': {
                'font_size': 'base',
                'font_weight': 'normal',
                'line_height': 1.5,
                'margin_bottom': 'sm'
            },
            'caption': {
                'font_size': 'sm',
                'font_weight': 'normal',
                'line_height': 1.4,
                'color': 'text_secondary'
            },
            'button': {
                'font_size': 'base',
                'font_weight': 'semibold',
                'line_height': 1,
                'text_transform': 'none'
            }
        }
    
    def apply_typography_theme(self, theme_name):
        """
        Apply typography theme to the application
        """
        font_stack = self.font_stacks.get(theme_name, self.font_stacks['system'])
        type_scale = self.type_scales['major_third']
        
        typography_css = f"""
        /* Typography Theme: {theme_name} */
        :root {{
            --font-family: {', '.join(font_stack)};
            --font-size-xs: {type_scale['sizes']['xs']}px;
            --font-size-sm: {type_scale['sizes']['sm']}px;
            --font-size-base: {type_scale['sizes']['base']}px;
            --font-size-lg: {type_scale['sizes']['lg']}px;
            --font-size-xl: {type_scale['sizes']['xl']}px;
            --font-size-2xl: {type_scale['sizes']['2xl']}px;
            --font-size-3xl: {type_scale['sizes']['3xl']}px;
            --font-size-4xl: {type_scale['sizes']['4xl']}px;
            --font-size-5xl: {type_scale['sizes']['5xl']}px;
            
            --font-weight-light: 300;
            --font-weight-normal: 400;
            --font-weight-medium: 500;
            --font-weight-semibold: 600;
            --font-weight-bold: 700;
        }}
        
        /* Text style classes */
        .text-xs {{ font-size: var(--font-size-xs); }}
        .text-sm {{ font-size: var(--font-size-sm); }}
        .text-base {{ font-size: var(--font-size-base); }}
        .text-lg {{ font-size: var(--font-size-lg); }}
        .text-xl {{ font-size: var(--font-size-xl); }}
        .text-2xl {{ font-size: var(--font-size-2xl); }}
        .text-3xl {{ font-size: var(--font-size-3xl); }}
        .text-4xl {{ font-size: var(--font-size-4xl); }}
        .text-5xl {{ font-size: var(--font-size-5xl); }}
        
        .font-light {{ font-weight: var(--font-weight-light); }}
        .font-normal {{ font-weight: var(--font-weight-normal); }}
        .font-medium {{ font-weight: var(--font-weight-medium); }}
        .font-semibold {{ font-weight: var(--font-weight-semibold); }}
        .font-bold {{ font-weight: var(--font-weight-bold); }}
        """
        
        return typography_css
```

## 🎛️ Theme Switching

### Dynamic Theme Switcher
```python
class ThemeSwitcher:
    """
    Handle dynamic theme switching functionality
    """
    
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager
        self.user_preferences = UserPreferences()
        
    def create_theme_selector(self):
        """
        Create theme selector UI component
        """
        with st.sidebar:
            st.markdown("### 🎨 Theme Settings")
            
            # Theme selection
            available_themes = list(self.theme_manager.theme_configs.keys())
            current_theme = st.selectbox(
                "Select Theme",
                available_themes,
                index=available_themes.index(self.theme_manager.current_theme),
                key="theme_selector"
            )
            
            # Apply theme if changed
            if current_theme != self.theme_manager.current_theme:
                self.switch_theme(current_theme)
            
            # Color customization
            if st.checkbox("Customize Colors", key="color_customization"):
                self.create_color_customizer()
            
            # Accessibility options
            if st.checkbox("Accessibility Options", key="accessibility_options"):
                self.create_accessibility_controls()
    
    def switch_theme(self, theme_name):
        """
        Switch to a different theme
        """
        try:
            # Load new theme
            self.theme_manager.load_theme(theme_name)
            
            # Save user preference
            self.user_preferences.save_theme_preference(theme_name)
            
            # Show success message
            st.success(f"Theme switched to {theme_name}")
            
            # Rerun to apply changes
            st.experimental_rerun()
            
        except Exception as e:
            st.error(f"Failed to switch theme: {str(e)}")
    
    def create_color_customizer(self):
        """
        Create color customization interface
        """
        st.markdown("#### Custom Colors")
        
        current_colors = self.theme_manager.theme_configs[
            self.theme_manager.current_theme
        ]['colors']
        
        # Primary color picker
        new_primary = st.color_picker(
            "Primary Color",
            value=current_colors['primary'],
            key="primary_color_picker"
        )
        
        # Secondary color picker
        new_secondary = st.color_picker(
            "Secondary Color",
            value=current_colors['secondary'],
            key="secondary_color_picker"
        )
        
        # Accent color picker
        new_accent = st.color_picker(
            "Accent Color",
            value=current_colors['accent'],
            key="accent_color_picker"
        )
        
        # Apply custom colors
        if st.button("Apply Custom Colors", key="apply_custom_colors"):
            self.apply_custom_colors({
                'primary': new_primary,
                'secondary': new_secondary,
                'accent': new_accent
            })
    
    def create_accessibility_controls(self):
        """
        Create accessibility control interface
        """
        st.markdown("#### Accessibility")
        
        # High contrast mode
        high_contrast = st.checkbox(
            "High Contrast Mode",
            key="high_contrast_mode"
        )
        
        # Large text mode
        large_text = st.checkbox(
            "Large Text Mode",
            key="large_text_mode"
        )
        
        # Color blind friendly
        color_blind_friendly = st.checkbox(
            "Color Blind Friendly",
            key="color_blind_friendly"
        )
        
        # Apply accessibility settings
        if st.button("Apply Accessibility Settings", key="apply_accessibility"):
            self.apply_accessibility_settings({
                'high_contrast': high_contrast,
                'large_text': large_text,
                'color_blind_friendly': color_blind_friendly
            })
```

## ♿ Accessibility Features

### Accessibility Manager
```python
class AccessibilityManager:
    """
    Manage accessibility features across themes
    """
    
    def __init__(self):
        self.contrast_ratios = self.define_contrast_requirements()
        self.color_blind_palettes = self.define_color_blind_palettes()
        self.screen_reader_support = ScreenReaderSupport()
        
    def define_contrast_requirements(self):
        """
        Define WCAG contrast ratio requirements
        """
        return {
            'aa_normal': 4.5,      # WCAG AA for normal text
            'aa_large': 3.0,       # WCAG AA for large text
            'aaa_normal': 7.0,     # WCAG AAA for normal text
            'aaa_large': 4.5       # WCAG AAA for large text
        }
    
    def calculate_contrast_ratio(self, color1, color2):
        """
        Calculate contrast ratio between two colors
        """
        def get_relative_luminance(color):
            # Convert hex to RGB
            rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            
            # Convert to relative luminance
            def to_linear(c):
                c = c / 255.0
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            
            r, g, b = [to_linear(c) for c in rgb]
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        l1 = get_relative_luminance(color1)
        l2 = get_relative_luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    def apply_accessibility_features(self, settings):
        """
        Apply accessibility features based on settings
        """
        accessibility_css = ""
        
        if settings.get('high_contrast'):
            accessibility_css += self.generate_high_contrast_css()
        
        if settings.get('large_text'):
            accessibility_css += self.generate_large_text_css()
        
        if settings.get('color_blind_friendly'):
            accessibility_css += self.generate_color_blind_css()
        
        if settings.get('reduced_motion'):
            accessibility_css += self.generate_reduced_motion_css()
        
        return accessibility_css
    
    def generate_high_contrast_css(self):
        """
        Generate high contrast CSS
        """
        return """
        /* High Contrast Mode */
        .high-contrast {
            --primary-color: #000000;
            --background-color: #ffffff;
            --text-color: #000000;
            --border-color: #000000;
        }
        
        .high-contrast .stButton > button {
            background-color: #000000;
            color: #ffffff;
            border: 2px solid #000000;
        }
        
        .high-contrast .stSelectbox > div > div {
            border: 2px solid #000000;
        }
        """
    
    def validate_theme_accessibility(self, theme_config):
        """
        Validate theme for accessibility compliance
        """
        validation_results = {
            'contrast_ratios': {},
            'color_blind_safe': False,
            'keyboard_navigation': True,
            'screen_reader_friendly': True,
            'overall_score': 0
        }
        
        colors = theme_config['colors']
        
        # Check contrast ratios
        text_bg_ratio = self.calculate_contrast_ratio(
            colors['text'], colors['background']
        )
        primary_bg_ratio = self.calculate_contrast_ratio(
            colors['primary'], colors['background']
        )
        
        validation_results['contrast_ratios'] = {
            'text_background': {
                'ratio': text_bg_ratio,
                'passes_aa': text_bg_ratio >= self.contrast_ratios['aa_normal'],
                'passes_aaa': text_bg_ratio >= self.contrast_ratios['aaa_normal']
            },
            'primary_background': {
                'ratio': primary_bg_ratio,
                'passes_aa': primary_bg_ratio >= self.contrast_ratios['aa_normal'],
                'passes_aaa': primary_bg_ratio >= self.contrast_ratios['aaa_normal']
            }
        }
        
        # Calculate overall score
        accessibility_score = 0
        total_checks = 0
        
        for check, results in validation_results['contrast_ratios'].items():
            if results['passes_aa']:
                accessibility_score += 1
            total_checks += 1
        
        validation_results['overall_score'] = accessibility_score / total_checks
        
        return validation_results
```

## 📱 Responsive Theme Features

### Responsive Theme Adapter
```python
class ResponsiveThemeAdapter:
    """
    Adapt themes for different screen sizes and devices
    """
    
    def __init__(self):
        self.breakpoints = self.define_breakpoints()
        self.responsive_adjustments = self.define_responsive_adjustments()
        
    def define_breakpoints(self):
        """
        Define responsive breakpoints
        """
        return {
            'mobile': 480,
            'tablet': 768,
            'desktop': 1024,
            'large_desktop': 1440
        }
    
    def generate_responsive_css(self, theme_config):
        """
        Generate responsive CSS for the theme
        """
        css_rules = []
        
        # Mobile adjustments
        css_rules.append(f"""
        @media (max-width: {self.breakpoints['mobile']}px) {{
            .main {{
                padding: var(--spacing-sm);
            }}
            
            .stButton > button {{
                width: 100%;
                padding: var(--spacing-md);
                font-size: var(--font-size-lg);
            }}
            
            .metric-container {{
                margin: var(--spacing-xs) 0;
                padding: var(--spacing-sm);
            }}
        }}
        """)
        
        # Tablet adjustments
        css_rules.append(f"""
        @media (min-width: {self.breakpoints['mobile'] + 1}px) and (max-width: {self.breakpoints['tablet']}px) {{
            .main {{
                padding: var(--spacing-md);
            }}
            
            .chart-container {{
                padding: var(--spacing-sm);
            }}
        }}
        """)
        
        return '\n'.join(css_rules)
```

## 🔧 Configuration

### Theme System Settings
```python
THEME_SYSTEM_CONFIG = {
    'default_theme': 'light',
    'available_themes': ['light', 'dark', 'corporate', 'high_contrast'],
    'custom_themes_enabled': True,
    'theme_persistence': {
        'enabled': True,
        'storage': 'browser_local_storage',
        'session_duration': 30  # days
    },
    'accessibility': {
        'contrast_checking': True,
        'color_blind_support': True,
        'screen_reader_support': True,
        'keyboard_navigation': True
    },
    'responsive_design': {
        'enabled': True,
        'breakpoints': {
            'mobile': 480,
            'tablet': 768,
            'desktop': 1024
        }
    },
    'performance': {
        'css_minification': True,
        'theme_caching': True,
        'lazy_loading': True
    }
}
```

## 🔗 Related Documentation
- [Responsive Design](responsive-design.md) - Responsive layout system
- [Customization](customization.md) - Theme customization guide
- [Frontend Components](../components/analysis-dashboard.md) - Component styling
- [User Interface](../user-interface/navigation.md) - UI integration