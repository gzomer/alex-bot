# Alex - Your personal assistant at work
![](https://github.com/gzomer/alex-bot/blob/master/assets/readme_images/intro.png)

Alex is a chat bot that helps you at work, saving your time and boosting your productivity 💪.

He can help you to ask for expenses refunds, add tasks, create tickets, find documents and answer questions.

One more thing: Alex is friend of Alexa 😬.

Click below 👇 to see the demo 😎

[<img src="https://img.youtube.com/vi/VWoXdn9n9fY/maxresdefault.jpg" width="50%">](https://youtu.be/VWoXdn9n9fY)

# Table of contents


- [Features](#features)
- [Architecture](#architecture)
	- [AWS Services](#aws-services-used)
	- [AWS Curated models](#aws-curated-models-used)
	- [Sequence Diagrams](#sequence-diagrams)
		- [Send passport](#send-passport)
		- [Add task](#add-task)
		- [Open ticket](#open-ticket)
		- [Extract expense](#extract-expense)
		- [Find document](#find-document)
		- [Ask question](#ask-question)		
- [Inputs and Outputs](#inputs-and-outputs)
- [Testing](#testing)
	- [Models](#models)
	- [Use-cases](#use-cases)
- [Deploying](#deploying)

# Features

| Feature | Message | Code | AWS Curated Models used | AWS Services used
| :--: | :--: | :--: | :--: | :--: |
| Send passport| *Alex, here is my passport* | [lambda_send_passport.py](https://github.com/gzomer/alex-bot/blob/master/lambda_send_passport.py) |`Passport Data Page Detection`|`Lex` `S3` `SageMaker` |
| Add task| *Alex, can you add a task* | [lambda_add_task.py](https://github.com/gzomer/alex-bot/blob/master/lambda_add_task.py) |`Mphasis Autocode WireframeToCode`|`Lex` `S3` `SageMaker` `Alexa Skills`|
| Add expense| *Alex, can you add this expense* | [lambda_track_expense.py](https://github.com/gzomer/alex-bot/blob/master/lambda_track_expense.py) |`Mphasis DeepInsights Address Extraction`|`Lex` `S3` `SageMaker` `Textract` `Comprehend`|
| Open ticket| *Alex, can you open a ticket* | [lambda_open_ticket.py](https://github.com/gzomer/alex-bot/blob/master/lambda_open_ticket.py) |`Mphasis Optimize.AI Expert Identifier`|`Lex` `S3` `SageMaker` `Kendra`|
| Find document| *Alex, can you find a document* | [lambda_find_document.py](https://github.com/gzomer/alex-bot/blob/master/lambda_find_document.py) |`Mphasis DeepInsights Text Summarizer `|`Lex` `S3` `SageMaker` `Kendra`|
| Ask question | *Alex, {how, what, why} ...* | [lambda_ask_question.py](https://github.com/gzomer/alex-bot/blob/master/lambda_ask_question.py) || `S3` `Kendra` `Alexa Skills` `Lex`|

# Architecture


![Architecture](https://github.com/gzomer/alex-bot/blob/master/assets/readme_images/architecture.png)

### AWS Services used
- Amazon Lex
- Amazon S3
- Amazon Textract
- Amazon Comprehend
- Amazon SageMaker
- Amazon Kendra
- Alexa Skills

### AWS Curated models used
- Passport Data Page Detection
- Mphasis Autocode WireframeToCode
- Mphasis DeepInsights Address Extraction
- Mphasis Optimize.AI Expert Identifier
- Mphasis DeepInsights Text Summarizer


### Sequence diagrams

#### Send Passport
[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IEhlcmUgaXMgbXkgcGFzc3BvcnRcbiAgTGV4LT4-bGFtYmRhX2FsZXhfZmxvdzogU2VuZFBhc3Nwb3J0SW50ZW50XG4gIGxhbWJkYV9hbGV4X2Zsb3ctPj5sYW1iZGFfc2VuZF9wYXNzcG9ydDogeyBJbWFnZTondXBsb2FkZWRJbWFnZSd9XG4gIGxhbWJkYV9zZW5kX3Bhc3Nwb3J0LT4-UGFzc3BvcnQgTW9kZWw6IGltYWdlX2RhdGEgKGJ5dGVzKVxuICBQYXNzcG9ydCBNb2RlbC0tPj5sYW1iZGFfc2VuZF9wYXNzcG9ydDogcmV0dXJuIHBhc3Nwb3J0X2RldGFpbHNcbiAgbGFtYmRhX3NlbmRfcGFzc3BvcnQtLT4-bGFtYmRhX2FsZXhfZmxvdzogcmV0dXJuIHBhc3Nwb3J0X2RldGFpbHNcbiAgbGFtYmRhX2FsZXhfZmxvdy0tPj5MZXg6IERvIHlvdSBjb25maXJtIHlvdXIgcGFzc3BvcnQgaW5mbyBpcyAuLi5cbiAgTGV4LS0-PlVzZXI6IERvIHlvdSBjb25maXJtIHlvdXIgcGFzc3BvcnQgaW5mbyBpcyAuLi4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IEhlcmUgaXMgbXkgcGFzc3BvcnRcbiAgTGV4LT4-bGFtYmRhX2FsZXhfZmxvdzogU2VuZFBhc3Nwb3J0SW50ZW50XG4gIGxhbWJkYV9hbGV4X2Zsb3ctPj5sYW1iZGFfc2VuZF9wYXNzcG9ydDogeyBJbWFnZTondXBsb2FkZWRJbWFnZSd9XG4gIGxhbWJkYV9zZW5kX3Bhc3Nwb3J0LT4-UGFzc3BvcnQgTW9kZWw6IGltYWdlX2RhdGEgKGJ5dGVzKVxuICBQYXNzcG9ydCBNb2RlbC0tPj5sYW1iZGFfc2VuZF9wYXNzcG9ydDogcmV0dXJuIHBhc3Nwb3J0X2RldGFpbHNcbiAgbGFtYmRhX3NlbmRfcGFzc3BvcnQtLT4-bGFtYmRhX2FsZXhfZmxvdzogcmV0dXJuIHBhc3Nwb3J0X2RldGFpbHNcbiAgbGFtYmRhX2FsZXhfZmxvdy0tPj5MZXg6IERvIHlvdSBjb25maXJtIHlvdXIgcGFzc3BvcnQgaW5mbyBpcyAuLi5cbiAgTGV4LS0-PlVzZXI6IERvIHlvdSBjb25maXJtIHlvdXIgcGFzc3BvcnQgaW5mbyBpcyAuLi4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)

#### Add task
[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiB5b3UgYWRkIGEgdGFza1xuICBMZXgtPj5sYW1iZGFfYWxleF9mbG93OiBBZGRUYXNrSW50ZW50XG4gIGxhbWJkYV9hbGV4X2Zsb3ctPj5sYW1iZGFfYWRkX3Rhc2s6IHsgVGl0bGU6J3RpdGxlJywgSW1hZ2U6J3VwbG9hZGVkSW1hZ2UnfVxuICBsYW1iZGFfYWRkX3Rhc2stPj5XaXJlZnJhbWVUb0NvZGU6IGltYWdlX2RhdGEgKGJ5dGVzKSA8YnI-IGdlbmVyYXRlX3dpcmVmcmFtZVxuICBXaXJlZnJhbWVUb0NvZGUtLT4-bGFtYmRhX2FkZF90YXNrOiByZXR1cm4gd2lyZWZyYW1lX2NvbnRlbnRcbiAgbGFtYmRhX2FkZF90YXNrLT4-UzM6IHNhdmVfd2lyZWZyYW1lXG4gIFMzLS0-PmxhbWJkYV9hZGRfdGFzazogcmV0dXJuIHdpcmVmcmFtZV91cmxcbiAgbGFtYmRhX2FkZF90YXNrLS0-PlRyZWxsbzoge25hbWU6J3RpdGxlJywgJ2F0dGFjaG1lbnRzJzpbLi4uXX08YnI-IGNyZWF0ZV90YXNrXG4gIFRyZWxsby0tPj5sYW1iZGFfYWRkX3Rhc2s6IHJldHVybiBjcmVhdGVkX2NhcmRcbiAgbGFtYmRhX2FkZF90YXNrLS0-PmxhbWJkYV9hbGV4X2Zsb3c6IHsnVXJsJzondXJsX3RyZWxsbyd9XG4gIGxhbWJkYV9hbGV4X2Zsb3ctLT4-TGV4OiBIZXJlIGlzIHRoZSBsaW5rIG9mIHlvdXIgbmV3IGNhcmQgLi4uXG4gIExleC0tPj5Vc2VyOiAgSGVyZSBpcyB0aGUgbGluayBvZiB5b3VyIG5ldyBjYXJkIC4uLiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiB5b3UgYWRkIGEgdGFza1xuICBMZXgtPj5sYW1iZGFfYWxleF9mbG93OiBBZGRUYXNrSW50ZW50XG4gIGxhbWJkYV9hbGV4X2Zsb3ctPj5sYW1iZGFfYWRkX3Rhc2s6IHsgVGl0bGU6J3RpdGxlJywgSW1hZ2U6J3VwbG9hZGVkSW1hZ2UnfVxuICBsYW1iZGFfYWRkX3Rhc2stPj5XaXJlZnJhbWVUb0NvZGU6IGltYWdlX2RhdGEgKGJ5dGVzKSA8YnI-IGdlbmVyYXRlX3dpcmVmcmFtZVxuICBXaXJlZnJhbWVUb0NvZGUtLT4-bGFtYmRhX2FkZF90YXNrOiByZXR1cm4gd2lyZWZyYW1lX2NvbnRlbnRcbiAgbGFtYmRhX2FkZF90YXNrLT4-UzM6IHNhdmVfd2lyZWZyYW1lXG4gIFMzLS0-PmxhbWJkYV9hZGRfdGFzazogcmV0dXJuIHdpcmVmcmFtZV91cmxcbiAgbGFtYmRhX2FkZF90YXNrLS0-PlRyZWxsbzoge25hbWU6J3RpdGxlJywgJ2F0dGFjaG1lbnRzJzpbLi4uXX08YnI-IGNyZWF0ZV90YXNrXG4gIFRyZWxsby0tPj5sYW1iZGFfYWRkX3Rhc2s6IHJldHVybiBjcmVhdGVkX2NhcmRcbiAgbGFtYmRhX2FkZF90YXNrLS0-PmxhbWJkYV9hbGV4X2Zsb3c6IHsnVXJsJzondXJsX3RyZWxsbyd9XG4gIGxhbWJkYV9hbGV4X2Zsb3ctLT4-TGV4OiBIZXJlIGlzIHRoZSBsaW5rIG9mIHlvdXIgbmV3IGNhcmQgLi4uXG4gIExleC0tPj5Vc2VyOiAgSGVyZSBpcyB0aGUgbGluayBvZiB5b3VyIG5ldyBjYXJkIC4uLiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

#### Extract expense

[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiB5b3UgYWRkIHRoaXMgZXhwZW5zZVxuICBMZXgtPj5sYW1iZGFfYWxleF9mbG93OiBUcmFja0V4cGVuc2VJbnRlbnRcbiAgbGFtYmRhX2FsZXhfZmxvdy0-PmxhbWJkYV90cmFja19leHBlbnNlOiB7IEltYWdlOid1cGxvYWRlZEltYWdlJ31cbiAgbGFtYmRhX3RyYWNrX2V4cGVuc2UtPj5UZXh0cmFjdDogaW1hZ2VfZGF0YSAoYnl0ZXMpIDxicj4gZXh0cmFjdF90ZXh0XG4gIFRleHRyYWN0LS0-PmxhbWJkYV90cmFja19leHBlbnNlOiByZXR1cm4gZGV0ZWN0ZWRfYmxvY2tzXG4gIGxhbWJkYV90cmFja19leHBlbnNlLT4-Q29tcHJlaGVuZDogZGV0ZWN0X2tleV9waHJhc2VzXG4gIENvbXByZWhlbmQtLT4-bGFtYmRhX3RyYWNrX2V4cGVuc2U6IHJldHVybiBrZXlfcGhyYXNlc1xuICBsYW1iZGFfdHJhY2tfZXhwZW5zZS0-PmxhbWJkYV90cmFja19leHBlbnNlOiB7S2V5UGhyYXNlczpbLi4uXX0gPGJyPiBnZXRfcHJpY2VcbiAgbGFtYmRhX3RyYWNrX2V4cGVuc2UtPj5Db21wcmVoZW5kOiBkZXRlY3Rfc3ludGF4XG4gIENvbXByZWhlbmQtLT4-bGFtYmRhX3RyYWNrX2V4cGVuc2U6IHJldHVybiBzeW50YXhcbiAgbGFtYmRhX3RyYWNrX2V4cGVuc2UtPj5sYW1iZGFfdHJhY2tfZXhwZW5zZToge1BPUzpbLi4uXX0gPGJyPiBnZXRfc3RvcmVcbiAgbGFtYmRhX3RyYWNrX2V4cGVuc2UtPj5BZGRyZXNzRXh0cmFjdGlvbjoge2Jsb2NrczpbLi4uXX0gPGJyPiBnZXRfbG9jYXRpb25cbiAgQWRkcmVzc0V4dHJhY3Rpb24tLT4-bGFtYmRhX3RyYWNrX2V4cGVuc2U6IHJldHVybiBhZGRyZXNzXG4gIGxhbWJkYV90cmFja19leHBlbnNlLS0-PmxhbWJkYV9hbGV4X2Zsb3c6IHsnUHJpY2UnOiAnJywgJ0xvY2F0aW9uJzogJycsICdTdG9yZSc6ICcnfSA8YnI-IHJldHVyblxuICBsYW1iZGFfYWxleF9mbG93LS0-PkxleDogQ2FuIHlvdSBjb25maXJtIHRoaXMgaXMgYW4gZXhwZW5zZSBvZiAuLi5cbiAgTGV4LS0-PlVzZXI6ICBDYW4geW91IGNvbmZpcm0gdGhpcyBpcyBhbiBleHBlbnNlIG9mIC4uLiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiB5b3UgYWRkIHRoaXMgZXhwZW5zZVxuICBMZXgtPj5sYW1iZGFfYWxleF9mbG93OiBUcmFja0V4cGVuc2VJbnRlbnRcbiAgbGFtYmRhX2FsZXhfZmxvdy0-PmxhbWJkYV90cmFja19leHBlbnNlOiB7IEltYWdlOid1cGxvYWRlZEltYWdlJ31cbiAgbGFtYmRhX3RyYWNrX2V4cGVuc2UtPj5UZXh0cmFjdDogaW1hZ2VfZGF0YSAoYnl0ZXMpIDxicj4gZXh0cmFjdF90ZXh0XG4gIFRleHRyYWN0LS0-PmxhbWJkYV90cmFja19leHBlbnNlOiByZXR1cm4gZGV0ZWN0ZWRfYmxvY2tzXG4gIGxhbWJkYV90cmFja19leHBlbnNlLT4-Q29tcHJlaGVuZDogZGV0ZWN0X2tleV9waHJhc2VzXG4gIENvbXByZWhlbmQtLT4-bGFtYmRhX3RyYWNrX2V4cGVuc2U6IHJldHVybiBrZXlfcGhyYXNlc1xuICBsYW1iZGFfdHJhY2tfZXhwZW5zZS0-PmxhbWJkYV90cmFja19leHBlbnNlOiB7S2V5UGhyYXNlczpbLi4uXX0gPGJyPiBnZXRfcHJpY2VcbiAgbGFtYmRhX3RyYWNrX2V4cGVuc2UtPj5Db21wcmVoZW5kOiBkZXRlY3Rfc3ludGF4XG4gIENvbXByZWhlbmQtLT4-bGFtYmRhX3RyYWNrX2V4cGVuc2U6IHJldHVybiBzeW50YXhcbiAgbGFtYmRhX3RyYWNrX2V4cGVuc2UtPj5sYW1iZGFfdHJhY2tfZXhwZW5zZToge1BPUzpbLi4uXX0gPGJyPiBnZXRfc3RvcmVcbiAgbGFtYmRhX3RyYWNrX2V4cGVuc2UtPj5BZGRyZXNzRXh0cmFjdGlvbjoge2Jsb2NrczpbLi4uXX0gPGJyPiBnZXRfbG9jYXRpb25cbiAgQWRkcmVzc0V4dHJhY3Rpb24tLT4-bGFtYmRhX3RyYWNrX2V4cGVuc2U6IHJldHVybiBhZGRyZXNzXG4gIGxhbWJkYV90cmFja19leHBlbnNlLS0-PmxhbWJkYV9hbGV4X2Zsb3c6IHsnUHJpY2UnOiAnJywgJ0xvY2F0aW9uJzogJycsICdTdG9yZSc6ICcnfSA8YnI-IHJldHVyblxuICBsYW1iZGFfYWxleF9mbG93LS0-PkxleDogQ2FuIHlvdSBjb25maXJtIHRoaXMgaXMgYW4gZXhwZW5zZSBvZiAuLi5cbiAgTGV4LS0-PlVzZXI6ICBDYW4geW91IGNvbmZpcm0gdGhpcyBpcyBhbiBleHBlbnNlIG9mIC4uLiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

#### Open Ticket

[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiB5b3Ugb3BlbiBhIHRpY2tldFxuICBMZXgtPj5sYW1iZGFfYWxleF9mbG93OiBPcGVuVGlja2V0SW50ZW50XG4gIGxhbWJkYV9hbGV4X2Zsb3ctPj5sYW1iZGFfb3Blbl90aWNrZXQ6IHsgRGVzY3JpcHRpb246Jyd9XG4gIGxhbWJkYV9vcGVuX3RpY2tldC0-PktlbmRyYTogRGVzY3JpcHRpb24gPGJyPiBzZWFyY2hfaW5kZXhcbiAgS2VuZHJhLS0-PmxhbWJkYV9vcGVuX3RpY2tldDogcmV0dXJuIHF1ZXJ5X3Jlc3VsdHNcbiAgbGFtYmRhX29wZW5fdGlja2V0LS0-PmxhbWJkYV9hbGV4X2Zsb3c6IHtTdW1tYXJ5fSA8YnI-IHJldHVyblxuICBsYW1iZGFfYWxleF9mbG93LS0-PkxleDogSSBmb3VuZCB0aGlzIC4uLiBEb2VzIGl0IHNvbHZlIHlvdXIgcHJvYmxlbT9cbiAgTGV4LS0-PlVzZXI6IEkgZm91bmQgdGhpcyAuLi4gRG9lcyBpdCBzb2x2ZSB5b3VyIHByb2JsZW0_IFxuICBVc2VyLS0-PkxleDogTm9cbiAgTGV4LT4-bGFtYmRhX2FsZXhfZmxvdzogT3BlblRpY2tldEludGVudFxuICBsYW1iZGFfYWxleF9mbG93LT4-bGFtYmRhX29wZW5fdGlja2V0OiB7IERlc2NyaXB0aW9uOicnfVxuICBsYW1iZGFfb3Blbl90aWNrZXQtPj5FeHBlcnRJZGVudGlmaWVyOiBoaXN0b3JpY2FsICsgbmV3IHRpY2tldCAoQ1NWKSA8YnI-IGdldF9leHBlcnRcbiAgRXhwZXJ0SWRlbnRpZmllci0tPj5sYW1iZGFfb3Blbl90aWNrZXQ6IHJldHVybiBleHBlcnRcbiAgbGFtYmRhX29wZW5fdGlja2V0LS0-PmxhbWJkYV9hbGV4X2Zsb3c6IHtUaWNrZXQ6IC4uLn0gPGJyPiByZXR1cm5cbiAgbGFtYmRhX2FsZXhfZmxvdy0tPj5MZXg6IE9rIHRoZW4sIEkgaGF2ZSBvcGVuZWQgYSB0aWNrZXQgLi4uXG4gIExleC0tPj5Vc2VyOiBPayB0aGVuLCBJIGhhdmUgb3BlbmVkIGEgdGlja2V0IC4uLiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiB5b3Ugb3BlbiBhIHRpY2tldFxuICBMZXgtPj5sYW1iZGFfYWxleF9mbG93OiBPcGVuVGlja2V0SW50ZW50XG4gIGxhbWJkYV9hbGV4X2Zsb3ctPj5sYW1iZGFfb3Blbl90aWNrZXQ6IHsgRGVzY3JpcHRpb246Jyd9XG4gIGxhbWJkYV9vcGVuX3RpY2tldC0-PktlbmRyYTogRGVzY3JpcHRpb24gPGJyPiBzZWFyY2hfaW5kZXhcbiAgS2VuZHJhLS0-PmxhbWJkYV9vcGVuX3RpY2tldDogcmV0dXJuIHF1ZXJ5X3Jlc3VsdHNcbiAgbGFtYmRhX29wZW5fdGlja2V0LS0-PmxhbWJkYV9hbGV4X2Zsb3c6IHtTdW1tYXJ5fSA8YnI-IHJldHVyblxuICBsYW1iZGFfYWxleF9mbG93LS0-PkxleDogSSBmb3VuZCB0aGlzIC4uLiBEb2VzIGl0IHNvbHZlIHlvdXIgcHJvYmxlbT9cbiAgTGV4LS0-PlVzZXI6IEkgZm91bmQgdGhpcyAuLi4gRG9lcyBpdCBzb2x2ZSB5b3VyIHByb2JsZW0_IFxuICBVc2VyLS0-PkxleDogTm9cbiAgTGV4LT4-bGFtYmRhX2FsZXhfZmxvdzogT3BlblRpY2tldEludGVudFxuICBsYW1iZGFfYWxleF9mbG93LT4-bGFtYmRhX29wZW5fdGlja2V0OiB7IERlc2NyaXB0aW9uOicnfVxuICBsYW1iZGFfb3Blbl90aWNrZXQtPj5FeHBlcnRJZGVudGlmaWVyOiBoaXN0b3JpY2FsICsgbmV3IHRpY2tldCAoQ1NWKSA8YnI-IGdldF9leHBlcnRcbiAgRXhwZXJ0SWRlbnRpZmllci0tPj5sYW1iZGFfb3Blbl90aWNrZXQ6IHJldHVybiBleHBlcnRcbiAgbGFtYmRhX29wZW5fdGlja2V0LS0-PmxhbWJkYV9hbGV4X2Zsb3c6IHtUaWNrZXQ6IC4uLn0gPGJyPiByZXR1cm5cbiAgbGFtYmRhX2FsZXhfZmxvdy0tPj5MZXg6IE9rIHRoZW4sIEkgaGF2ZSBvcGVuZWQgYSB0aWNrZXQgLi4uXG4gIExleC0tPj5Vc2VyOiBPayB0aGVuLCBJIGhhdmUgb3BlbmVkIGEgdGlja2V0IC4uLiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

#### Find document

[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiB5b3UgZmluZCBhIGRvY3VtZW50XG4gIExleC0-PmxhbWJkYV9hbGV4X2Zsb3c6IEZpbmREb2N1bWVudEludGVudFxuICBsYW1iZGFfYWxleF9mbG93LT4-bGFtYmRhX2ZpbmRfZG9jdW1lbnQ6IHsgRGVzY3JpcHRpb246Jyd9XG4gIGxhbWJkYV9maW5kX2RvY3VtZW50LT4-S2VuZHJhOiBEZXNjcmlwdGlvbiA8YnI-IHNlYXJjaF9pbmRleFxuICBLZW5kcmEtLT4-bGFtYmRhX2ZpbmRfZG9jdW1lbnQ6IHJldHVybiBxdWVyeV9yZXN1bHRzXG4gIGxhbWJkYV9maW5kX2RvY3VtZW50LT4-U3VtbWFyaXplck1vZGVsOiAoZmlsZV9jb250ZW50KSA8YnI-IHN1bW1hcml6ZV90ZXh0XG4gIFN1bW1hcml6ZXJNb2RlbC0tPj5sYW1iZGFfZmluZF9kb2N1bWVudDogcmV0dXJuIHN1bW1hcnlcbiAgbGFtYmRhX2ZpbmRfZG9jdW1lbnQtLT4-bGFtYmRhX2FsZXhfZmxvdzoge1N1bW1hcnl9IDxicj4gcmV0dXJuXG4gIGxhbWJkYV9hbGV4X2Zsb3ctLT4-TGV4OiBoZXJlIGlzIHRoZSBzdW1tYXJ5IC4uLiBcbiAgTGV4LS0-PlVzZXI6IGhlcmUgaXMgdGhlIHN1bW1hcnkgLi4uIFxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiB5b3UgZmluZCBhIGRvY3VtZW50XG4gIExleC0-PmxhbWJkYV9hbGV4X2Zsb3c6IEZpbmREb2N1bWVudEludGVudFxuICBsYW1iZGFfYWxleF9mbG93LT4-bGFtYmRhX2ZpbmRfZG9jdW1lbnQ6IHsgRGVzY3JpcHRpb246Jyd9XG4gIGxhbWJkYV9maW5kX2RvY3VtZW50LT4-S2VuZHJhOiBEZXNjcmlwdGlvbiA8YnI-IHNlYXJjaF9pbmRleFxuICBLZW5kcmEtLT4-bGFtYmRhX2ZpbmRfZG9jdW1lbnQ6IHJldHVybiBxdWVyeV9yZXN1bHRzXG4gIGxhbWJkYV9maW5kX2RvY3VtZW50LT4-U3VtbWFyaXplck1vZGVsOiAoZmlsZV9jb250ZW50KSA8YnI-IHN1bW1hcml6ZV90ZXh0XG4gIFN1bW1hcml6ZXJNb2RlbC0tPj5sYW1iZGFfZmluZF9kb2N1bWVudDogcmV0dXJuIHN1bW1hcnlcbiAgbGFtYmRhX2ZpbmRfZG9jdW1lbnQtLT4-bGFtYmRhX2FsZXhfZmxvdzoge1N1bW1hcnl9IDxicj4gcmV0dXJuXG4gIGxhbWJkYV9hbGV4X2Zsb3ctLT4-TGV4OiBoZXJlIGlzIHRoZSBzdW1tYXJ5IC4uLiBcbiAgTGV4LS0-PlVzZXI6IGhlcmUgaXMgdGhlIHN1bW1hcnkgLi4uIFxuIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)


### Ask question

[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiBJIGFzayB5b3UgYSBxdWVzdGlvblxuICBMZXgtPj5sYW1iZGFfYWxleF9mbG93OiBBc2tRdWVzdGlvbkludGVudFxuICBsYW1iZGFfYWxleF9mbG93LT4-bGFtYmRhX2Fza19xdWVzdGlvbjogeyBEZXNjcmlwdGlvbjonJ31cbiAgbGFtYmRhX2Fza19xdWVzdGlvbi0-PktlbmRyYTogRGVzY3JpcHRpb24gPGJyPiBzZWFyY2hfaW5kZXhcbiAgS2VuZHJhLS0-PmxhbWJkYV9hc2tfcXVlc3Rpb246IHJldHVybiBxdWVyeV9yZXN1bHRzXG4gIGxhbWJkYV9hc2tfcXVlc3Rpb24tLT4-bGFtYmRhX2Fza19xdWVzdGlvbjogZ2V0X2hpZ2hsaWdodHNfZnJvbV9rZW5kcmFcbiAgbGFtYmRhX2Fza19xdWVzdGlvbi0tPj5sYW1iZGFfYWxleF9mbG93OiB7SGlnaGxpZ2h0c30gPGJyPiByZXR1cm5cbiAgbGFtYmRhX2FsZXhfZmxvdy0tPj5MZXg6IEhlcmUgaXMgeW91ciBhbnN3ZXIgLi4uIFxuICBMZXgtLT4-VXNlcjogSGVyZSBpcyB5b3VyIGFuc3dlciAuLi4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gIFVzZXItPj5MZXg6IENhbiBJIGFzayB5b3UgYSBxdWVzdGlvblxuICBMZXgtPj5sYW1iZGFfYWxleF9mbG93OiBBc2tRdWVzdGlvbkludGVudFxuICBsYW1iZGFfYWxleF9mbG93LT4-bGFtYmRhX2Fza19xdWVzdGlvbjogeyBEZXNjcmlwdGlvbjonJ31cbiAgbGFtYmRhX2Fza19xdWVzdGlvbi0-PktlbmRyYTogRGVzY3JpcHRpb24gPGJyPiBzZWFyY2hfaW5kZXhcbiAgS2VuZHJhLS0-PmxhbWJkYV9hc2tfcXVlc3Rpb246IHJldHVybiBxdWVyeV9yZXN1bHRzXG4gIGxhbWJkYV9hc2tfcXVlc3Rpb24tLT4-bGFtYmRhX2Fza19xdWVzdGlvbjogZ2V0X2hpZ2hsaWdodHNfZnJvbV9rZW5kcmFcbiAgbGFtYmRhX2Fza19xdWVzdGlvbi0tPj5sYW1iZGFfYWxleF9mbG93OiB7SGlnaGxpZ2h0c30gPGJyPiByZXR1cm5cbiAgbGFtYmRhX2FsZXhfZmxvdy0tPj5MZXg6IEhlcmUgaXMgeW91ciBhbnN3ZXIgLi4uIFxuICBMZXgtLT4-VXNlcjogSGVyZSBpcyB5b3VyIGFuc3dlciAuLi4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)

# Inputs and Outputs

| Feature | Input | Output |
| :--: | :--: | :--: 
| Send passport|  [data-input/Passport.jpg](https://github.com/gzomer/alex-bot/blob/master/data-input/Passport.jpg) | ```{'ExpirationDate': '17/01/1985','BirthDate': '31/01/2016','PassportNumber': '107185703'}``` |
| Add task|  [data-input/wireframe.jpg](https://github.com/gzomer/alex-bot/blob/master/data-input/wireframe.jpg) | [data-output/wireframe.html](data-output/wireframe.html) |
| Add expense|  [data-input/expense.jpg](https://github.com/gzomer/alex-bot/blob/master/data-input/expense.jpg) | ```{'Price': '13.54', 'Location': 'Guildford', 'Store': 'Co-op'}``` |
| Open ticket| ```{'query':'My internet is not working'}``` and [this file](https://github.com/gzomer/alex-bot/blob/master/data-input/How%20to%20Troubleshoot%20Home%20WiFi%20and%20Router%20Issues%20_%20Guides.pdf) | ```{'Summary': 'Wait 2-5 minutes before plugging it back in.\n\n\n3. Wait 5 more minutes and retry the connection.\n\n\nIn most cases, this should x your issue and allow you to get back online. If you go through\nthese steps and something still isnt working, you may need to contact your internet\nservice provider for assistance.\n\n\nUnderstanding Your Routers Icons\n\n\nMost routers have a series of icons that illuminate to convey dierent status messages at a\nglance. Though these can vary from brand to brand, most manufacturers include at least\nthree primary status indicators:\n\n\nWiFi not working\n\n\nWiFi slowed down\n\n\nWiFi network disappearing\n\n\nDevices that wont connect to Wi\n\n\nGlobe icon: solid when modem is connected to the Internet.'}```|
| Find document| ```{'Description': 'Privacy policy'}``` and [this file](https://github.com/gzomer/alex-bot/blob/master/data-input/AmazonPrivacyPolicy.html)| ```{'Summary': 'We collect your personal information in order to provide and continually improve our products and services. What personal information about customers does amazon europe collect ?provide , troubleshoot , and improve amazon services.'}```|
| Ask question | ```{'Description': 'How many vacation weeks I have on my first year?'}``` and [this file](https://github.com/gzomer/alex-bot/blob/master/data-input/Paid%20Time%20Off%20for%20U.S.%20Amazon%20Employees_%20_%20Amazon.jobs.pdf) | ```{'Summary': "Amazon.\ncom's salaried employees earn two weeks of vacation time in their first year of employment and three weeks of vacation in their\nsecond year"}``` |

# Testing

There are three levels of testing you can follow, with increasing levels of difficulty.

You can test only the [Models](#models), test the [Use-cases](#use-cases) and test the [Full deployment](#deploying). 


### Models

If you just want just wand to test the deployment of the curated models and perform inference, follow the instructions at [this Jupyter notebook](https://github.com/gzomer/alex-bot/blob/master/Deploy%20Models%20and%20Perform%20Inference.ipynb).

### Use-cases

Now, if you want to test the use-cases, i.e. test the models integrated with the business logic and AWS services, use this [this Jupyter notebook](https://github.com/gzomer/alex-bot/blob/master/Features%20Testing.ipynb).

Please note that for this you will need to have deployed the models, and depending on the feature you want to test, you may need to configure S3 Buckets, Kendra index, and get a Trello API key/token.

# Deploying

As I said, doing a full deploy is not exactly easy 😅.

But bear with me and let's follow these steps:

1. [Config](#config)
2. [Deploying Models](#deploying-models)
2. [Deploying AWS services](#deploying-aws-services)
2. [Building Mobile App](#mobile-app)

## Config

1. Open the file `config.py`
2. Edit with the configurations from your AWS account

## Deploying Models

Run this command in the command line and wait (it will take some time to deploy all models): 

```python models_deploy.py```

Skip if you have already deployed the models with the Jupyter Notebook.

## Deploying AWS services

- [S3 Buckets](#s3-buckets)
- [Amazon Kendra](#amazon-kendra)
- [Lambda functions](#lambda-functions)
- [Amazon Lex Bot](#amazon-lex-bot)
- [Alexa Skill](#alexa-skill)
- [Configuring Permissions and IAM](#configuring-permissions-and-iam)

### S3 Buckets

1. Create a bucket for images and HTML files (Remember to replace the bucket in your `config.py` file)
2. Create a bucket to store the documents for Kendra

### Amazon Kendra

I'm not going to explain in details how to deploy a **Kendra** index because AWS docs does a good job on this.

You need to follow two steps:

1. [Configure prerequisites](https://docs.aws.amazon.com/kendra/latest/dg/gs-prerequisites.html)
2. [Create index](https://docs.aws.amazon.com/kendra/latest/dg/gs-console.html)

You just need to make sure you use the bucket you have created above as the datasource for the **Kendra** index.

### Lambda functions

Now it is time to create our Lambda functions.

It is very simple to create a Lambda function via the console, you can follow this [tutorial](https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html).

You will need to create seven functions, namely:

1. [alex_flow](https://github.com/gzomer/alex-bot/blob/master/lambda_alex_flow.py)
2. [ask_question](https://github.com/gzomer/alex-bot/blob/master/lambda_ask_question.py)
3. [find_document](https://github.com/gzomer/alex-bot/blob/master/lambda_find_document.py)
4. [add_task](https://github.com/gzomer/alex-bot/blob/master/lambda_add_task.py)
5. [open_ticket](https://github.com/gzomer/alex-bot/blob/master/lambda_open_ticket.py)
6. [send_passport](https://github.com/gzomer/alex-bot/blob/master/lambda_send_passport.py)
7. [upload_file](https://github.com/gzomer/alex-bot/blob/master/lambda_upload_file.py)

Click on the links above to copy the source code for the Lambda function and paste at the Lambda configuration. All of them use Python 3.6 engine. 

**Important** You will need to configure the timeout for at least 60 seconds, or otherwise the functions will fail. This is because some of the models are slow to perform inference.

### Amazon Lex Bot

1. Go to the [Amazon Lex](https://us-east-1.console.aws.amazon.com/lex/home?region=us-east-1#bots:) service page in AWS Console 
2. Open the file [intent_config_lex.json](https://github.com/gzomer/alex-bot/blob/master/intent_config_lex.json) and replace all instances of {AWS_ACCOUNT_ID} with your AWS account id
2. Click import and select the file [intent_config_lex.json](https://github.com/gzomer/alex-bot/blob/master/intent_config_lex.json) (you will actually need to zip it first)
3. Click Build and then Publish
3. Done! Your bot is created

### Alexa Skill

#### Creating Lambda

We need to create a Lambda to handle the requests from Alexa. For this we are going to use the starting application from AWS Serverless repository because it already creates the necessary Alexa Skill trigger for us, and we just need to update the Lambda code.

1. Go to the same page that you used to create a Lambda function
2. Choose Browse serverless app repository
3. Type alexa-skills-kit-python36-facts-skill and select the app
4. Change the application name to alex-alexa-skill
5. Change the Lambda name to alex-alexa-skill
6. Click Deploy
7. Now select the Lambda function and paste [this code](https://github.com/gzomer/alex-bot/blob/master/lambda_alexa.py)
8. Click save

**Important** You will need to configure the timeout for at least 60 seconds

#### Creating Bot

1. Go to the [Alexa](https://developer.amazon.com/alexa/console/ask) developer dashboard
2. Select Create Skill
3. Choose Custom and provision your own
4. Select Start from scratch
5. Click JSON Editor and drag and drop this [file](https://github.com/gzomer/alex-bot/blob/master/intent_config_alexa.json) into the editor
7. Go to Endpoint and copy and paste the ARN of your application from the previous step
6. Click Save model and Build model

### Configuring permissions and IAM

First, let's create a custom Policy named **InvokeLambda**. This is needed because we need to allow Lambda functions to call other Lambda functions (such as `lambda_alex_flow.py`).

Go to [this link](https://console.aws.amazon.com/iam/home?#/policies) to create the policy and add `InvokeAsync` and `InvokeFunction` actions.

#### Adding policies to Lambda's roles

Now we need to attach a number of policies to each Lambda role. You can find attach politices to roles at this [link](https://console.aws.amazon.com/iam/home?#/roles).

1. alex_flow
	* InvokeLambda 
2. ask_question
	* AmazonSageMakerFullAccess
	*  AmazonKendraFullAccess
3. find_document
	* AmazonSageMakerFullAccess
	* AmazonKendraFullAccess
	* AmazonS3FullAccess
	* InvokeLambda
4. add_task
	* AmazonSageMakerFullAccess
	* AmazonS3FullAccess
5. open_ticket
	* AmazonKendraFullAccess
	* AmazonSageMakerFullAccess
6. send_passport
	* AmazonSageMakerFullAccess
7. upload_file
	* AmazonS3FullAccess

You should also add InvokeLambda to the role for your Alexa Skill app, which should be named something like
serverlessrepo-alexa-skil-(....)

### Mobile App

There are two projects for the mobile app, the cordova wrapper and the Lex Bot UI (which was based on [this project](https://github.com/aws-samples/aws-lex-web-ui) from Amazon)

#### Lex bot UI

First, you need create a Cognito pool ID and add the Lex policy.

Next, open those three files:

- lex-ui/src/config.dev.json
- lex-ui/src/config.prod.json
- lex-ui/src/store/action.js

And replace `{YOUR_API_GATEWAY_TO_UPLOAD_FILE_LAMBDA}` for `https://{YOU_ENDPOINT}.execute-api.us-east-1.amazonaws.com/Production/upload_file`

Also replace `YOUR_COGNITO_POOL_ID` with the Cognito pool ID you have created above.

1. `npm install`
2. `npm run build`
3. `python move_files.py` (this is necessary to copy the built UI to the cordova Wrapper)



#### Cordova App

1. Install Ionic `npm install -g ionic`
2. Install Cordova `npm install -g cordova`
3. Run `ionic cap add ios`
4. Run `ionic build`
5. Run `ionic cap copy ios`
5. Run `ionic cap sync ios`
6. Run `ionic cap open ios` and now you can deploy the app to your device using Xcode


# Thank you!

Congratulations for reaching this far 🙏

![](https://staffino.com/blog/wp-content/uploads/2016/09/59349318.jpg)