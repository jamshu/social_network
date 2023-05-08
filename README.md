# Social Networking Application API

This project is a simple social networking application API built with Django and Django Rest Framework. It allows users to search for other users, send friend requests, accept or reject friend requests, and view their friends list and pending friend requests.

## Features

- User authentication (login and signup)
- Search users by email and name
- Send, accept, and reject friend requests
- List friends
- List pending friend requests
- Throttle on friend requests (max 3 requests per minute)

## Requirements

- Docker
- docker-compose

## Installation

1. Clone the repository:

```bash 
$ git clone git@github.com:jamshu/social_network.git
$ cd social-network
```
2. Build and run the Docker containers:
```bash 
$ docker-compose build
$ docker-compose up
```
The API should now be accessible at http://localhost:8000.

API Endpoints
- /api/user/signup/: create users 
- /api/user/login/: Login User
- /api/user/search/?search=abc: Search users by email or name (authenticated users only)
- /api/user/send-friend-request/:  create friend requests (authenticated users only)
- /api/user/list-pending-friend-requests/: list of Friend request to the logined user(authenticated users only)
- /api/user/list-friends/: list of Friend (authenticated users only)
- /api/user/accept-friend-request/{id}/ : Accept Friend Request
- /api/user/reject-friend-request/{id}/ : Reject Friend Request
