# Visualization Documentation

The Visualization module creates interactive charts, graphs, and visual dashboards to present analysis results in an intuitive and engaging format for different audiences and use cases.

## 🎯 Overview

This module transforms complex analysis data into clear, actionable visualizations using modern charting libraries and interactive frameworks, enabling stakeholders to quickly understand insights and make data-driven decisions.

### Core Capabilities
- **Interactive Charts** - Dynamic, responsive visualizations
- **Multi-Type Visualizations** - Charts, graphs, heatmaps, and dashboards
- **Real-Time Updates** - Live data visualization capabilities
- **Export Flexibility** - Multiple format support (PNG, SVG, PDF, HTML)
- **Accessibility Features** - Screen reader and mobile-friendly designs

## 🏗️ Visualization Architecture

### Multi-Layer Visualization Framework
```python
class VisualizationArchitecture:
    """
    Comprehensive visualization system architecture
    """
    
    VISUALIZATION_TYPES = {
        'statistical': {
            'charts': ['bar', 'line', 'pie', 'scatter', 'histogram', 'box_plot'],
            'use_cases': ['distribution_analysis', 'trend_analysis', 'comparison'],
            'libraries': ['plotly', 'matplotlib', 'seaborn']
        },
        'network': {
            'charts': ['network_graph', 'sankey', 'chord', 'tree'],
            'use_cases': ['relationship_analysis', 'flow_analysis', 'hierarchy'],
            'libraries': ['networkx', 'plotly', 'd3js']
        },
        'geographic': {
            'charts': ['choropleth', 'scatter_mapbox', 'heatmap'],
            'use_cases': ['location_analysis', 'regional_comparison'],
            'libraries': ['plotly', 'folium', 'geopandas']
        },
        'temporal': {
            'charts': ['time_series', 'gantt', 'timeline', 'calendar_heatmap'],
            'use_cases': ['time_analysis', 'pattern_detection', 'forecasting'],
            'libraries': ['plotly', 'matplotlib', 'altair']
        },
        'text': {
            'charts': ['word_cloud', 'sentiment_flow', 'topic_evolution'],
            'use_cases': ['text_analysis', 'sentiment_visualization', 'topic_modeling'],
            'libraries': ['wordcloud', 'plotly', 'pyldavis']
        }
    }
    
    DASHBOARD_FRAMEWORKS = {
        'streamlit': 'Python-based web app framework',
        'plotly_dash': 'Interactive web dashboard framework',
        'bokeh': 'Interactive visualization library',
        'shiny': 'R-based web application framework'
    }
```

## 🎨 Core Visualization Engine

