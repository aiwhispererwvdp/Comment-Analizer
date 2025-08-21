# Comment Reader Documentation

The Comment Reader module provides intelligent reading and parsing of customer comments from various file formats, ensuring accurate data extraction and preprocessing for analysis.

## 🎯 Overview

The Comment Reader handles the critical first step in the analysis pipeline - extracting and normalizing customer feedback from different sources while maintaining data integrity and handling various formats and encodings.

### Core Capabilities
- **Multi-Format Support** - Excel, CSV, JSON, TXT files
- **Intelligent Parsing** - Auto-detect structure and delimiters
- **Encoding Detection** - Handle various character encodings
- **Data Validation** - Ensure comment quality and completeness
- **Error Recovery** - Graceful handling of malformed data

## 🏗️ Reader Architecture

### File Processing Pipeline
```python
class CommentReaderArchitecture:
    """
    Comment reading and processing pipeline
    """
    
    SUPPORTED_FORMATS = {
        'excel': ['.xlsx', '.xls', '.xlsm'],
        'csv': ['.csv', '.tsv'],
        'json': ['.json', '.jsonl'],
        'text': ['.txt', '.text']
    }
    
    PROCESSING_STAGES = [
        'format_detection',
        'encoding_detection',
        'structure_analysis',
        'data_extraction',
        'validation',
        'normalization'
    ]
```

## 📖 Core Reader Implementation

### Universal Comment Reader
```python
class CommentReader:
    """
    Universal reader for all comment file formats
    """
    
    def __init__(self):
        self.format_detector = FormatDetector()
        self.encoding_detector = EncodingDetector()
        self.parsers = {
            'excel': ExcelParser(),
            'csv': CSVParser(),
            'json': JSONParser(),
            'text': TextParser()
        }
        self.validator = CommentValidator()
    
    async def read_comments(self, file_path, options=None):
        """
        Read comments from file with automatic format detection
        """
        # Detect file format
        file_format = self.format_detector.detect(file_path)
        
        if not file_format:
            raise UnsupportedFormatError(f"Cannot determine format of {file_path}")
        
        # Detect encoding
        encoding = self.encoding_detector.detect(file_path)
        
        # Select appropriate parser
        parser = self.parsers.get(file_format)
        if not parser:
            raise ParserNotFoundError(f"No parser for format: {file_format}")
        
        # Parse file
        raw_data = await parser.parse(file_path, encoding, options)
        
        # Extract comments
        comments = self.extract_comments(raw_data, file_format)
        
        # Validate and normalize
        validated_comments = self.validator.validate_batch(comments)
        
        return {
            'comments': validated_comments,
            'metadata': {
                'source_file': file_path,
                'format': file_format,
                'encoding': encoding,
                'total_rows': len(raw_data),
                'valid_comments': len(validated_comments),
                'parse_errors': self.get_parse_errors()
            }
        }
```

## 📊 Excel Reader

### Advanced Excel Parser
```python
class ExcelParser:
    """
    Sophisticated Excel file parser with multi-sheet support
    """
    
    def __init__(self):
        self.column_detector = ColumnDetector()
        self.date_parser = DateParser()
        self.formula_evaluator = FormulaEvaluator()
    
    async def parse(self, file_path, encoding='utf-8', options=None):
        """
        Parse Excel file with intelligent column detection
        """
        try:
            # Load workbook
            workbook = openpyxl.load_workbook(
                file_path,
                read_only=True,
                data_only=True  # Get values not formulas
            )
            
            all_comments = []
            
            # Process each sheet
            for sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                
                # Skip empty sheets
                if sheet.max_row == 0:
                    continue
                
                # Detect comment columns
                comment_columns = self.column_detector.find_comment_columns(sheet)
                
                if not comment_columns:
                    logger.warning(f"No comment columns found in sheet: {sheet_name}")
                    continue
                
                # Extract comments from detected columns
                sheet_comments = self.extract_sheet_comments(
                    sheet,
                    comment_columns,
                    options
                )
                
                # Add sheet metadata
                for comment in sheet_comments:
                    comment['sheet'] = sheet_name
                
                all_comments.extend(sheet_comments)
            
            workbook.close()
            return all_comments
            
        except Exception as e:
            raise ExcelParseError(f"Failed to parse Excel file: {e}")
    
    def extract_sheet_comments(self, sheet, comment_columns, options):
        """
        Extract comments from specific columns in sheet
        """
        comments = []
        
        # Determine header row
        header_row = options.get('header_row', 1) if options else 1
        
        # Extract headers
        headers = {}
        for col_idx in range(1, sheet.max_column + 1):
            cell = sheet.cell(row=header_row, column=col_idx)
            if cell.value:
                headers[col_idx] = str(cell.value).strip()
        
        # Process data rows
        for row_idx in range(header_row + 1, sheet.max_row + 1):
            row_data = {}
            
            # Extract all column values
            for col_idx, col_name in headers.items():
                cell = sheet.cell(row=row_idx, column=col_idx)
                value = self.process_cell_value(cell)
                if value:
                    row_data[col_name] = value
            
            # Extract comments from identified columns
            for col_idx in comment_columns:
                if col_idx in headers:
                    comment_text = row_data.get(headers[col_idx])
                    if comment_text and self.is_valid_comment(comment_text):
                        comments.append({
                            'text': comment_text,
                            'row': row_idx,
                            'column': headers[col_idx],
                            'metadata': self.extract_row_metadata(row_data)
                        })
        
        return comments
```

