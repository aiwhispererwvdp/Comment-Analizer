# File Upload Service Documentation

The File Upload Service manages the complete lifecycle of data ingestion, from file upload and validation to preprocessing and storage for the Personal Paraguay Fiber Comments Analysis System.

## 🎯 Overview

This service provides robust file handling capabilities with support for multiple formats, intelligent validation, automatic preprocessing, and efficient storage management.

### Core Responsibilities
- **Multi-format Support** - Excel, CSV, JSON, TXT file handling
- **Data Validation** - Structure and content validation
- **Preprocessing** - Data cleaning and standardization
- **Column Detection** - Automatic identification of comment columns
- **Error Recovery** - Graceful handling of malformed data

## 🏗️ Service Architecture

### File Upload Pipeline
```python
class FileUploadService:
    """
    Comprehensive file upload and processing service
    """
    
    def __init__(self):
        self.file_validator = FileValidator()
        self.data_processor = DataProcessor()
        self.column_detector = ColumnDetector()
        self.storage_manager = StorageManager()
        self.session_manager = SessionManager()
    
    async def process_upload(self, file_data, user_session):
        """
        Complete file upload processing pipeline
        """
        # Step 1: Initial validation
        validation_result = await self.validate_file(file_data)
        
        # Step 2: Parse file content
        parsed_data = await self.parse_file(file_data)
        
        # Step 3: Detect columns
        column_mapping = await self.detect_columns(parsed_data)
        
        # Step 4: Process and clean data
        processed_data = await self.process_data(parsed_data, column_mapping)
        
        # Step 5: Store processed data
        storage_result = await self.store_data(processed_data, user_session)
        
        return {
            'status': 'success',
            'data': processed_data,
            'statistics': self.calculate_statistics(processed_data),
            'storage_id': storage_result['id']
        }
```

## 📁 File Format Handlers

### Excel Handler
```python
class ExcelHandler:
    """
    Handle Excel file uploads (.xlsx, .xls)
    """
    
    def __init__(self):
        self.max_file_size = 200 * 1024 * 1024  # 200MB
        self.supported_extensions = ['.xlsx', '.xls']
    
    async def read_excel_file(self, file_content):
        """
        Read and parse Excel file
        """
        try:
            # Read Excel file
            excel_file = pd.ExcelFile(io.BytesIO(file_content))
            
            # Handle multiple sheets
            sheets_data = {}
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(
                    excel_file, 
                    sheet_name=sheet_name,
                    engine='openpyxl'
                )
                
                # Clean and validate sheet data
                cleaned_df = self.clean_dataframe(df)
                
                if not cleaned_df.empty:
                    sheets_data[sheet_name] = cleaned_df
            
            return {
                'format': 'excel',
                'sheets': sheets_data,
                'primary_sheet': self.select_primary_sheet(sheets_data)
            }
            
        except Exception as e:
            raise FileProcessingError(f"Failed to read Excel file: {str(e)}")
    
    def clean_dataframe(self, df):
        """
        Clean and standardize dataframe
        """
        # Remove empty rows and columns
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')
        
        # Remove duplicate rows
        df = df.drop_duplicates()
        
        # Strip whitespace from string columns
        string_columns = df.select_dtypes(include=['object']).columns
        df[string_columns] = df[string_columns].apply(lambda x: x.str.strip())
        
        return df
```