### Master Visualization Creator
```python
class VisualizationEngine:
    """
    Master visualization engine coordinating all chart creation
    """
    
    def __init__(self):
        self.chart_factories = {
            'plotly': PlotlyChartFactory(),
            'matplotlib': MatplotlibChartFactory(),
            'seaborn': SeabornChartFactory(),
            'bokeh': BokehChartFactory()
        }
        
        self.dashboard_builders = {
            'streamlit': StreamlitDashboardBuilder(),
            'plotly_dash': PlotlyDashboardBuilder(),
            'static': StaticDashboardBuilder()
        }
        
        self.style_manager = VisualizationStyleManager()
        self.color_palette = ColorPaletteManager()
        self.interaction_manager = InteractionManager()
        
    async def create_visualization_suite(self, analysis_results, viz_config):
        """
        Create comprehensive visualization suite from analysis results
        """
        # Validate configuration
        validated_config = self.validate_config(viz_config)
        
        # Create visualization session
        viz_session = VisualizationSession(
            session_id=self.generate_session_id(),
            config=validated_config,
            timestamp=datetime.now()
        )
        
        try:
            # Phase 1: Data preparation
            prepared_data = await self.prepare_visualization_data(
                analysis_results,
                viz_session
            )
            
            # Phase 2: Individual chart creation
            individual_charts = await self.create_individual_charts(
                prepared_data,
                viz_session
            )
            
            # Phase 3: Dashboard creation
            dashboards = await self.create_dashboards(
                prepared_data,
                individual_charts,
                viz_session
            )
            
            # Phase 4: Export and packaging
            exported_visualizations = await self.export_visualizations(
                individual_charts,
                dashboards,
                viz_session
            )
            
            return {
                'individual_charts': individual_charts,
                'dashboards': dashboards,
                'exported_files': exported_visualizations,
                'session_metadata': viz_session.get_metadata()
            }
            
        except Exception as e:
            return await self.handle_visualization_error(e, viz_session)
    
    async def create_individual_charts(self, data, session):
        """
        Create individual charts based on analysis data
        """
        charts = {}
        
        # Sentiment analysis charts
        if 'sentiment' in data:
            charts['sentiment'] = await self.create_sentiment_charts(
                data['sentiment'],
                session.config.get('sentiment_config', {})
            )
        
        # Theme analysis charts
        if 'themes' in data:
            charts['themes'] = await self.create_theme_charts(
                data['themes'],
                session.config.get('theme_config', {})
            )
        
        # Temporal analysis charts
        if 'temporal' in data:
            charts['temporal'] = await self.create_temporal_charts(
                data['temporal'],
                session.config.get('temporal_config', {})
            )
        
        # Emotion analysis charts
        if 'emotions' in data:
            charts['emotions'] = await self.create_emotion_charts(
                data['emotions'],
                session.config.get('emotion_config', {})
            )
        
        # Language analysis charts
        if 'languages' in data:
            charts['languages'] = await self.create_language_charts(
                data['languages'],
                session.config.get('language_config', {})
            )
        
        return charts
```

## 📊 Sentiment Visualization

