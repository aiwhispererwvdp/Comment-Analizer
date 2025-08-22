# Excel Export Documentation

The Excel Export module provides comprehensive Excel file generation capabilities, creating professional, formatted reports with advanced features like charts, pivot tables, and interactive elements.

## 🎯 Overview

This module transforms analysis results into sophisticated Excel workbooks with multiple sheets, professional formatting, interactive charts, and business-ready presentations suitable for stakeholders and decision-makers.

### Core Capabilities
- **Multi-Sheet Workbooks** - Organized data across multiple sheets
- **Professional Formatting** - Corporate-grade styling and layouts
- **Interactive Charts** - Dynamic visualizations and dashboards
- **Pivot Tables** - Advanced data analysis capabilities
- **Conditional Formatting** - Visual data highlighting and insights

## 🏗️ Excel Export Architecture

### Multi-Sheet Export Framework
```python
class ExcelExportArchitecture:
    """
    Comprehensive Excel export system architecture
    """
    
    WORKBOOK_STRUCTURE = {
        'summary': {
            'purpose': 'Executive summary and key metrics',
            'sections': ['overview', 'key_insights', 'recommendations'],
            'charts': ['sentiment_distribution', 'theme_overview']
        },
        'detailed_analysis': {
            'purpose': 'Complete analysis results',
            'sections': ['all_comments', 'analysis_results', 'confidence_scores'],
            'features': ['filtering', 'sorting', 'conditional_formatting']
        },
        'charts_dashboard': {
            'purpose': 'Visual dashboard with interactive charts',
            'sections': ['sentiment_trends', 'theme_analysis', 'temporal_patterns'],
            'interactivity': ['slicers', 'pivot_charts', 'dynamic_ranges']
        },
        'pivot_analysis': {
            'purpose': 'Pivot tables for deep-dive analysis',
            'sections': ['sentiment_pivot', 'theme_pivot', 'temporal_pivot'],
            'features': ['drill_down', 'calculated_fields', 'custom_grouping']
        },
        'raw_data': {
            'purpose': 'Original comments and metadata',
            'sections': ['original_comments', 'processing_log', 'data_quality'],
            'features': ['data_validation', 'source_tracking']
        }
    }
```

## 📊 Core Excel Generator

### Advanced Excel Workbook Builder
```python
class ExcelExporter:
    """
    Advanced Excel export with comprehensive formatting and features
    """
    
    def __init__(self):
        self.workbook_builder = WorkbookBuilder()
        self.chart_generator = ChartGenerator()
        self.pivot_creator = PivotTableCreator()
        self.formatter = ExcelFormatter()
        self.style_manager = StyleManager()
        
        # Initialize Excel engine
        self.excel_engine = 'openpyxl'  # or 'xlsxwriter'
        
    async def export_analysis_results(self, analysis_results, export_config=None):
        """
        Export comprehensive analysis results to Excel
        """
        # Apply configuration
        config = self.apply_export_config(export_config)
        
        # Create workbook
        workbook = self.workbook_builder.create_workbook()
        
        # Generate all sheets
        sheets = await self.generate_all_sheets(analysis_results, config)
        
        # Add sheets to workbook
        for sheet_name, sheet_data in sheets.items():
            await self.add_sheet_to_workbook(workbook, sheet_name, sheet_data)
        
        # Apply workbook-level formatting
        self.apply_workbook_formatting(workbook, config)
        
        # Generate file
        output_path = await self.save_workbook(workbook, config)
        
        return {
            'file_path': output_path,
            'sheets_created': list(sheets.keys()),
            'file_size': self.get_file_size(output_path),
            'creation_timestamp': datetime.now(),
            'export_metadata': self.generate_export_metadata(analysis_results, config)
        }
    
    async def generate_all_sheets(self, analysis_results, config):
        """
        Generate all Excel sheets based on configuration
        """
        sheets = {}
        
        # Summary sheet
        if config.get('include_summary', True):
            sheets['Summary'] = await self.generate_summary_sheet(analysis_results)
        
        # Detailed analysis sheet
        if config.get('include_detailed', True):
            sheets['Detailed Analysis'] = await self.generate_detailed_sheet(analysis_results)
        
        # Charts dashboard
        if config.get('include_charts', True):
            sheets['Charts Dashboard'] = await self.generate_charts_sheet(analysis_results)
        
        # Pivot tables
        if config.get('include_pivots', True):
            pivot_sheets = await self.generate_pivot_sheets(analysis_results)
            sheets.update(pivot_sheets)
        
        # Raw data
        if config.get('include_raw_data', True):
            sheets['Raw Data'] = await self.generate_raw_data_sheet(analysis_results)
        
        return sheets
```