### CSV Handler
```python
class CSVHandler:
    """
    Handle CSV file uploads
    """
    
    def __init__(self):
        self.encoding_detection = True
        self.delimiter_detection = True
        self.supported_encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    async def read_csv_file(self, file_content):
        """
        Read CSV with automatic encoding and delimiter detection
        """
        # Detect encoding
        encoding = self.detect_encoding(file_content)
        
        # Detect delimiter
        delimiter = self.detect_delimiter(file_content, encoding)
        
        try:
            # Read CSV
            df = pd.read_csv(
                io.BytesIO(file_content),
                encoding=encoding,
                delimiter=delimiter,
                error_bad_lines=False,
                warn_bad_lines=True
            )
            
            return {
                'format': 'csv',
                'data': df,
                'encoding': encoding,
                'delimiter': delimiter
            }
            
        except Exception as e:
            # Try alternative parsing methods
            return self.fallback_csv_parsing(file_content)
    
    def detect_encoding(self, file_content):
        """
        Detect file encoding
        """
        import chardet
        
        # Sample first 10KB for detection
        sample = file_content[:10240]
        detection = chardet.detect(sample)
        
        confidence = detection.get('confidence', 0)
        encoding = detection.get('encoding', 'utf-8')
        
        # Fallback to utf-8 if confidence is low
        if confidence < 0.7:
            encoding = 'utf-8'
        
        return encoding
    
    def detect_delimiter(self, file_content, encoding):
        """
        Detect CSV delimiter
        """
        sample = file_content[:1024].decode(encoding, errors='ignore')
        
        # Count potential delimiters
        delimiters = {',': 0, ';': 0, '\t': 0, '|': 0}
        
        for delimiter in delimiters:
            delimiters[delimiter] = sample.count(delimiter)
        
        # Return most frequent delimiter
        return max(delimiters, key=delimiters.get)
```

### JSON Handler
```python
class JSONHandler:
    """
    Handle JSON file uploads
    """
    
    async def read_json_file(self, file_content):
        """
        Read and parse JSON file
        """
        try:
            # Parse JSON
            data = json.loads(file_content.decode('utf-8'))
            
            # Convert to DataFrame based on structure
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try to find the main data array
                df = self.extract_dataframe_from_dict(data)
            else:
                raise ValueError("Unsupported JSON structure")
            
            return {
                'format': 'json',
                'data': df,
                'original_structure': type(data).__name__
            }
            
        except json.JSONDecodeError as e:
            raise FileProcessingError(f"Invalid JSON file: {str(e)}")
    
    def extract_dataframe_from_dict(self, data):
        """
        Extract DataFrame from nested JSON structure
        """
        # Look for common data keys
        data_keys = ['data', 'comments', 'records', 'items', 'results']
        
        for key in data_keys:
            if key in data and isinstance(data[key], list):
                return pd.DataFrame(data[key])
        
        # Try to create DataFrame from dict
        return pd.DataFrame([data])
```

## 🔍 Column Detection

### Intelligent Column Detection
```python
class ColumnDetector:
    """
    Automatically detect relevant columns in uploaded data
    """
    
    def __init__(self):
        self.comment_keywords = [
            'comment', 'feedback', 'review', 'opinion', 
            'comentario', 'observacion', 'mensaje', 'texto'
        ]
        self.date_keywords = [
            'date', 'time', 'timestamp', 'fecha', 'created', 'posted'
        ]
    
    def detect_comment_column(self, df):
        """
        Identify column containing comments
        """
        potential_columns = []
        
        for col in df.columns:
            col_lower = str(col).lower()
            
            # Check column name
            if any(keyword in col_lower for keyword in self.comment_keywords):
                potential_columns.append((col, 1.0))  # High confidence
                continue
            
            # Check column content
            if df[col].dtype == 'object':
                # Sample content analysis
                sample = df[col].dropna().head(100)
                avg_length = sample.str.len().mean()
                
                # Likely comment column if average length > 50
                if avg_length > 50:
                    potential_columns.append((col, 0.7))
        
        # Return column with highest confidence
        if potential_columns:
            return max(potential_columns, key=lambda x: x[1])[0]
        
        return None
    
    def detect_date_column(self, df):
        """
        Identify date/timestamp column
        """
        for col in df.columns:
            col_lower = str(col).lower()
            
            # Check column name
            if any(keyword in col_lower for keyword in self.date_keywords):
                # Try to parse as datetime
                try:
                    pd.to_datetime(df[col])
                    return col
                except:
                    continue
            
            # Check if column contains dates
            if df[col].dtype == 'object':
                try:
                    # Sample parsing
                    sample = df[col].dropna().head(10)
                    pd.to_datetime(sample)
                    return col
                except:
                    continue
        
        return None
```