### Sentiment Analysis Charts
```python
class SentimentVisualizationCreator:
    """
    Create sentiment-specific visualizations
    """
    
    def __init__(self):
        self.chart_factory = PlotlyChartFactory()
        self.color_palette = SentimentColorPalette()
        
    async def create_sentiment_charts(self, sentiment_data, config):
        """
        Create comprehensive sentiment visualization suite
        """
        charts = {}
        
        # Sentiment distribution pie chart
        charts['sentiment_distribution'] = await self.create_sentiment_pie_chart(
            sentiment_data['distribution']
        )
        
        # Sentiment over time line chart
        charts['sentiment_timeline'] = await self.create_sentiment_timeline(
            sentiment_data['temporal']
        )
        
        # Sentiment by theme heatmap
        charts['sentiment_theme_heatmap'] = await self.create_sentiment_theme_heatmap(
            sentiment_data['by_theme']
        )
        
        # Sentiment confidence scatter plot
        charts['sentiment_confidence'] = await self.create_sentiment_confidence_scatter(
            sentiment_data['confidence_scores']
        )
        
        # Sentiment word cloud
        charts['sentiment_wordcloud'] = await self.create_sentiment_wordcloud(
            sentiment_data['text_by_sentiment']
        )
        
        return charts
    
    async def create_sentiment_pie_chart(self, distribution_data):
        """
        Create interactive sentiment distribution pie chart
        """
        # Prepare data
        labels = list(distribution_data.keys())
        values = list(distribution_data.values())
        colors = self.color_palette.get_sentiment_colors(labels)
        
        # Create Plotly pie chart
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>(%{value} comments)',
            hovertemplate='<b>%{label}</b><br>' +
                         'Count: %{value}<br>' +
                         'Percentage: %{percent}<br>' +
                         '<extra></extra>',
            hole=0.4  # Donut chart style
        )])
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Sentiment Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'family': 'Arial, sans-serif'}
            },
            font={'family': 'Arial, sans-serif'},
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            ),
            margin=dict(t=60, b=20, l=20, r=120),
            annotations=[
                dict(
                    text='Total<br>Comments',
                    x=0.5, y=0.5,
                    font_size=14,
                    showarrow=False
                )
            ]
        )
        
        return {
            'chart': fig,
            'type': 'pie',
            'title': 'Sentiment Distribution',
            'description': 'Distribution of sentiment across all analyzed comments',
            'export_formats': ['png', 'svg', 'html', 'pdf']
        }
    
    async def create_sentiment_timeline(self, temporal_data):
        """
        Create sentiment trend over time line chart
        """
        # Prepare data
        dates = list(temporal_data.keys())
        avg_sentiments = [data['avg_sentiment'] for data in temporal_data.values()]
        comment_counts = [data['comment_count'] for data in temporal_data.values()]
        
        # Create dual-axis line chart
        fig = make_subplots(
            specs=[[{"secondary_y": True}]],
            subplot_titles=("Sentiment Trend Over Time",)
        )
        
        # Add sentiment trend line
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=avg_sentiments,
                mode='lines+markers',
                name='Average Sentiment',
                line=dict(color='#2E86AB', width=3),
                marker=dict(size=6),
                hovertemplate='Date: %{x}<br>' +
                             'Avg Sentiment: %{y:.2f}<br>' +
                             '<extra></extra>'
            ),
            secondary_y=False,
        )
        
        # Add comment volume bars
        fig.add_trace(
            go.Bar(
                x=dates,
                y=comment_counts,
                name='Comment Volume',
                marker_color='rgba(174, 199, 232, 0.5)',
                hovertemplate='Date: %{x}<br>' +
                             'Comments: %{y}<br>' +
                             '<extra></extra>'
            ),
            secondary_y=True,
        )
        
        # Update layout
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Average Sentiment Score", secondary_y=False)
        fig.update_yaxes(title_text="Number of Comments", secondary_y=True)
        
        fig.update_layout(
            title={
                'text': 'Sentiment Trend Over Time',
                'x': 0.5,
                'xanchor': 'center'
            },
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return {
            'chart': fig,
            'type': 'line',
            'title': 'Sentiment Timeline',
            'description': 'Sentiment trends and comment volume over time',
            'export_formats': ['png', 'svg', 'html', 'pdf']
        }
```

## 🏷️ Theme Visualization

