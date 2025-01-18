
# Data Website Project



## Table of Contents

1. [Overview](#overview)
   - [Key Features](#key-features)
2. [Learning Objectives](#learning-objectives)
3. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Setup Instructions](#setup-instructions)
4. [Features Breakdown](#features-breakdown)
   - [Dataset Display](#1-dataset-display)
   - [Dynamic Visualizations](#2-dynamic-visualizations)
   - [Email Subscription](#3-email-subscription)
   - [A/B Tested Donation Page](#4-ab-tested-donation-page)
5. [File Structure](#file-structure)
6. [Example Usage](#example-usage)
   - [Home Page](#home-page)
   - [Browse Data](#browse-data)
   - [Visualizations](#visualizations)
   - [Email Subscription](#email-subscription)
   - [Donations](#donations)
7. [Future Enhancements](#future-enhancements)
8. [Acknowledgments](#acknowledgments)
9. [License](#license)

## Overview

This project is a **Data Website** built using **Python** and **Flask** to showcase and share datasets with dynamic visualizations. The application allows users to interact with the dataset through various features, such as viewing raw data, exploring visualizations, subscribing for updates, and contributing via a donation page optimized with A/B testing.

### Key Features

1.  **Data Display**
    -   A page that displays the dataset in both JSON and HTML table formats.
    -   Rate-limited JSON API for secure data access.
2.  **Dynamic Data Visualizations**
    -   Interactive SVG visualizations using Matplotlib.
    -   Supports query strings for generating dynamic plots.
3.  **Email Subscription**
    -   Email subscription with validation using regular expressions.
    -   Subscribers are stored securely and assigned unique IDs.
4.  **A/B Testing for Donations**
    -   Two homepage versions tested for optimal donation conversions.
    -   Tracks user interactions to determine the better-performing design.

----------

## Learning Objectives

This project highlights:

-   Building a web application using Flask.
-   Creating interactive and meaningful data visualizations.
-   Implementing regular expressions for email validation.
-   Performing A/B testing to optimize user interactions.
-   Designing secure APIs with rate-limiting capabilities.

----------

## Installation

### Prerequisites

-   Python 3.x installed.
-   Required Python libraries: Flask, Matplotlib, Pandas, BeautifulSoup4, lxml.

### Setup Instructions

1.  Clone the repository:
    
    ```bash
    git clone https://github.com/SrujayReddy/Data-Website-Project.git
    cd data-website
    
    ```
    
2.  Install dependencies:
    
    ```bash
    pip install Flask lxml html5lib beautifulsoup4 matplotlib pandas
    
    ```
    
3.  Run the application:
    
    ```bash
    python main.py
    
    ```
    
4.  Open your browser and navigate to `http://127.0.0.1:5000` to access the website.

----------

## Features Breakdown

### 1. Dataset Display

-   **HTML Table**: Displays the dataset (`main.csv`) in an HTML table on the `browse.html` page.
-   **JSON API**: Provides dataset access in JSON format at `/browse.json` with rate-limiting to prevent abuse.

### 2. Dynamic Visualizations

-   SVG plots generated using Matplotlib.
-   Supports query strings for customizable plots (e.g., `/dashboard1.svg?bins=20`).
-   Dashboard includes multiple distinct plots providing insights into the dataset.

### 3. Email Subscription

-   Validates email addresses using a regular expression.
-   Stores email addresses in `emails.txt` and assigns unique subscriber IDs.
-   Uses JavaScript for seamless form submission and user feedback.

### 4. A/B Tested Donation Page

-   Two versions of the homepage alternate for the first 10 visits.
-   Tracks donation clicks to determine the better-performing design.

----------

## File Structure

```
Data-Website-Project/
├── main.py                 # Flask application code
├── main.csv                # Dataset used for the website
├── static/
│   ├── dashboard1.svg      # First static visualization
│   ├── dashboard1-query.svg # Visualization with query parameters
│   ├── dashboard2.svg      # Second static visualization
├── templates/
│   ├── index.html          # Homepage (A/B tested versions embedded)
│   ├── browse.html         # Data browsing page
│   ├── donate.html         # Donation page
├── emails.txt              # Stores email subscribers
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── tester.py               # Tester script for project validation

```

----------

## Example Usage

### Home Page

Visit the homepage at `http://127.0.0.1:5000/` to:

-   View dynamic visualizations.
-   Navigate to the dataset and donation pages.

### Browse Data

-   Access the dataset in an HTML table at `/browse.html`.
-   Retrieve the dataset as JSON at `/browse.json`. Note: Rate-limited to one request per minute per IP.

### Visualizations

-   View visualizations at `/dashboard1.svg` and `/dashboard2.svg`.
-   Generate dynamic plots with query strings (e.g., `/dashboard1.svg?bins=30`).

### Email Subscription

-   Click the **Subscribe** button on the homepage to register your email.
-   Submissions are validated and stored securely.

### Donations

-   Explore the donation page at `/donate.html`.
-   Homepage versions alternate for A/B testing to optimize donations.

----------

## Future Enhancements

-   Add authentication for managing subscriptions.
-   Enable more interactive visualizations (e.g., D3.js or Plotly).
-   Extend A/B testing to other pages and features.

----------

## Acknowledgments

This project was developed as part of a machine project for CS 320 at the University of Wisconsin–Madison. Special thanks to the teaching staff for guidance and support.

----------

## License

This project was developed as part of the **CS 320: Introduction to Software Engineering** course at the University of Wisconsin–Madison. It is shared strictly for educational and learning purposes only.

**Important Notes:**

-   Redistribution or reuse of this code for academic submissions is prohibited and may violate academic integrity policies.
-   The project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Any usage outside academic purposes must include proper attribution.