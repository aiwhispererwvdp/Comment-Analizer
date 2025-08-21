# File Upload Component Documentation

The file upload system handles data ingestion for the Personal Paraguay Fiber Comments Analysis System, supporting multiple file formats and providing real-time validation.

## 📁 Component Files

- **`file_upload_ui.py`** - Standard file upload interface
- **`optimized_file_upload_ui.py`** - Performance-optimized version
- **`responsive_file_upload_ui.py`** - Mobile-responsive version

## 🔧 Core Functionality

### Supported File Formats
- **Excel (.xlsx)** - Primary format for customer comments
- **CSV (.csv)** - Comma-separated values with encoding detection
- **JSON (.json)** - Structured data format
- **Text (.txt)** - Plain text, one comment per line

### Upload Process
1. **File Selection** - Drag-and-drop or file browser
2. **Format Detection** - Automatic file type identification
3. **Validation** - Structure and content validation
4. **Preview** - Data preview with statistics
5. **Processing** - Data cleaning and preparation

## 🎯 Key Features

### Smart Column Detection
```python
def detect_comment_columns(df):
    """
    Automatically identifies comment columns in uploaded data
    
    Logic:
    - Looks for columns with text data
    - Prioritizes columns with 'comment', 'feedback', 'review' keywords
    - Validates data quality and completeness
    """
```

### Data Validation
- **Format Validation** - Ensures file format compatibility
- **Structure Validation** - Checks for required columns
- **Content Validation** - Validates comment data quality
- **Encoding Detection** - Handles various text encodings

### Progress Indicators
- Upload progress bar
- Validation status indicators
- Processing step indicators
- Error and warning messages

## 📊 Data Processing Pipeline

### 1. File Upload Handler
```python
def handle_file_upload():
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['xlsx', 'csv', 'json', 'txt'],
        help="Upload customer comments data"
    )
```

### 2. Data Reader
```python
def read_uploaded_file(uploaded_file):
    """
    Reads and processes uploaded files based on format
    
    Returns:
        pandas.DataFrame: Processed comment data
    """
```

### 3. Data Cleaning
- Remove empty rows and columns
- Standardize text encoding
- Handle special characters
- Detect and process language variants

## 🎨 User Interface Elements

### Upload Area
- Drag-and-drop zone with visual feedback
- File browser button as fallback
- Format restrictions display
- Upload progress visualization

### Data Preview
- Tabular data preview (first 100 rows)
- Column information and statistics
- Data quality indicators
- Sample data visualization

### Validation Messages
- Success indicators for valid uploads
- Warning messages for data issues
- Error messages with specific guidance
- Help text and documentation links

## 📱 Responsive Features

### Mobile Optimization
- Touch-friendly upload controls
- Simplified interface for small screens
- Optimized file browser integration
- Reduced data preview for performance

### Desktop Enhancements
- Drag-and-drop functionality
- Keyboard shortcuts
- Multiple file selection
- Advanced preview options

## ⚙️ Configuration Options

### Upload Settings
```python
MAX_FILE_SIZE = 200  # MB
SUPPORTED_ENCODINGS = ['utf-8', 'latin-1', 'cp1252']
CHUNK_SIZE = 10000  # rows for large files
```

### Validation Rules
- Minimum comment length requirements
- Maximum file size limits
- Column name patterns
- Data quality thresholds

## 🔍 Error Handling

### Common Error Scenarios
1. **Unsupported File Format**
   - Clear error message with supported formats
   - Suggestions for file conversion

2. **Corrupted or Empty Files**
   - Validation error with specific issue
   - Guidance for file preparation

3. **Encoding Issues**
   - Automatic encoding detection
   - Manual encoding selection option

4. **Large File Handling**
   - Progress indicators for large uploads
   - Memory-efficient processing
   - Chunked processing options

## 📈 Performance Considerations

### Optimization Strategies
- **Streaming Upload** - Process files as they upload
- **Lazy Loading** - Load data in chunks for large files
- **Caching** - Cache processed data for re-use
- **Compression** - Compress data in memory

### Memory Management
```python
def process_large_file(file_path, chunk_size=10000):
    """
    Process large files in chunks to manage memory usage
    """
    for chunk in pd.read_excel(file_path, chunksize=chunk_size):
        yield process_chunk(chunk)
```

## 🧪 Testing Scenarios

### Test Data Formats
1. **Standard Excel** - Typical customer feedback file
2. **CSV with Encoding Issues** - Non-UTF8 encodings
3. **Large Files** - Performance and memory testing
4. **Malformed Data** - Error handling validation

### Validation Tests
- Upload various file formats
- Test with empty/corrupted files
- Validate large file processing
- Test responsive interface on mobile

## 🔮 Future Enhancements

### Planned Features
- **Cloud Storage Integration** - Direct upload from cloud services
- **Real-time Validation** - Live validation during upload
- **Batch Upload** - Multiple file upload support
- **Data Mapping** - Custom column mapping interface

### Technical Improvements
- **Progressive Upload** - Resume interrupted uploads
- **Client-side Processing** - Browser-based file processing
- **Advanced Preview** - Interactive data exploration
- **Auto-correction** - Automatic data cleaning suggestions

## 🔗 Related Components

- **[Analysis Dashboard](analysis-dashboard.md)** - Processes uploaded data
- **[Results Display](results-display.md)** - Shows analysis results
- **[Data Processing](../../business-logic/data-processing/)** - Backend data handling