### Theme Analysis Charts
```python
class ThemeVisualizationCreator:
    """
    Create theme-specific visualizations
    """
    
    def __init__(self):
        self.chart_factory = PlotlyChartFactory()
        self.network_builder = NetworkGraphBuilder()
        
    async def create_theme_charts(self, theme_data, config):
        """
        Create comprehensive theme visualization suite
        """
        charts = {}
        
        # Theme frequency bar chart
        charts['theme_frequency'] = await self.create_theme_frequency_chart(
            theme_data['frequencies']
        )
        
        # Theme relationship network
        charts['theme_network'] = await self.create_theme_network_graph(
            theme_data['relationships']
        )
        
        # Theme-sentiment heatmap
        charts['theme_sentiment_heatmap'] = await self.create_theme_sentiment_heatmap(
            theme_data['sentiment_by_theme']
        )
        
        # Theme evolution over time
        charts['theme_evolution'] = await self.create_theme_evolution_chart(
            theme_data['temporal_evolution']
        )
        
        # Theme word clouds
        charts['theme_wordclouds'] = await self.create_theme_wordclouds(
            theme_data['theme_texts']
        )
        
        return charts
    
    async def create_theme_frequency_chart(self, frequency_data):
        """
        Create horizontal bar chart of theme frequencies
        """
        # Sort themes by frequency
        sorted_themes = sorted(
            frequency_data.items(),
            key=lambda x: x[1],
            reverse=True
        )[:15]  # Top 15 themes
        
        themes = [item[0] for item in sorted_themes]
        frequencies = [item[1] for item in sorted_themes]
        
        # Create horizontal bar chart
        fig = go.Figure(data=[
            go.Bar(
                y=themes,
                x=frequencies,
                orientation='h',
                marker=dict(
                    color=frequencies,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Frequency")
                ),
                text=frequencies,
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>' +
                             'Frequency: %{x}<br>' +
                             '<extra></extra>'
            )
        ])
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'Top Themes by Frequency',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title="Frequency",
            yaxis_title="Themes",
            yaxis=dict(automargin=True),
            height=max(400, len(themes) * 30),
            margin=dict(l=200, r=50, t=60, b=50)
        )
        
        return {
            'chart': fig,
            'type': 'horizontal_bar',
            'title': 'Theme Frequency Analysis',
            'description': 'Most frequently mentioned themes in customer feedback',
            'export_formats': ['png', 'svg', 'html', 'pdf']
        }
    
    async def create_theme_network_graph(self, relationship_data):
        """
        Create network graph showing theme relationships
        """
        # Build network graph
        network = self.network_builder.build_theme_network(relationship_data)
        
        # Calculate node positions using layout algorithm
        pos = nx.spring_layout(network, k=1, iterations=50)
        
        # Prepare node trace
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        
        for node in network.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            node_size.append(network.degree(node) * 10 + 10)
        
        # Prepare edge trace
        edge_x = []
        edge_y = []
        
        for edge in network.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Create traces
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='rgba(50,50,50,0.5)'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                size=node_size,
                color='lightblue',
                line=dict(width=2, color='darkblue')
            ),
            hovertemplate='<b>%{text}</b><br>' +
                         'Connections: %{marker.size}<br>' +
                         '<extra></extra>'
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace])
        
        fig.update_layout(
            title='Theme Relationship Network',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Themes connected by co-occurrence in comments",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color='gray', size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        return {
            'chart': fig,
            'type': 'network',
            'title': 'Theme Network Analysis',
            'description': 'Network showing relationships between themes',
            'export_formats': ['png', 'svg', 'html']
        }
```

## 📅 Temporal Visualization

### Time-Based Analysis Charts
```python
class TemporalVisualizationCreator:
    """
    Create time-based visualizations
    """
    
    def __init__(self):
        self.chart_factory = PlotlyChartFactory()
        
    async def create_temporal_charts(self, temporal_data, config):
        """
        Create comprehensive temporal visualization suite
        """
        charts = {}
        
        # Volume over time
        charts['volume_timeline'] = await self.create_volume_timeline(
            temporal_data['volume']
        )
        
        # Hourly pattern heatmap
        charts['hourly_heatmap'] = await self.create_hourly_pattern_heatmap(
            temporal_data['hourly_patterns']
        )
        
        # Weekly pattern analysis
        charts['weekly_patterns'] = await self.create_weekly_pattern_chart(
            temporal_data['weekly_patterns']
        )
        
        # Seasonal trends
        charts['seasonal_trends'] = await self.create_seasonal_trends_chart(
            temporal_data['seasonal_data']
        )
        
        return charts
    
    async def create_hourly_pattern_heatmap(self, hourly_data):
        """
        Create heatmap showing hourly comment patterns
        """
        # Prepare data matrix
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours = list(range(24))
        
        # Create data matrix
        heatmap_data = []
        for day in days:
            day_data = []
            for hour in hours:
                count = hourly_data.get(day, {}).get(hour, 0)
                day_data.append(count)
            heatmap_data.append(day_data)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=[f"{h:02d}:00" for h in hours],
            y=days,
            colorscale='Blues',
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>' +
                         'Hour: %{x}<br>' +
                         'Comments: %{z}<br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title='Comment Activity by Hour and Day',
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week",
            font={'family': 'Arial, sans-serif'}
        )
        
        return {
            'chart': fig,
            'type': 'heatmap',
            'title': 'Hourly Activity Patterns',
            'description': 'Comment activity patterns by hour and day of week',
            'export_formats': ['png', 'svg', 'html', 'pdf']
        }
```

