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

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