## 📈 Summary Sheet Generation

### Executive Summary Builder
```python
class SummarySheetGenerator:
    """
    Generate executive summary sheet with key insights
    """
    
    def __init__(self):
        self.kpi_calculator = KPICalculator()
        self.insight_generator = InsightGenerator()
        self.chart_creator = SummaryChartCreator()
    
    async def generate_summary_sheet(self, analysis_results):
        """
        Generate comprehensive summary sheet
        """
        # Calculate key metrics
        key_metrics = self.kpi_calculator.calculate_key_metrics(analysis_results)
        
        # Generate insights
        key_insights = self.insight_generator.generate_key_insights(analysis_results)
        
        # Create summary structure
        summary_data = {
            'header': self.create_summary_header(),
            'key_metrics': key_metrics,
            'insights': key_insights,
            'charts': await self.create_summary_charts(analysis_results),
            'recommendations': self.generate_recommendations(analysis_results)
        }
        
        return summary_data
    
    def create_summary_header(self):
        """
        Create professional summary header
        """
        return {
            'title': 'Customer Feedback Analysis Summary',
            'subtitle': 'Personal Paraguay Fiber Comments Analysis',
            'generated_date': datetime.now().strftime('%B %d, %Y'),
            'generated_time': datetime.now().strftime('%I:%M %p'),
            'logo': self.get_company_logo(),
            'styling': {
                'title_font': 'Calibri',
                'title_size': 18,
                'title_bold': True,
                'subtitle_size': 14,
                'date_size': 10
            }
        }
    
    async def create_summary_charts(self, analysis_results):
        """
        Create charts for summary sheet
        """
        charts = {}
        
        # Sentiment distribution pie chart
        charts['sentiment_pie'] = await self.chart_creator.create_sentiment_pie_chart(
            analysis_results
        )
        
        # Top themes bar chart
        charts['themes_bar'] = await self.chart_creator.create_themes_bar_chart(
            analysis_results
        )
        
        # Confidence gauge chart
        charts['confidence_gauge'] = await self.chart_creator.create_confidence_gauge(
            analysis_results
        )
        
        # Temporal trend line chart
        charts['temporal_trend'] = await self.chart_creator.create_temporal_trend(
            analysis_results
        )
        
        return charts
```

## 📋 Detailed Analysis Sheet

### Comprehensive Data Sheet Builder
```python
class DetailedSheetGenerator:
    """
    Generate detailed analysis sheet with all results
    """
    
    def __init__(self):
        self.data_formatter = DataFormatter()
        self.conditional_formatter = ConditionalFormatter()
        self.filter_creator = FilterCreator()
    
    async def generate_detailed_sheet(self, analysis_results):
        """
        Generate detailed analysis sheet with full data
        """
        # Prepare detailed data
        detailed_data = self.prepare_detailed_data(analysis_results)
        
        # Create column headers
        headers = self.create_detailed_headers()
        
        # Apply data formatting
        formatted_data = self.data_formatter.format_analysis_data(detailed_data)
        
        # Create conditional formatting rules
        conditional_rules = self.conditional_formatter.create_analysis_rules()
        
        # Create filters and sorting
        filter_config = self.filter_creator.create_analysis_filters(headers)
        
        return {
            'headers': headers,
            'data': formatted_data,
            'conditional_formatting': conditional_rules,
            'filters': filter_config,
            'column_widths': self.calculate_optimal_column_widths(headers, formatted_data),
            'freeze_panes': (1, 2)  # Freeze header row and first column
        }
    
    def create_detailed_headers(self):
        """
        Create comprehensive column headers for detailed analysis
        """
        return [
            {'name': 'Comment ID', 'width': 12, 'type': 'text'},
            {'name': 'Original Text', 'width': 50, 'type': 'text'},
            {'name': 'Language', 'width': 10, 'type': 'text'},
            {'name': 'Sentiment', 'width': 12, 'type': 'text'},
            {'name': 'Sentiment Score', 'width': 15, 'type': 'number', 'format': '0.00'},
            {'name': 'Primary Theme', 'width': 20, 'type': 'text'},
            {'name': 'Secondary Themes', 'width': 30, 'type': 'text'},
            {'name': 'Primary Emotion', 'width': 15, 'type': 'text'},
            {'name': 'Emotion Intensity', 'width': 15, 'type': 'number', 'format': '0.00'},
            {'name': 'Confidence Score', 'width': 15, 'type': 'number', 'format': '0.00'},
            {'name': 'Processing Date', 'width': 15, 'type': 'date'},
            {'name': 'Quality Flag', 'width': 12, 'type': 'text'}
        ]
    
    def prepare_detailed_data(self, analysis_results):
        """
        Prepare detailed data rows from analysis results
        """
        detailed_rows = []
        
        for result in analysis_results:
            row = [
                result.get('comment_id', ''),
                result.get('original_text', ''),
                result['analysis']['language']['detected'],
                result['analysis']['sentiment']['polarity'],
                result['analysis']['sentiment']['score'],
                result['analysis']['themes']['primary_themes'][0] if result['analysis']['themes']['primary_themes'] else '',
                ', '.join(result['analysis']['themes']['secondary_themes']),
                result['analysis']['emotions']['primary_emotion'],
                result['analysis']['emotions']['intensity'],
                result['quality_indicators']['overall_confidence'],
                result['metadata']['processing_timestamp'],
                self.determine_quality_flag(result)
            ]
            
            detailed_rows.append(row)
        
        return detailed_rows
```

