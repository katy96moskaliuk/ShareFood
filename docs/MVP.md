from pathlib import Path

content = r"""# MVP Project “ShareFood”

## Project Idea

A platform where people can give away food with a good expiration date for free to those who need it.  
An OLIO-like platform, but as a simple local MVP.

# MVP Goal

To validate:

- whether people are willing to post food listings;
- whether other users are willing to collect the food;
- how convenient the interaction is.

# Main Roles

## 1. Guest

Can:

- browse listings;
- search for food;
- register an account.

## 2. User

Can:

- create listings;
- edit listings;
- delete listings;
- reserve food items;
- message other users;
- view their profile/dashboard.

# Core MVP Features

# 1. Home Page

Sections:

- Hero section
- How the service works
- Latest listings
- “Create Listing” button

CTA buttons:

- “Browse Listings”
- “Share Food”

# 2. Registration and Login

## Registration:

- name;
- email;
- password.

## Login:

- email;
- password.

# 3. Listings Feed

## Listing Card Contains:

- photo;
- title;
- description;
- district/area;
- expiration date;
- “I’ll Take It” button.

## Filters:

- search;
- district/area;
- category.

# 4. Create Listing

## Fields:

- title;
- description;
- photo;
- expiration date;
- address/district;
- category.

# Allowed Food Categories

- Fruits
- Vegetables
- Grains & Pasta
- Canned Food
- Drinks
- Sweets

# Prohibited Categories

- Dairy products
- Meat
- Fish
- Homemade food
- alcoholic drinks

# 5. Listing Page

Contains:

- large photo;
- description;
- map/district;
- contact section;
- “Contact User” button.

# 6. User Dashboard

The user can see:

- their listings;
- reserved food items;
- listing statuses.

# 7. Messaging System

## MVP Solution

A simple built-in chat inside the platform.

## Benefits:

- no need to share phone numbers;
- safer communication;
- users stay inside the platform;
- moderation can be added later.

## Safety

Do not display:

- exact address;
- phone number;
- personal information.

Display only:

- district/area;
- approximate location.

The exact address is shared later in the chat.
"""