## ✅ Data Validation

### Comprehensive Validation
```python
class DataValidator:
    """
    Validate uploaded data quality and structure
    """
    
    def __init__(self):
        self.min_comment_length = 10
        self.max_comment_length = 5000
        self.min_valid_rows = 1
        
    def validate_data(self, df, column_mapping):
        """
        Comprehensive data validation
        """
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }
        
        # Check if we have comment column
        if not column_mapping.get('comment_column'):
            validation_results['is_valid'] = False
            validation_results['errors'].append("No comment column detected")
            return validation_results
        
        comment_col = column_mapping['comment_column']
        
        # Validate comment data
        comments = df[comment_col].dropna()
        
        # Check minimum rows
        if len(comments) < self.min_valid_rows:
            validation_results['is_valid'] = False
            validation_results['errors'].append(f"Too few valid comments: {len(comments)}")
        
        # Check comment lengths
        short_comments = comments[comments.str.len() < self.min_comment_length]
        if len(short_comments) > 0:
            validation_results['warnings'].append(
                f"{len(short_comments)} comments shorter than {self.min_comment_length} characters"
            )
        
        # Calculate statistics
        validation_results['statistics'] = {
            'total_rows': len(df),
            'valid_comments': len(comments),
            'empty_comments': len(df) - len(comments),
            'avg_comment_length': comments.str.len().mean(),
            'languages_detected': self.detect_languages_summary(comments)
        }
        
        return validation_results
    
    def detect_languages_summary(self, comments):
        """
        Quick language detection summary
        """
        sample_size = min(100, len(comments))
        sample = comments.sample(sample_size) if len(comments) > sample_size else comments
        
        languages = {'spanish': 0, 'guarani': 0, 'mixed': 0, 'other': 0}
        
        for comment in sample:
            # Simple language detection logic
            if self.contains_guarani(comment):
                if self.contains_spanish(comment):
                    languages['mixed'] += 1
                else:
                    languages['guarani'] += 1
            elif self.contains_spanish(comment):
                languages['spanish'] += 1
            else:
                languages['other'] += 1
        
        # Convert to percentages
        total = sum(languages.values())
        return {k: (v/total)*100 for k, v in languages.items() if v > 0}
```

## 🔄 Data Processing

### Data Preprocessing Pipeline
```python
class DataPreprocessor:
    """
    Preprocess data for analysis
    """
    
    def preprocess_comments(self, df, comment_column):
        """
        Clean and prepare comments for analysis
        """
        # Create a copy
        processed_df = df.copy()
        
        # Clean comments
        processed_df['processed_comment'] = df[comment_column].apply(
            self.clean_comment
        )
        
        # Remove duplicates
        processed_df = self.remove_duplicates(processed_df)
        
        # Add metadata
        processed_df = self.add_metadata(processed_df)
        
        # Filter invalid comments
        processed_df = self.filter_invalid_comments(processed_df)
        
        return processed_df
    
    def clean_comment(self, comment):
        """
        Clean individual comment
        """
        if pd.isna(comment):
            return None
        
        # Convert to string
        comment = str(comment)
        
        # Remove excessive whitespace
        comment = ' '.join(comment.split())
        
        # Remove special characters but keep Spanish/Guaraní chars
        comment = re.sub(r'[^\w\s\ñÑáéíóúÁÉÍÓÚãẽĩõũỹÃẼĨÕŨỸ.,!?-]', '', comment)
        
        # Remove URLs
        comment = re.sub(r'http[s]?://\S+', '', comment)
        
        # Remove email addresses
        comment = re.sub(r'\S+@\S+', '', comment)
        
        return comment.strip()
    
    def remove_duplicates(self, df):
        """
        Intelligent duplicate removal
        """
        # Exact duplicates
        df = df.drop_duplicates(subset=['processed_comment'])
        
        # Near duplicates (using similarity)
        df = self.remove_near_duplicates(df, threshold=0.95)
        
        return df
```

