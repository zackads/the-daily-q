# The Daily Q

Email a random maths question every morning.

## Pre-requisites

- [Python](https://www.python.org/) 3.10+
- [node](https://nodejs.org/en/) (for AWS CDK)

## Setup

```bash
$ npm install -g aws-cdk
$ pip install -r requirements.txt
```

## Deploy

```bash
$ cd infrastructure
$ cdk bootstrap && cdk deploy
```

## FAQ

### Where are the questions from?

- [A-level questions](https://www.physicsandmathstutor.com)
- [STEP assignments](https://maths.org/step/)

### How hard are the questions?

I created this to help with UK A-level maths revision, so advanced pre-university. Calculus features. Check out the [syllabus](https://qualifications.pearson.com/content/dam/pdf/A%20Level/Mathematics/2017/specification-and-sample-assesment/a-level-l3-mathematics-specification-issue4.pdf).