## 📊 Chart Generation

### Interactive Chart Creator
```python
class ChartGenerator:
    """
    Generate interactive charts for Excel workbooks
    """
    
    def __init__(self):
        self.color_palette = ColorPalette()
        self.chart_styler = ChartStyler()
    
    async def create_sentiment_distribution_chart(self, analysis_results):
        """
        Create sentiment distribution chart
        """
        # Calculate sentiment distribution
        sentiment_counts = self.calculate_sentiment_distribution(analysis_results)
        
        # Create pie chart
        chart_config = {
            'type': 'pie',
            'title': 'Sentiment Distribution',
            'data': {
                'labels': list(sentiment_counts.keys()),
                'values': list(sentiment_counts.values())
            },
            'styling': {
                'colors': self.color_palette.get_sentiment_colors(),
                'title_font_size': 14,
                'data_labels': True,
                'legend_position': 'right'
            },
            'position': {
                'anchor_cell': 'A15',
                'width': 400,
                'height': 300
            }
        }
        
        return chart_config
    
    async def create_theme_analysis_chart(self, analysis_results):
        """
        Create theme analysis bar chart
        """
        # Calculate theme frequencies
        theme_frequencies = self.calculate_theme_frequencies(analysis_results)
        
        # Sort by frequency
        sorted_themes = sorted(
            theme_frequencies.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]  # Top 10 themes
        
        # Create horizontal bar chart
        chart_config = {
            'type': 'horizontal_bar',
            'title': 'Top 10 Themes',
            'data': {
                'categories': [theme[0] for theme in sorted_themes],
                'values': [theme[1] for theme in sorted_themes]
            },
            'styling': {
                'colors': self.color_palette.get_theme_colors(),
                'title_font_size': 14,
                'data_labels': True,
                'grid_lines': True
            },
            'position': {
                'anchor_cell': 'F15',
                'width': 500,
                'height': 350
            }
        }
        
        return chart_config
    
    async def create_temporal_trend_chart(self, analysis_results):
        """
        Create temporal trend line chart
        """
        # Group by time periods
        temporal_data = self.group_by_temporal_periods(analysis_results)
        
        # Create line chart
        chart_config = {
            'type': 'line',
            'title': 'Sentiment Trend Over Time',
            'data': {
                'categories': list(temporal_data.keys()),
                'series': [
                    {
                        'name': 'Average Sentiment',
                        'values': [data['avg_sentiment'] for data in temporal_data.values()],
                        'color': '#2E86AB'
                    },
                    {
                        'name': 'Comment Volume',
                        'values': [data['comment_count'] for data in temporal_data.values()],
                        'color': '#A23B72',
                        'y_axis': 'secondary'
                    }
                ]
            },
            'styling': {
                'title_font_size': 14,
                'smooth_lines': True,
                'markers': True,
                'grid_lines': True
            },
            'position': {
                'anchor_cell': 'A35',
                'width': 600,
                'height': 300
            }
        }
        
        return chart_config
```

## 🔄 Pivot Table Creation