## 💾 Storage Management

### File Storage Service
```python
class FileStorageManager:
    """
    Manage uploaded file storage
    """
    
    def __init__(self):
        self.storage_path = Path('data/uploads')
        self.processed_path = Path('data/processed')
        self.max_storage_gb = 10
        
    async def store_uploaded_file(self, file_content, filename, user_session):
        """
        Store uploaded file securely
        """
        # Generate unique filename
        file_id = self.generate_file_id()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Sanitize filename
        safe_filename = self.sanitize_filename(filename)
        
        # Create storage path
        storage_filename = f"{user_session}_{timestamp}_{file_id}_{safe_filename}"
        file_path = self.storage_path / storage_filename
        
        # Ensure directory exists
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Store file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Store metadata
        metadata = {
            'file_id': file_id,
            'original_name': filename,
            'storage_path': str(file_path),
            'size_bytes': len(file_content),
            'upload_time': datetime.now(),
            'user_session': user_session
        }
        
        await self.store_metadata(metadata)
        
        return metadata
    
    def cleanup_old_files(self, days_to_keep=7):
        """
        Clean up old uploaded files
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for file_path in self.storage_path.glob('*'):
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    file_path.unlink()
```

## 🔐 Security

### File Security Validation
```python
class FileSecurityValidator:
    """
    Security validation for uploaded files
    """
    
    def __init__(self):
        self.max_file_size = 200 * 1024 * 1024  # 200MB
        self.allowed_extensions = ['.xlsx', '.xls', '.csv', '.json', '.txt']
        self.blocked_content = ['<script', 'javascript:', 'onclick']
    
    def validate_file_security(self, file_content, filename):
        """
        Comprehensive security validation
        """
        # Check file size
        if len(file_content) > self.max_file_size:
            raise SecurityError(f"File too large: {len(file_content)} bytes")
        
        # Check extension
        ext = Path(filename).suffix.lower()
        if ext not in self.allowed_extensions:
            raise SecurityError(f"File type not allowed: {ext}")
        
        # Check for malicious content
        content_sample = file_content[:10240].decode('utf-8', errors='ignore')
        for blocked in self.blocked_content:
            if blocked in content_sample.lower():
                raise SecurityError("Potentially malicious content detected")
        
        # Validate file structure
        if not self.validate_file_structure(file_content, ext):
            raise SecurityError("Invalid file structure")
        
        return True
    
    def sanitize_content(self, content):
        """
        Sanitize content for safety
        """
        # Remove any potential script tags
        content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
        
        # Remove event handlers
        content = re.sub(r'on\w+\s*=\s*["\'].*?["\']', '', content)
        
        return content
```

## 📊 Statistics and Reporting

### Upload Statistics
```python
class UploadStatistics:
    """
    Track and report upload statistics
    """
    
    def generate_upload_report(self, processed_data):
        """
        Generate comprehensive upload statistics
        """
        return {
            'file_info': {
                'format': processed_data['format'],
                'size_mb': processed_data['size_bytes'] / (1024*1024),
                'upload_time': processed_data['upload_time']
            },
            'data_statistics': {
                'total_rows': len(processed_data['data']),
                'valid_comments': processed_data['valid_comments'],
                'invalid_comments': processed_data['invalid_comments'],
                'duplicate_removed': processed_data['duplicates_removed']
            },
            'quality_metrics': {
                'avg_comment_length': processed_data['avg_length'],
                'language_distribution': processed_data['languages'],
                'data_completeness': processed_data['completeness']
            },
            'processing_info': {
                'processing_time_seconds': processed_data['processing_time'],
                'columns_detected': processed_data['column_mapping'],
                'warnings': processed_data.get('warnings', [])
            }
        }
```

## 🔗 Related Documentation
- [Session Management](session-management.md) - User session handling
- [Data Processing](../../business-logic/data-processing/comment-reader.md) - Data processing logic
- [File Upload UI](../../frontend/components/file-upload.md) - Frontend component
- [Security](../infrastructure/security.md) - Security implementation