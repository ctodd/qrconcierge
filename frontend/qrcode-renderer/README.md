# QR Code Generator

A TypeScript-based web application that generates QR codes using tokens from an API. The application includes a countdown animation indicating when the token expires and automatically requests a new token upon expiration.

## Features

- Generate QR codes using tokens from an API
- Countdown animation showing token expiration time
- Automatic token refresh upon expiration
- Optional geolocation support
- Error handling with meaningful messages based on status codes

## API Integration

The application integrates with an API endpoint to retrieve tokens:

- Endpoint: `https://lgnd27dxvc.execute-api.us-east-1.amazonaws.com/prod/getToken`
- Required parameters:
  - `uniqueId`: A unique identifier (e.g., phone number)
- Optional parameters:
  - `latitude`: User's latitude coordinate
  - `longitude`: User's longitude coordinate

## Project Structure

```
qrcode-generator/
├── src/
│   ├── components/
│   │   └── QRCodeDisplay.tsx    # QR code display with countdown
│   ├── App.tsx                  # Main application component
│   ├── api.ts                   # API integration
│   ├── types.ts                 # TypeScript interfaces
│   ├── main.tsx                 # Application entry point
│   └── index.css                # Styles
├── public/
├── cloudformation/
│   └── deployment-stack.yaml    # CloudFormation template for deployment
├── index.html                   # HTML entry point
├── package.json                 # Dependencies and scripts
├── tsconfig.json                # TypeScript configuration
└── vite.config.ts               # Vite configuration
```

## Development Setup

1. Install dependencies:
   ```
   npm install
   ```

2. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```
   
   Then update the `.env` file with your actual API URL.

3. Start the development server:
   ```
   npm run dev
   ```

4. Build for production:
   ```
   npm run build
   ```

## Deployment

The application can be deployed using the provided CloudFormation templates:

1. Deploy the hosting infrastructure:
   ```
   aws cloudformation deploy \
     --template-file cloudformation/hosting-stack.yaml \
     --stack-name qrcode-generator-hosting \
     --parameter-overrides \
       DomainName=example.com \
       CertificateArn=arn:aws:acm:us-east-1:123456789012:certificate/abcd1234-abcd-1234-abcd-1234abcd5678
   ```

2. Build and upload the application to an S3 bucket:
   ```
   npm run build
   zip -r build.zip dist/
   aws s3 cp build.zip s3://your-artifact-bucket/qrcode-generator/build.zip
   ```

3. Deploy the application to a subdirectory:
   ```
   aws cloudformation deploy \
     --template-file cloudformation/deployment-stack.yaml \
     --stack-name qrcode-generator-deployment \
     --parameter-overrides \
       HostingStackName=qrcode-generator-hosting \
       SubdirectoryPath=qrcode-generator \
       ArtifactBucket=your-artifact-bucket \
       ArtifactKey=qrcode-generator/build.zip
   ```

## License

MIT