## 📄 CSV Reader

### Intelligent CSV Parser
```python
class CSVParser:
    """
    CSV parser with delimiter detection and encoding handling
    """
    
    def __init__(self):
        self.delimiter_detector = DelimiterDetector()
        self.quote_char_detector = QuoteCharDetector()
        self.encoding_fixer = EncodingFixer()
    
    async def parse(self, file_path, encoding='utf-8', options=None):
        """
        Parse CSV file with automatic delimiter detection
        """
        # Detect delimiter
        delimiter = await self.delimiter_detector.detect(file_path)
        
        # Detect quote character
        quote_char = await self.quote_char_detector.detect(file_path)
        
        comments = []
        
        try:
            with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                # Create CSV reader with detected parameters
                reader = csv.DictReader(
                    file,
                    delimiter=delimiter,
                    quotechar=quote_char,
                    skipinitialspace=True
                )
                
                # Process each row
                for row_num, row in enumerate(reader, start=2):
                    # Find comment fields
                    comment_fields = self.identify_comment_fields(row)
                    
                    for field_name in comment_fields:
                        comment_text = row.get(field_name, '').strip()
                        
                        if comment_text:
                            # Fix encoding issues if present
                            comment_text = self.encoding_fixer.fix(comment_text)
                            
                            comments.append({
                                'text': comment_text,
                                'row': row_num,
                                'field': field_name,
                                'metadata': self.extract_metadata(row)
                            })
        
        except Exception as e:
            raise CSVParseError(f"Failed to parse CSV file: {e}")
        
        return comments
    
    def identify_comment_fields(self, row):
        """
        Identify fields containing comments
        """
        comment_keywords = [
            'comment', 'feedback', 'review', 'opinion',
            'comentario', 'respuesta', 'observacion'
        ]
        
        comment_fields = []
        
        for field_name in row.keys():
            if field_name:
                # Check if field name suggests comments
                field_lower = field_name.lower()
                if any(keyword in field_lower for keyword in comment_keywords):
                    comment_fields.append(field_name)
                
                # Check field content characteristics
                elif self.looks_like_comment(row.get(field_name, '')):
                    comment_fields.append(field_name)
        
        return comment_fields
```

## 🔤 Encoding Detection

### Multi-Method Encoding Detector
```python
class EncodingDetector:
    """
    Detect file encoding using multiple methods
    """
    
    def __init__(self):
        self.common_encodings = [
            'utf-8', 'utf-16', 'latin-1', 'iso-8859-1',
            'windows-1252', 'cp1252', 'ascii'
        ]
    
    def detect(self, file_path):
        """
        Detect file encoding with high accuracy
        """
        # Method 1: Use chardet library
        encoding = self.detect_with_chardet(file_path)
        if encoding and self.validate_encoding(file_path, encoding):
            return encoding
        
        # Method 2: Try common encodings
        for enc in self.common_encodings:
            if self.validate_encoding(file_path, enc):
                return enc
        
        # Method 3: Use file BOM
        bom_encoding = self.detect_bom(file_path)
        if bom_encoding:
            return bom_encoding
        
        # Default fallback
        return 'utf-8'
    
    def detect_with_chardet(self, file_path):
        """
        Use chardet library for encoding detection
        """
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                
                if result['confidence'] > 0.7:
                    return result['encoding']
        except Exception:
            pass
        
        return None
    
    def validate_encoding(self, file_path, encoding):
        """
        Validate if file can be read with encoding
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                file.read(1000)  # Try reading first 1000 chars
            return True
        except (UnicodeDecodeError, LookupError):
            return False
```

## ✅ Comment Validation

### Comprehensive Comment Validator
```python
class CommentValidator:
    """
    Validate and clean comments
    """
    
    def __init__(self):
        self.min_length = 10
        self.max_length = 10000
        self.language_detector = LanguageDetector()
        self.spam_detector = SpamDetector()
    
    def validate_batch(self, comments):
        """
        Validate batch of comments
        """
        validated = []
        
        for comment in comments:
            validation_result = self.validate_single(comment)
            
            if validation_result['is_valid']:
                # Add validation metadata
                comment['validation'] = validation_result
                validated.append(comment)
            else:
                # Log invalid comment
                logger.debug(f"Invalid comment: {validation_result['reason']}")
        
        return validated
    
    def validate_single(self, comment):
        """
        Validate individual comment
        """
        text = comment.get('text', '')
        
        # Check if empty
        if not text or not text.strip():
            return {'is_valid': False, 'reason': 'empty'}
        
        # Check length
        if len(text) < self.min_length:
            return {'is_valid': False, 'reason': 'too_short'}
        
        if len(text) > self.max_length:
            return {'is_valid': False, 'reason': 'too_long'}
        
        # Check for spam
        if self.spam_detector.is_spam(text):
            return {'is_valid': False, 'reason': 'spam'}
        
        # Check for repetitive content
        if self.is_repetitive(text):
            return {'is_valid': False, 'reason': 'repetitive'}
        
        # Detect language
        language = self.language_detector.detect(text)
        
        return {
            'is_valid': True,
            'language': language,
            'quality_score': self.calculate_quality_score(text)
        }
    
    def is_repetitive(self, text):
        """
        Check if comment is repetitive
        """
        # Check for repeated characters
        if re.search(r'(.)\1{10,}', text):
            return True
        
        # Check for repeated words
        words = text.split()
        if len(words) > 3:
            unique_words = len(set(words))
            if unique_words / len(words) < 0.3:
                return True
        
        return False
```

