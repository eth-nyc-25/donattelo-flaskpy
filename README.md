# Donattelo Flask + Walrus Storage

A Flask application that integrates with the Walrus decentralized storage system for analyzing images and storing them with metadata.

## Features

- **Image Analysis**: Analyze uploaded images and extract metadata
- **Walrus Storage**: Store images and metadata in decentralized storage
- **Metadata Extraction**: Extract comprehensive image information using Pillow
- **RESTful API**: Clean API endpoints for image operations
- **Error Handling**: Comprehensive error handling with Walrus API integration

## Prerequisites

- Python 3.8+
- Walrus testnet access
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd donattelo-flaskpy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env_template.txt .env
# Edit .env with your configuration
```

## Configuration

The application uses the following Walrus testnet endpoints:
- Publisher: `https://publisher.walrus-testnet.walrus.space`
- Aggregator: `https://aggregator.walrus-testnet.walrus.space`

## Usage

### Starting the Application

```bash
python app.py
```

The Flask server will start on `http://localhost:5000`

### API Endpoints

#### Health Check
```
GET /health
```

#### Analyze and Store Image
```
POST /analyze/image
Content-Type: multipart/form-data

image: [image file]
```

#### Download Image
```
GET /image/<blob_id>
```

#### Download Metadata
```
GET /metadata/<blob_id>
```

#### List Blobs (Placeholder)
```
GET /blobs
```

## Testing

### 1. Test Walrus SDK Independently

First, test the Walrus SDK functionality:

```bash
python test_walrus_sdk.py
```

This will test:
- Connection to Walrus
- Upload operations
- Download operations
- Metadata operations
- File upload operations

### 2. Test the Flask API

Start the Flask server, then run:

```bash
python test_api.py
```

This will test:
- Health check endpoint
- Image analysis and storage
- Image download
- Metadata download
- Other API endpoints

### 3. Test Local Functionality

Test the image analysis and storage without the web server:

```bash
python local_test.py
```

## Project Structure

```
donattelo-flaskpy/
├── app.py                 # Main Flask application
├── walrus_storage.py      # Walrus storage integration
├── image_analyzer.py      # Image analysis functionality
├── test_walrus_sdk.py     # Walrus SDK tests
├── test_api.py            # API endpoint tests
├── local_test.py          # Local functionality tests
├── requirements.txt       # Python dependencies
├── env_template.txt       # Environment variables template
├── test/                  # Test files and results
│   ├── img/              # Test images
│   └── results/          # Test results
└── output/               # Generated output files
```

## Walrus Integration Details

The application integrates with the [Walrus Python SDK](https://github.com/standard-crypto/walrus-python) to provide:

- **Decentralized Storage**: Store images and metadata on the Sui blockchain
- **Blob Management**: Upload, download, and manage binary data
- **Metadata Storage**: Store structured data alongside binary content
- **Error Handling**: Proper handling of Walrus API errors

### Key Walrus Operations

1. **Upload**: `client.put_blob()` for binary data
2. **Download**: `client.get_blob()` for retrieving data
3. **Metadata**: `client.get_blob_metadata()` for blob information
4. **File Upload**: `client.put_blob_from_file()` for file-based uploads

## Image Analysis Features

The application extracts comprehensive metadata from uploaded images:

- **Basic Information**: Filename, format, dimensions, mode
- **File Details**: File size, analysis timestamp
- **Image Properties**: Color space, compression, etc.
- **Technical Data**: Any additional metadata available from the image

## Error Handling

The application includes comprehensive error handling:

- **Walrus API Errors**: Catches and handles `WalrusAPIError` exceptions
- **File Operations**: Proper cleanup of temporary files
- **Input Validation**: Validates file types and request parameters
- **HTTP Status Codes**: Appropriate HTTP responses for different error types

## Development

### Adding New Features

1. **New Endpoints**: Add routes in `app.py`
2. **Storage Operations**: Extend `walrus_storage.py`
3. **Image Processing**: Enhance `image_analyzer.py`
4. **Testing**: Add corresponding tests

### Debugging

- Enable Flask debug mode: `app.run(debug=True)`
- Check Walrus SDK logs for storage operations
- Monitor test results in `test/results/` directory

## Troubleshooting

### Common Issues

1. **Connection Errors**: Ensure Walrus testnet is accessible
2. **Upload Failures**: Check file size and format
3. **Download Errors**: Verify blob IDs are valid
4. **Import Errors**: Ensure all dependencies are installed

### Walrus-Specific Issues

- **API Rate Limits**: Walrus may have rate limiting
- **Network Issues**: Testnet endpoints may be unstable
- **SDK Version**: Ensure compatibility with `walrus-python==0.1.0`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Your License Here]

## Support

For issues related to:
- **Walrus SDK**: Check the [official repository](https://github.com/standard-crypto/walrus-python)
- **Application**: Open an issue in this repository
- **Blockchain**: Refer to Sui documentation
