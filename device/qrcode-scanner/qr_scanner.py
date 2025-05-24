#!/usr/bin/env python3
"""
QR Code Scanner for Mac
-----------------------
This script uses the Mac laptop camera to scan QR codes and sends the contents
to a validateToken API endpoint.
"""

import cv2
import requests
import time
import json
import sys
import argparse
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API configuration from environment variables
API_BASE_URL = os.getenv('API_BASE_URL', '')
API_STAGE = os.getenv('API_STAGE', 'prod')
API_RESOURCE = os.getenv('API_RESOURCE', '/validateToken')
API_KEY = os.getenv('API_KEY', '')

# Construct the full API endpoint
API_ENDPOINT = f"{API_BASE_URL}/{API_STAGE}{API_RESOURCE}"

def validate_token(token_data, verbose=False):
    """
    Send the token data to the validation API endpoint
    
    Args:
        token_data (str): The data extracted from the QR code
        verbose (bool): Whether to print detailed information
        
    Returns:
        dict: The API response
    """
    if verbose:
        print(f"QR Code Content: {token_data}")
        print(f"Content Length: {len(token_data)} characters")
        try:
            # Try to parse as JSON if it looks like JSON
            if token_data.strip().startswith('{') and token_data.strip().endswith('}'):
                parsed = json.loads(token_data)
                print(f"Content appears to be JSON: {json.dumps(parsed, indent=2)}")
        except json.JSONDecodeError:
            pass
            
    try:
        headers = {
            'Content-Type': 'application/json',
        }
        
        # Add API key to headers if available
        if API_KEY:
            headers['x-api-key'] = API_KEY
        
        payload = {
            'token': token_data
        }
        
        if verbose:
            print(f"Sending payload to {API_ENDPOINT}: {json.dumps(payload, indent=2)}")
            # Don't print API key in logs
            safe_headers = headers.copy()
            if 'x-api-key' in safe_headers:
                safe_headers['x-api-key'] = '***hidden***'
            print(f"Headers: {safe_headers}")
            
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        
        if verbose:
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"error": str(e)}

def is_valid_url(url):
    """Check if the string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def scan_qr_code(verbose=False, scan_delay=3):
    """
    Access the camera and scan for QR codes
    
    Args:
        verbose (bool): Whether to print detailed information about QR code contents
        scan_delay (int): Delay in seconds between valid scans
    """
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is usually the built-in camera
    
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return
    
    # Initialize QR Code detector
    qr_detector = cv2.QRCodeDetector()
    
    print("QR Code Scanner is running. Press 'q' to quit.")
    print("Position a QR code in front of the camera...")
    print(f"Waiting {scan_delay} seconds between valid scans...")
    
    last_scan_time = 0
    last_data = None
    scanning_enabled = True
    
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        current_time = time.time()
        
        # Check if we should re-enable scanning
        if not scanning_enabled and (current_time - last_scan_time >= scan_delay):
            scanning_enabled = True
            print("Scanner ready for next QR code...")
        
        # Try to detect and decode QR code
        data, bbox, _ = qr_detector.detectAndDecode(frame)
        
        # If a QR code is detected and scanning is enabled
        if data and scanning_enabled and data != last_data:
            print(f"QR Code detected!")
            if verbose:
                print(f"Content: {data}")
            
            # Send to API
            print("Sending to validation API...")
            response = validate_token(data, verbose)
            print(f"API Response: {json.dumps(response, indent=2)}")
            
            # Update tracking variables
            last_scan_time = current_time
            last_data = data
            scanning_enabled = False
            
            # Display countdown message
            print(f"Waiting {scan_delay} seconds before next scan...")
        
        # Draw bounding box around QR code if detected
        if bbox is not None and len(bbox) > 0:
            # Convert bbox to integer points
            bbox = bbox.astype(int)
            # Draw rectangle
            cv2.polylines(frame, [bbox], True, (0, 255, 0), 2)
            
            # Add text if data was detected
            if data:
                cv2.putText(frame, "QR Code Detected", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Add content preview if verbose mode is on
                if verbose and data:
                    # Truncate data if it's too long
                    preview = data if len(data) < 30 else data[:27] + "..."
                    cv2.putText(frame, f"Content: {preview}", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Show scanning status
                if not scanning_enabled:
                    time_left = max(0, int(scan_delay - (current_time - last_scan_time)))
                    cv2.putText(frame, f"Next scan in: {time_left}s", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Display the frame
        cv2.imshow("QR Code Scanner", frame)
        
        # Check for key press to exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='QR Code Scanner for Mac')
        parser.add_argument('-v', '--verbose', action='store_true', 
                            help='Enable verbose mode to print detailed QR code contents')
        parser.add_argument('-d', '--delay', type=int, default=3,
                            help='Delay in seconds between valid scans (default: 3)')
        args = parser.parse_args()
        
        # Print API configuration (without sensitive info)
        print(f"API Endpoint: {API_ENDPOINT}")
        print(f"API Key: {'Configured' if API_KEY else 'Not configured'}")
        
        # Run the scanner with the verbose flag and specified delay
        scan_qr_code(args.verbose, args.delay)
    except KeyboardInterrupt:
        print("\nQR Code Scanner stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