## 🔄 Data Normalization

### Comment Normalizer
```python
class CommentNormalizer:
    """
    Normalize comments for consistent processing
    """
    
    def __init__(self):
        self.text_cleaner = TextCleaner()
        self.emoji_handler = EmojiHandler()
        self.accent_normalizer = AccentNormalizer()
    
    def normalize(self, comment):
        """
        Apply normalization pipeline
        """
        text = comment['text']
        
        # Clean whitespace
        text = self.text_cleaner.clean_whitespace(text)
        
        # Handle special characters
        text = self.handle_special_chars(text)
        
        # Process emojis
        emoji_info = self.emoji_handler.process(text)
        text = emoji_info['cleaned_text']
        comment['emojis'] = emoji_info['emojis']
        
        # Normalize accents for search
        comment['normalized_text'] = self.accent_normalizer.normalize(text)
        
        # Keep original for display
        comment['original_text'] = comment['text']
        comment['text'] = text
        
        return comment
    
    def handle_special_chars(self, text):
        """
        Handle special characters and formatting
        """
        # Fix common encoding issues
        replacements = {
            'â€™': "'",
            'â€œ': '"',
            'â€': '"',
            'â€¦': '...',
            'â€"': '-',
            'â€"': '-'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Remove control characters
        text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
        
        return text
```

## 🔍 Structure Detection

### Automatic Structure Detector
```python
class StructureDetector:
    """
    Detect data structure in files
    """
    
    def detect_structure(self, file_path, sample_size=100):
        """
        Analyze file structure
        """
        structure = {
            'has_headers': False,
            'delimiter': None,
            'comment_columns': [],
            'metadata_columns': [],
            'date_columns': [],
            'id_columns': []
        }
        
        # Read sample
        sample = self.read_sample(file_path, sample_size)
        
        # Detect headers
        structure['has_headers'] = self.detect_headers(sample)
        
        # Identify column types
        if structure['has_headers']:
            headers = sample[0]
            structure['comment_columns'] = self.find_comment_columns(headers)
            structure['metadata_columns'] = self.find_metadata_columns(headers)
            structure['date_columns'] = self.find_date_columns(headers, sample)
            structure['id_columns'] = self.find_id_columns(headers, sample)
        
        return structure
```

## 📊 Batch Processing

### Efficient Batch Reader
```python
class BatchCommentReader:
    """
    Read large files in batches for memory efficiency
    """
    
    def __init__(self, batch_size=1000):
        self.batch_size = batch_size
        self.reader = CommentReader()
    
    async def read_in_batches(self, file_path, process_func):
        """
        Read and process file in batches
        """
        file_format = self.detect_format(file_path)
        
        if file_format == 'excel':
            async for batch in self.read_excel_batches(file_path):
                await process_func(batch)
        
        elif file_format == 'csv':
            async for batch in self.read_csv_batches(file_path):
                await process_func(batch)
    
    async def read_csv_batches(self, file_path):
        """
        Read CSV file in batches
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            batch = []
            
            for row in reader:
                batch.append(row)
                
                if len(batch) >= self.batch_size:
                    yield batch
                    batch = []
            
            if batch:
                yield batch
```

## 🔧 Configuration

### Reader Configuration
```python
READER_CONFIG = {
    'supported_formats': {
        'excel': ['.xlsx', '.xls'],
        'csv': ['.csv', '.tsv'],
        'json': ['.json'],
        'text': ['.txt']
    },
    'validation': {
        'min_comment_length': 10,
        'max_comment_length': 10000,
        'required_confidence': 0.7
    },
    'encoding': {
        'default': 'utf-8',
        'fallback': 'latin-1',
        'detect_bom': True
    },
    'parsing': {
        'max_file_size_mb': 100,
        'batch_size': 1000,
        'parallel_processing': True
    }
}
```

## 🔗 Related Documentation
- [Language Detector](language-detector.md) - Language detection
- [Duplicate Cleaner](duplicate-cleaner.md) - Duplicate removal
- [Sentiment Analysis](../analysis-engines/sentiment-analysis.md) - Analysis pipeline
- [File Upload Service](../../backend/services/file-upload-service.md) - File handling