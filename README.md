# Campus Help Assistant (Frontend + Backend)

This project is a demo **Campus Help Assistant** chatbot:
- Frontend: HTML + Tailwind + JavaScript (connects to Amazon Lex)
- Backend: AWS Lambda (Python) used as Lex fulfillment
- Database: Amazon DynamoDB table `Complaints`

> IMPORTANT: This repo contains placeholders. **Do not** add AWS secrets to the files. Replace placeholders with your AWS resource IDs.

## Files in this package
- `index.html` - Web UI for the chatbot
- `script.js` - Frontend logic; communicates with Amazon Lex (V2)
- `lambda_function.py` - Lambda function (Python) to save complaints and check status in DynamoDB
- `requirements.txt` - Python dependencies for local testing / packaging
- `style.css` - (optional local styles)

## Setup overview

1. **Create DynamoDB table**
   - Table name: `Complaints`
   - Primary key: `complaintId` (String)

2. **Create Lambda function**
   - Runtime: Python 3.10 or 3.11
   - Handler: `lambda_function.lambda_handler`
   - Add environment variable `TABLE_NAME` if you change the table name
   - Attach IAM policy allowing `dynamodb:PutItem`, `dynamodb:GetItem`, and CloudWatch logs

   Example minimal IAM policy (attach to Lambda role):
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "dynamodb:PutItem",
           "dynamodb:GetItem",
           "dynamodb:Query",
           "dynamodb:Scan"
         ],
         "Resource": "arn:aws:dynamodb:YOUR_REGION:YOUR_ACCOUNT_ID:table/Complaints"
       },
       {
         "Effect": "Allow",
         "Action": [
           "logs:CreateLogGroup",
           "logs:CreateLogStream",
           "logs:PutLogEvents"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

3. **Create Lex Bot**
   - Use Amazon Lex V2
   - Create intents:
     - `GreetingIntent` (no slots)
     - `ComplaintIntent` with slots: `UserName`, `Issue`
     - `StatusIntent` with slot: `ComplaintID`
   - Under **Fulfillment**, select **AWS Lambda** and choose the Lambda function you've created. Enable the necessary permissions when prompted.

4. **Cognito Identity Pool (for browser access)**
   - Create an Identity Pool (unauthenticated access allowed) and attach a policy that allows `lex:RecognizeText` for your bot ARN.
   - In `script.js`, replace `YOUR_IDENTITY_POOL_ID`, `YOUR_REGION`, `YOUR_BOT_ID`, and `YOUR_BOT_ALIAS_ID`.

5. **Host frontend**
   - Upload `index.html`, `script.js` to S3 (static website hosting) or use AWS Amplify.

## Testing
- Open the hosted `index.html` in a browser.
- Type messages to interact with the Lex bot.
- For complaints: provide a name and issue when prompted. The Lambda will save the complaint and return an ID.
- For status: ask `What is the status of complaint <ID>` or use the `StatusIntent`.

## Notes
- This project is a starter template. Add validations, error handling, authentication (Cognito auth flow), and admin dashboards as next steps.
- If you plan to expose admin APIs (to read/update DynamoDB), create separate API Gateway + Lambda endpoints secured with Cognito authorizers.