### Advanced Pivot Table Builder
```python
class PivotTableCreator:
    """
    Create sophisticated pivot tables for data analysis
    """
    
    def __init__(self):
        self.pivot_designer = PivotDesigner()
        self.calculated_fields = CalculatedFieldsManager()
    
    async def create_sentiment_pivot(self, analysis_results):
        """
        Create sentiment analysis pivot table
        """
        # Prepare pivot data source
        pivot_data = self.prepare_pivot_data(analysis_results)
        
        # Define pivot table structure
        pivot_config = {
            'name': 'Sentiment Analysis Pivot',
            'source_data': pivot_data,
            'location': 'Sentiment_Pivot!A1',
            'structure': {
                'rows': ['Primary_Theme', 'Language'],
                'columns': ['Sentiment'],
                'values': [
                    {'field': 'Comment_Count', 'function': 'count'},
                    {'field': 'Sentiment_Score', 'function': 'average'},
                    {'field': 'Confidence_Score', 'function': 'average'}
                ],
                'filters': ['Processing_Date', 'Quality_Flag']
            },
            'formatting': {
                'number_format': {
                    'Sentiment_Score': '0.00',
                    'Confidence_Score': '0.00%'
                },
                'conditional_formatting': {
                    'Sentiment_Score': self.create_sentiment_color_scale()
                }
            }
        }
        
        return pivot_config
    
    async def create_theme_analysis_pivot(self, analysis_results):
        """
        Create theme analysis pivot table
        """
        pivot_config = {
            'name': 'Theme Analysis Pivot',
            'source_data': self.prepare_theme_pivot_data(analysis_results),
            'location': 'Theme_Pivot!A1',
            'structure': {
                'rows': ['Primary_Theme', 'Secondary_Theme'],
                'columns': ['Sentiment', 'Primary_Emotion'],
                'values': [
                    {'field': 'Comment_Count', 'function': 'count'},
                    {'field': 'Theme_Confidence', 'function': 'average'},
                    {'field': 'Emotion_Intensity', 'function': 'average'}
                ],
                'filters': ['Language', 'Processing_Date']
            },
            'calculated_fields': [
                {
                    'name': 'Theme_Sentiment_Score',
                    'formula': 'Sentiment_Score * Theme_Confidence',
                    'format': '0.00'
                }
            ]
        }
        
        return pivot_config
```

## 🎨 Professional Formatting

### Advanced Excel Formatting
```python
class ExcelFormatter:
    """
    Apply professional formatting to Excel workbooks
    """
    
    def __init__(self):
        self.corporate_styles = CorporateStyles()
        self.color_scheme = ColorScheme()
        self.font_manager = FontManager()
    
    def apply_summary_formatting(self, worksheet, summary_data):
        """
        Apply professional formatting to summary sheet
        """
        # Header formatting
        self.format_summary_header(worksheet, summary_data['header'])
        
        # Key metrics formatting
        self.format_key_metrics(worksheet, summary_data['key_metrics'])
        
        # Insights formatting
        self.format_insights_section(worksheet, summary_data['insights'])
        
        # Chart positioning
        self.position_summary_charts(worksheet, summary_data['charts'])
        
        # Apply corporate styling
        self.apply_corporate_theme(worksheet)
    
    def format_summary_header(self, worksheet, header_data):
        """
        Format the summary sheet header
        """
        # Title
        title_cell = worksheet['A1']
        title_cell.value = header_data['title']
        title_cell.font = Font(
            name=header_data['styling']['title_font'],
            size=header_data['styling']['title_size'],
            bold=header_data['styling']['title_bold'],
            color='1F4E79'
        )
        
        # Subtitle
        subtitle_cell = worksheet['A2']
        subtitle_cell.value = header_data['subtitle']
        subtitle_cell.font = Font(
            name='Calibri',
            size=header_data['styling']['subtitle_size'],
            color='5B9BD5'
        )
        
        # Date and time
        date_cell = worksheet['A3']
        date_cell.value = f"Generated: {header_data['generated_date']} at {header_data['generated_time']}"
        date_cell.font = Font(
            name='Calibri',
            size=header_data['styling']['date_size'],
            italic=True,
            color='7F7F7F'
        )
    
    def create_conditional_formatting_rules(self):
        """
        Create conditional formatting rules for analysis data
        """
        rules = {}
        
        # Sentiment score color scale
        rules['sentiment_score'] = {
            'type': '3_color_scale',
            'min_color': 'F8696B',  # Red for negative
            'mid_color': 'FFEB9C',  # Yellow for neutral
            'max_color': '63BE7B'   # Green for positive
        }
        
        # Confidence score color scale
        rules['confidence_score'] = {
            'type': '3_color_scale',
            'min_color': 'F8696B',  # Red for low confidence
            'mid_color': 'FFEB9C',  # Yellow for medium confidence
            'max_color': '63BE7B'   # Green for high confidence
        }
        
        # Data quality indicators
        rules['quality_flag'] = {
            'type': 'icon_set',
            'icon_style': 'traffic_lights',
            'conditions': {
                'High': 'green',
                'Medium': 'yellow',
                'Low': 'red'
            }
        }
        
        return rules
```

## 📱 Interactive Features

