## Build Vaccination Verification Solution Using Amazon Textract Queries

### Overview:

As travel resumes post-pandemic, verifying a traveler’s vaccination status may be required in many cases. Hotels and travel agencies often need to review vaccination cards to gather important details like whether the traveler is fully vaccinated, vaccine dates, and the traveler’s name. Some agencies do this through manual verification of cards, which can be time-consuming for staff and leaves room for human error.

Amazon Textract Queries helps address these challenges as it allows you to specify and extract only the piece of information that you need from the document, giveing you precise and accurate information from the document.

Follow the step-by-step implementation guide to build a vaccination status verification solution using Amazon Textract Queries. The solution showcases how to process vaccination cards using an Amazon Textract query, verify the vaccination status, and store the information for future use.

### High Level Architecture:

![image](https://github.com/aws-samples/build-vaccination-verification-solution-using-amazon-textract-queries/assets/45221995/0148e14a-68ea-464c-8dc5-b60411b03330)


The workflow includes the following steps:

1) The user takes a photo of a vaccination card.

2) The image is uploaded to an Amazon Simple Storage Service (Amazon S3) bucket.

3) When the image gets saved in the S3 bucket, it invokes an AWS Step Functions workflow:

4) The **"Queries-Decider"** AWS Lambda function examines the document passed in and adds information about the mime type, the number of pages, and the number of queries to the Step Functions workflow (for our example, we have four queries).

5) **"NumberQueriesAndPagesChoice"** is a Choice state that adds conditional logic to a workflow. If there are between 15–31 queries and the number of pages is between 2–3,001, then Amazon Textract asynchronous processing is the only option, because synchronous APIs only support up to 15 queries and one-page documents. For all other cases, we route to the random selection of synchronous or asynchronous processing.

6) The **"TextractSync"** Lambda function sends a request to Amazon Textract to analyze the document based on the following Amazon Textract queries:
  a) What is Vaccination Status?
  b) What is Name?
  c) What is Date of Birth?
  d) What is Document Number?

7) Amazon Textract analyzes the image and sends the answers of these queries back to the Lambda function.

8) The Lambda function verifies the customer’s vaccination status and stores the final result in CSV format in the same S3 bucket (**"demoqueries-textractxxx"**) in the **"csv-output"** folder.

### Deployment Steps:

1) Create an AWS Cloud9 instance and install the necessary dependencies on the instance with the AWS Cloud Development Kit (AWS CDK) and Docker. AWS Cloud9 is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser.

2) In the terminal, choose **"Upload Local Files"** on the **"File"** menu.
3) Choose **"Select folder"** and choose the *"vaccination_verification_solution"* folder you downloaded from GitHub.
4) In the terminal, prepare your serverless application for subsequent steps in your development workflow in AWS Serverless Application Model (AWS SAM) using the following command:

   ```
   $ cd vaccination_verification_solution/
   $ pip install -r requirements.txt
   ```
5) Deploy the application using the cdk deploy command:

   ```
   $ cdk deploy DemoQueries --outputs-file demo_queries.json --require-approval never
   ```

6) When deployment is complete, you can check the deployed resources on the AWS CloudFormation console on the **Resources** tab of the stack details page.

### Test the Solution:

1) To trigger the workflow, use *"aws s3"* cp to upload the *"vac_card.jpg"* file to *"DemoQueries.DocumentUploadLocation"* inside the docs folder:

   ```
   $ aws s3 cp docs/vac_card.JPG $(aws cloudformation list-exports --query 'Exports[?Name==`DemoQueries-DocumentUploadLocation`].Value' --output text)
   ```

2) The vaccination certificate file automatically gets uploaded to the S3 bucket *"demoqueries-textractxxx"* in the uploads folder.
3) The Step Functions workflow is triggered via a Lambda function as soon as the vaccination certificate file is uploaded to the S3 bucket.
4) The final output is stored in the same S3 bucket in the csv-output folder as a CSV file. You can download the file to your local machine using the following command:

   ```
   $ aws s3 cp <paste the S3 URL from TextractOutputCSVPath>
   ```
5) The format of the result is timestamp, classification, filename, page number, key name, key_confidence, value, value_confidence, key_bb_top, key_bb_height, key_bb.width, key_bb_left, value_bb_top, value_bb_height, value_bb_width, value_bb_left.

   ![image](https://github.com/aws-samples/build-vaccination-verification-solution-using-amazon-textract-queries/assets/45221995/f81ac694-a0c9-4d41-b776-28fd20f1a0f3)


### Note: ###

You can scale the solution to hundreds of vaccination certificate documents for multiple customers by uploading their vaccination certificates to *"DemoQueries.DocumentUploadLocation"*. This automatically triggers multiple runs of the Step Functions state machine, and the final result is stored in the same S3 bucket in the csv-output folder.

To change the initial set of queries that are fed into Amazon Textract, you can go to your AWS Cloud9 instance and open the *"start_execution.py"* file. In the file view in the left pane, navigate to lambda, *"start_queries, app, start_execution.py"*. This Lambda function is invoked when a file is uploaded to *"DemoQueries.DocumentUploadLocation"*. The queries sent to the workflow are defined in *"start_execution.py;"* you can change those by updating the code as shown in the following screenshot:

![image](https://github.com/aws-samples/build-vaccination-verification-solution-using-amazon-textract-queries/assets/45221995/b1a6c8c1-6851-4182-8507-bcbbf8561bd3)

### Clean Up ###

To avoid incurring ongoing charges, delete the resources created using the following command:

   ``` 
   $ cdk destroy DemoQueries
   ```


   
   

