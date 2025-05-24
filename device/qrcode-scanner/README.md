# QR Code Scanner

A Python application that uses the Mac laptop camera to scan QR codes and sends the contents to a validateToken API endpoint.

## Requirements

- Python 3.6+
- macOS
- Access to laptop camera

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Configure the environment variables by creating a `.env` file:

```
API_BASE_URL=https://lgnd27dxvc.execute-api.us-east-1.amazonaws.com
API_STAGE=prod
API_RESOURCE=/validateToken
API_KEY=your_api_key_here
```

## Usage

Run the script:

```bash
python qr_scanner.py
```

For verbose mode that shows detailed QR code contents:

```bash
python qr_scanner.py --verbose
```

or

```bash
python qr_scanner.py -v
```

To customize the delay between scans (default is 3 seconds):

```bash
python qr_scanner.py --delay 5
```

or 

```bash
python qr_scanner.py -d 5
```

You can combine options:

```bash
python qr_scanner.py -v -d 5
```

- Position a QR code in front of your camera
- The script will detect the QR code, extract its content, and send it to the API
- After a successful scan, the scanner will wait for the specified delay before accepting a new scan
- Press 'q' to quit the application

## Configuration

The application uses environment variables loaded from a `.env` file:

- `API_BASE_URL`: The base URL of the API (default: https://lgnd27dxvc.execute-api.us-east-1.amazonaws.com)
- `API_STAGE`: The API stage (default: prod)
- `API_RESOURCE`: The API resource path (default: /validateToken)
- `API_KEY`: Your API key for authentication

## Troubleshooting

If you encounter camera access issues:
1. Make sure your application has permission to access the camera
2. Go to System Preferences > Security & Privacy > Camera and enable access for Terminal or your Python IDE

If you encounter API connection issues:
1. Verify your API key is correct in the `.env` file
2. Check your internet connection
3. Run in verbose mode to see detailed request and response information