### Excel Interactivity Builder
```python
class InteractivityBuilder:
    """
    Add interactive features to Excel workbooks
    """
    
    def __init__(self):
        self.slicer_creator = SlicerCreator()
        self.dynamic_range_manager = DynamicRangeManager()
        self.form_control_builder = FormControlBuilder()
    
    def add_dashboard_interactivity(self, workbook, analysis_results):
        """
        Add interactive elements to dashboard
        """
        dashboard_sheet = workbook['Charts Dashboard']
        
        # Add slicers for filtering
        slicers = self.create_dashboard_slicers(analysis_results)
        for slicer in slicers:
            self.slicer_creator.add_slicer(dashboard_sheet, slicer)
        
        # Add dynamic charts that respond to slicers
        dynamic_charts = self.create_dynamic_charts(analysis_results)
        for chart in dynamic_charts:
            self.add_dynamic_chart(dashboard_sheet, chart)
        
        # Add dropdown filters
        dropdowns = self.create_filter_dropdowns()
        for dropdown in dropdowns:
            self.form_control_builder.add_dropdown(dashboard_sheet, dropdown)
    
    def create_dashboard_slicers(self, analysis_results):
        """
        Create slicers for dashboard filtering
        """
        slicers = [
            {
                'name': 'Language_Slicer',
                'source': 'Language',
                'position': {'row': 1, 'column': 1},
                'style': 'SlicerStyleLight3'
            },
            {
                'name': 'Sentiment_Slicer',
                'source': 'Sentiment',
                'position': {'row': 1, 'column': 3},
                'style': 'SlicerStyleLight5'
            },
            {
                'name': 'Theme_Slicer',
                'source': 'Primary_Theme',
                'position': {'row': 1, 'column': 5},
                'style': 'SlicerStyleLight6'
            }
        ]
        
        return slicers
```

## 📄 Report Templates

### Customizable Report Templates
```python
class ReportTemplateManager:
    """
    Manage and customize Excel report templates
    """
    
    def __init__(self):
        self.template_library = TemplateLibrary()
        self.customization_engine = CustomizationEngine()
    
    def create_executive_template(self):
        """
        Create executive summary template
        """
        template = {
            'name': 'Executive Summary',
            'description': 'High-level overview for executives',
            'sheets': ['Executive Summary', 'Key Insights', 'Action Items'],
            'features': [
                'executive_dashboard',
                'key_metrics_cards',
                'trend_analysis',
                'recommendations'
            ],
            'styling': {
                'theme': 'corporate_blue',
                'font_family': 'Calibri',
                'color_scheme': 'professional'
            }
        }
        
        return template
    
    def create_detailed_template(self):
        """
        Create detailed analysis template
        """
        template = {
            'name': 'Detailed Analysis',
            'description': 'Comprehensive analysis for analysts',
            'sheets': [
                'Summary',
                'Detailed Results',
                'Charts',
                'Pivot Analysis',
                'Raw Data'
            ],
            'features': [
                'full_data_export',
                'interactive_charts',
                'pivot_tables',
                'filtering_and_sorting',
                'conditional_formatting'
            ],
            'styling': {
                'theme': 'professional_gray',
                'font_family': 'Calibri',
                'color_scheme': 'analytical'
            }
        }
        
        return template
```

## 🔧 Configuration

### Excel Export Settings
```python
EXCEL_EXPORT_CONFIG = {
    'default_template': 'comprehensive',
    'file_naming': {
        'pattern': 'feedback_analysis_{timestamp}',
        'timestamp_format': '%Y%m%d_%H%M%S',
        'include_metadata': True
    },
    'sheets': {
        'summary': True,
        'detailed_analysis': True,
        'charts_dashboard': True,
        'pivot_tables': True,
        'raw_data': True
    },
    'formatting': {
        'corporate_theme': True,
        'conditional_formatting': True,
        'auto_column_width': True,
        'freeze_panes': True
    },
    'charts': {
        'include_charts': True,
        'chart_types': ['pie', 'bar', 'line', 'scatter'],
        'interactive_features': True,
        'color_scheme': 'professional'
    },
    'interactivity': {
        'slicers': True,
        'pivot_tables': True,
        'dynamic_ranges': True,
        'form_controls': True
    },
    'performance': {
        'optimize_file_size': True,
        'compress_images': True,
        'limit_precision': 2
    }
}
```

## 🔗 Related Documentation
- [Report Generation](report-generation.md) - Report creation process
- [Visualization](visualization.md) - Chart and graph creation
- [Analysis Results](../analysis-engines/sentiment-analysis.md) - Analysis output format
- [Data Export](../../user-guides/tutorials/export-workflows.md) - Export tutorials