## 🎭 Emotion Visualization

### Emotion Analysis Charts
```python
class EmotionVisualizationCreator:
    """
    Create emotion-specific visualizations
    """
    
    def __init__(self):
        self.chart_factory = PlotlyChartFactory()
        self.emotion_colors = EmotionColorPalette()
        
    async def create_emotion_charts(self, emotion_data, config):
        """
        Create comprehensive emotion visualization suite
        """
        charts = {}
        
        # Emotion distribution radar chart
        charts['emotion_radar'] = await self.create_emotion_radar_chart(
            emotion_data['distribution']
        )
        
        # Emotion intensity histogram
        charts['emotion_intensity'] = await self.create_emotion_intensity_chart(
            emotion_data['intensity_distribution']
        )
        
        # Emotion-theme correlation
        charts['emotion_theme_correlation'] = await self.create_emotion_theme_correlation(
            emotion_data['theme_correlations']
        )
        
        # Emotion evolution over time
        charts['emotion_timeline'] = await self.create_emotion_timeline(
            emotion_data['temporal_evolution']
        )
        
        return charts
    
    async def create_emotion_radar_chart(self, distribution_data):
        """
        Create radar chart showing emotion distribution
        """
        emotions = list(distribution_data.keys())
        values = list(distribution_data.values())
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=emotions,
            fill='toself',
            name='Emotion Distribution',
            marker=dict(color='rgba(46, 134, 171, 0.6)'),
            line=dict(color='rgba(46, 134, 171, 1.0)', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) * 1.1]
                )
            ),
            title={
                'text': 'Emotion Distribution',
                'x': 0.5,
                'xanchor': 'center'
            },
            showlegend=False
        )
        
        return {
            'chart': fig,
            'type': 'radar',
            'title': 'Emotion Distribution Radar',
            'description': 'Distribution of emotions detected in customer feedback',
            'export_formats': ['png', 'svg', 'html', 'pdf']
        }
```

## 📱 Interactive Dashboards

### Streamlit Dashboard Builder
```python
class StreamlitDashboardBuilder:
    """
    Build interactive Streamlit dashboards
    """
    
    def __init__(self):
        self.component_builder = StreamlitComponentBuilder()
        self.layout_manager = StreamlitLayoutManager()
        
    async def create_analysis_dashboard(self, analysis_results, charts):
        """
        Create comprehensive analysis dashboard
        """
        dashboard_components = {
            'header': self.create_dashboard_header(),
            'sidebar': self.create_dashboard_sidebar(analysis_results),
            'overview': self.create_overview_section(analysis_results),
            'sentiment_section': self.create_sentiment_section(charts['sentiment']),
            'theme_section': self.create_theme_section(charts['themes']),
            'temporal_section': self.create_temporal_section(charts['temporal']),
            'detailed_analysis': self.create_detailed_analysis_section(analysis_results)
        }
        
        return dashboard_components
    
    def create_dashboard_header(self):
        """
        Create dashboard header with title and metrics
        """
        return {
            'type': 'header',
            'components': [
                {
                    'type': 'title',
                    'text': 'Customer Feedback Analysis Dashboard',
                    'style': {'text-align': 'center', 'color': '#1f4e79'}
                },
                {
                    'type': 'subtitle',
                    'text': 'Personal Paraguay Fiber Comments Analysis',
                    'style': {'text-align': 'center', 'color': '#5b9bd5'}
                }
            ]
        }
    
    def create_dashboard_sidebar(self, analysis_results):
        """
        Create interactive sidebar with filters
        """
        return {
            'type': 'sidebar',
            'components': [
                {
                    'type': 'selectbox',
                    'label': 'Select Language',
                    'options': self.get_available_languages(analysis_results),
                    'default': 'All'
                },
                {
                    'type': 'selectbox',
                    'label': 'Select Sentiment',
                    'options': ['All', 'Positive', 'Neutral', 'Negative'],
                    'default': 'All'
                },
                {
                    'type': 'multiselect',
                    'label': 'Select Themes',
                    'options': self.get_available_themes(analysis_results),
                    'default': []
                },
                {
                    'type': 'date_range',
                    'label': 'Date Range',
                    'default_start': self.get_min_date(analysis_results),
                    'default_end': self.get_max_date(analysis_results)
                }
            ]
        }
```

## 🎨 Styling and Themes

### Visualization Style Manager
```python
class VisualizationStyleManager:
    """
    Manage visualization styling and themes
    """
    
    def __init__(self):
        self.themes = {
            'corporate': self.get_corporate_theme(),
            'modern': self.get_modern_theme(),
            'academic': self.get_academic_theme(),
            'colorful': self.get_colorful_theme()
        }
        
    def get_corporate_theme(self):
        """
        Corporate theme with professional colors
        """
        return {
            'colors': {
                'primary': '#1F4E79',
                'secondary': '#5B9BD5',
                'accent': '#70AD47',
                'background': '#FFFFFF',
                'text': '#2F2F2F',
                'grid': '#E8E8E8'
            },
            'fonts': {
                'family': 'Arial, sans-serif',
                'title_size': 18,
                'axis_size': 12,
                'legend_size': 10
            },
            'layout': {
                'margin': {'t': 60, 'b': 40, 'l': 60, 'r': 40},
                'showgrid': True,
                'gridcolor': '#E8E8E8',
                'zeroline': False
            }
        }
    
    def apply_theme(self, figure, theme_name='corporate'):
        """
        Apply theme to Plotly figure
        """
        theme = self.themes.get(theme_name, self.themes['corporate'])
        
        # Update layout with theme
        figure.update_layout(
            font={'family': theme['fonts']['family']},
            plot_bgcolor=theme['colors']['background'],
            paper_bgcolor=theme['colors']['background'],
            margin=theme['layout']['margin']
        )
        
        # Update axes
        figure.update_xaxes(
            gridcolor=theme['colors']['grid'],
            showgrid=theme['layout']['showgrid'],
            zeroline=theme['layout']['zeroline']
        )
        
        figure.update_yaxes(
            gridcolor=theme['colors']['grid'],
            showgrid=theme['layout']['showgrid'],
            zeroline=theme['layout']['zeroline']
        )
        
        return figure
```

## 🔧 Configuration

### Visualization Settings
```python
VISUALIZATION_CONFIG = {
    'default_library': 'plotly',
    'theme': 'corporate',
    'chart_types': {
        'sentiment': ['pie', 'bar', 'timeline', 'heatmap'],
        'themes': ['bar', 'network', 'wordcloud', 'treemap'],
        'emotions': ['radar', 'bar', 'scatter', 'timeline'],
        'temporal': ['line', 'heatmap', 'calendar', 'bar']
    },
    'interactivity': {
        'hover_info': True,
        'zoom_pan': True,
        'selection': True,
        'crossfilter': True
    },
    'export_options': {
        'formats': ['png', 'svg', 'pdf', 'html'],
        'resolution': 300,  # DPI for raster formats
        'width': 1200,
        'height': 800
    },
    'performance': {
        'max_data_points': 10000,
        'enable_webgl': True,
        'cache_charts': True
    },
    'accessibility': {
        'color_blind_friendly': True,
        'high_contrast_mode': False,
        'screen_reader_support': True
    }
}
```

## 🔗 Related Documentation
- [Excel Export](excel-export.md) - Excel chart integration
- [Report Generation](report-generation.md) - Report visualization
- [Analysis Engines](../analysis-engines/sentiment-analysis.md) - Data sources
- [Frontend Components](../../frontend/components/analysis-dashboard.md) - Dashboard implementation