# API Reference — Sports Recruitment Platform


---

## Health

### `GET /health`

**Response**
```json
{"status": "ok"}
```

---

## Auth

### `POST /auth/register`

Register a new athlete or sports organization.

**Request body**
```json
{
  "email": "athlete@example.com",
  "password": "secret123",
  "role": "ATHLETE",
  "first_name": "John",
  "last_name": "Doe",
  "sport": "Football",
  "position": "Forward",
  "nationality": "Morocco",
  "birth_date": "2000-05-15",
  "photo": null
}
```

For an organization:
```json
{
  "email": "club@example.com",
  "password": "secret123",
  "role": "ORGANIZATION",
  "organization_name": "EMSI Club",
  "organization_type": "club",
  "country": "Morocco",
  "city": "Casablanca",
  "description": "A great sports club",
  "logo": null
}
```

**Response** `200 OK`
```json
{
  "id": 1,
  "email": "athlete@example.com",
  "role": "ATHLETE",
  "token": "generated-auth-token"
}
```

---

### `POST /auth/login`

**Request body**
```json
{
  "email": "athlete@example.com",
  "password": "secret123"
}
```

**Response** `200 OK`
```json
{
  "id": 1,
  "email": "athlete@example.com",
  "role": "ATHLETE",
  "token": "generated-auth-token"
}
```

---

## Users

### `GET /users/`

List all users (athletes + organizations).

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "email": "athlete@example.com",
    "role": "ATHLETE",
    "is_active": true
  },
  {
    "id": 2,
    "email": "club@example.com",
    "role": "ORGANIZATION",
    "is_active": true
  }
]
```

---

### `GET /users/{user_id}`

**Response** `200 OK`
```json
{
  "id": 1,
  "email": "athlete@example.com",
  "role": "ATHLETE",
  "is_active": true
}
```

**Response** `404 Not Found`
```json
{"detail": "User not found"}
```

---

### `PUT /users/{user_id}`

**Request body**
```json
{
  "email": "newemail@example.com",
  "password": "newpassword"
}
```

**Response** `200 OK`
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "role": "ATHLETE",
  "is_active": true
}
```

---

### `DELETE /users/{user_id}`

**Response** `204 No Content` (no body)

---

## Athletes

### `GET /athletes/`

List all athlete profiles.

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "email": "athlete@example.com",
    "is_active": true,
    "first_name": "John",
    "last_name": "Doe",
    "sport": "Football",
    "position": "Forward",
    "nationality": "Morocco",
    "birth_date": "2000-05-15",
    "photo": null
  }
]
```

---

### `GET /athletes/{profile_id}`

**Response** `200 OK`
```json
{
  "id": 1,
  "email": "athlete@example.com",
  "is_active": true,
  "first_name": "John",
  "last_name": "Doe",
  "sport": "Football",
  "position": "Forward",
  "nationality": "Morocco",
  "birth_date": "2000-05-15",
  "photo": null
}
```

---

### `PUT /athletes/{profile_id}`

**Request body** (all fields optional)
```json
{
  "first_name": "Jane",
  "position": "Midfielder"
}
```

**Response** `200 OK`
```json
{
  "id": 1,
  "email": "athlete@example.com",
  "is_active": true,
  "first_name": "Jane",
  "last_name": "Doe",
  "sport": "Football",
  "position": "Midfielder",
  "nationality": "Morocco",
  "birth_date": "2000-05-15",
  "photo": null
}
```

---

### `DELETE /athletes/{profile_id}`

**Response** `204 No Content`

---

### `POST /athletes/{profile_id}/photo`

Upload the athlete's photo. Send as `multipart/form-data` with a file field named `file`.

Allowed formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif` — max 5 MB.

**Response** `200 OK` (returns updated athlete profile with `photo` URL)
```json
{
  "id": 1,
  "email": "athlete@example.com",
  "is_active": true,
  "first_name": "John",
  "last_name": "Doe",
  "sport": "Football",
  "position": "Forward",
  "nationality": "Morocco",
  "birth_date": "2000-05-15",
  "photo": "https://...supabase.co/storage/v1/object/public/uploads/athlete_1_abc123.jpg"
}
```

---

## Organizations

### `GET /organizations/`

List all sports organizations.

**Response** `200 OK`
```json
[
  {
    "id": 2,
    "email": "club@example.com",
    "is_active": true,
    "organization_name": "EMSI Club",
    "organization_type": "club",
    "country": "Morocco",
    "city": "Casablanca",
    "description": "A great sports club",
    "logo": null
  }
]
```

---

### `GET /organizations/{org_id}`

**Response** `200 OK`
```json
{
  "id": 2,
  "email": "club@example.com",
  "is_active": true,
  "organization_name": "EMSI Club",
  "organization_type": "club",
  "country": "Morocco",
  "city": "Casablanca",
  "description": "A great sports club",
  "logo": null
}
```

---

### `PUT /organizations/{org_id}`

**Request body** (all fields optional)
```json
{
  "organization_name": "EMSI Club Updated",
  "description": "Updated description"
}
```

**Response** `200 OK`
```json
{
  "id": 2,
  "email": "club@example.com",
  "is_active": true,
  "organization_name": "EMSI Club Updated",
  "organization_type": "club",
  "country": "Morocco",
  "city": "Casablanca",
  "description": "Updated description",
  "logo": null
}
```

---

### `DELETE /organizations/{org_id}`

**Response** `204 No Content`

---

### `POST /organizations/{org_id}/logo`

Upload the organization's logo. Send as `multipart/form-data` with a file field named `file`.

Allowed formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif` — max 5 MB.

**Response** `200 OK`
```json
{
  "id": 2,
  "email": "club@example.com",
  "is_active": true,
  "organization_name": "EMSI Club",
  "organization_type": "club",
  "country": "Morocco",
  "city": "Casablanca",
  "description": "A great sports club",
  "logo": "https://...supabase.co/storage/v1/object/public/uploads/org_2_abc123.png"
}
```

---

## Diplomas

### `POST /diplomas/`

**Request body**
```json
{
  "athlete_id": 1,
  "title": "Bachelor in Sports Science",
  "institution": "University of Casablanca",
  "year": 2022,
  "is_certification": false
}
```

**Response** `201 Created`
```json
{
  "id": 1,
  "athlete_id": 1,
  "title": "Bachelor in Sports Science",
  "institution": "University of Casablanca",
  "year": 2022,
  "is_certification": false
}
```

---

### `GET /diplomas/`

Filter by athlete (optional):
```
GET /diplomas/?athlete_id=1
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "athlete_id": 1,
    "title": "Bachelor in Sports Science",
    "institution": "University of Casablanca",
    "year": 2022,
    "is_certification": false
  }
]
```

---

### `PUT /diplomas/{diploma_id}`

**Request body** (all fields optional)
```json
{
  "title": "Master in Sports Science",
  "year": 2024
}
```

**Response** `200 OK`
```json
{
  "id": 1,
  "athlete_id": 1,
  "title": "Master in Sports Science",
  "institution": "University of Casablanca",
  "year": 2024,
  "is_certification": false
}
```

---

### `DELETE /diplomas/{diploma_id}`

**Response** `204 No Content`

---

## Experiences

### `POST /experiences/`

**Request body**
```json
{
  "athlete_id": 1,
  "position": "Forward",
  "organization": "Raja Casablanca",
  "start_date": "2020-09-01",
  "end_date": "2023-06-30",
  "description": "Played as a forward for Raja Casablanca"
}
```

**Response** `201 Created`
```json
{
  "id": 1,
  "athlete_id": 1,
  "position": "Forward",
  "organization": "Raja Casablanca",
  "start_date": "2020-09-01",
  "end_date": "2023-06-30",
  "description": "Played as a forward for Raja Casablanca"
}
```

---

### `GET /experiences/`

Filter by athlete (optional):
```
GET /experiences/?athlete_id=1
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "athlete_id": 1,
    "position": "Forward",
    "organization": "Raja Casablanca",
    "start_date": "2020-09-01",
    "end_date": "2023-06-30",
    "description": "Played as a forward for Raja Casablanca"
  }
]
```

---

### `PUT /experiences/{experience_id}`

**Request body** (all fields optional)
```json
{
  "position": "Striker",
  "end_date": "2024-01-15"
}
```

**Response** `200 OK`
```json
{
  "id": 1,
  "athlete_id": 1,
  "position": "Striker",
  "organization": "Raja Casablanca",
  "start_date": "2020-09-01",
  "end_date": "2024-01-15",
  "description": "Played as a forward for Raja Casablanca"
}
```

---

### `DELETE /experiences/{experience_id}`

**Response** `204 No Content`

---

## Offers

### `POST /offers/`

**Request body**
```json
{
  "organization_id": 2,
  "title": "Football Player Wanted",
  "description": "We are looking for a talented forward",
  "sport": "Football",
  "contract_type": "Full-time",
  "location": "Casablanca",
  "expiration_date": "2026-12-31"
}
```

**Response** `201 Created`
```json
{
  "id": 1,
  "organization_id": 2,
  "title": "Football Player Wanted",
  "description": "We are looking for a talented forward",
  "sport": "Football",
  "contract_type": "Full-time",
  "location": "Casablanca",
  "publication_date": "2026-06-22T12:00:00Z",
  "expiration_date": "2026-12-31",
  "status": "ACTIVE"
}
```

---

### `GET /offers/`

Filter by sport (optional):
```
GET /offers/?sport=Football
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "organization_id": 2,
    "title": "Football Player Wanted",
    "description": "We are looking for a talented forward",
    "sport": "Football",
    "contract_type": "Full-time",
    "location": "Casablanca",
    "publication_date": "2026-06-22T12:00:00Z",
    "expiration_date": "2026-12-31",
    "status": "ACTIVE"
  }
]
```

---

### `GET /offers/{offer_id}`

**Response** `200 OK`
```json
{
  "id": 1,
  "organization_id": 2,
  "title": "Football Player Wanted",
  "description": "We are looking for a talented forward",
  "sport": "Football",
  "contract_type": "Full-time",
  "location": "Casablanca",
  "publication_date": "2026-06-22T12:00:00Z",
  "expiration_date": "2026-12-31",
  "status": "ACTIVE"
}
```

---

### `PUT /offers/{offer_id}`

**Request body** (all fields optional)
```json
{
  "title": "Updated Title",
  "status": "CLOSED"
}
```

**Response** `200 OK`
```json
{
  "id": 1,
  "organization_id": 2,
  "title": "Updated Title",
  "description": "We are looking for a talented forward",
  "sport": "Football",
  "contract_type": "Full-time",
  "location": "Casablanca",
  "publication_date": "2026-06-22T12:00:00Z",
  "expiration_date": "2026-12-31",
  "status": "CLOSED"
}
```

---

### `DELETE /offers/{offer_id}`

**Response** `204 No Content`

---

## Applications

### `POST /applications/`

**Request body**
```json
{
  "athlete_id": 1,
  "offer_id": 1,
  "motivation_letter": "I am very interested in this position"
}
```

**Response** `201 Created`
```json
{
  "id": 1,
  "athlete_id": 1,
  "offer_id": 1,
  "application_date": "2026-06-22T12:00:00Z",
  "status": "PENDING",
  "cv": null,
  "motivation_letter": "I am very interested in this position"
}
```

---

### `GET /applications/`

Filter by athlete or offer:
```
GET /applications/?athlete_id=1
GET /applications/?offer_id=1
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "athlete_id": 1,
    "offer_id": 1,
    "application_date": "2026-06-22T12:00:00Z",
    "status": "PENDING",
    "cv": null,
    "motivation_letter": "I am very interested in this position"
  }
]
```

---

### `PUT /applications/{application_id}/accept`

**Response** `200 OK`
```json
{
  "id": 1,
  "athlete_id": 1,
  "offer_id": 1,
  "application_date": "2026-06-22T12:00:00Z",
  "status": "ACCEPTED",
  "cv": null,
  "motivation_letter": "I am very interested in this position"
}
```

---

### `PUT /applications/{application_id}/reject`

**Response** `200 OK`
```json
{
  "id": 1,
  "athlete_id": 1,
  "offer_id": 1,
  "application_date": "2026-06-22T12:00:00Z",
  "status": "REJECTED",
  "cv": null,
  "motivation_letter": "I am very interested in this position"
}
```

---

### `POST /applications/{application_id}/cv`

Upload a CV. Send as `multipart/form-data` with a file field named `file`.

Allowed formats: `.pdf`, `.doc`, `.docx` — max 5 MB.

**Response** `200 OK`
```json
{
  "id": 1,
  "athlete_id": 1,
  "offer_id": 1,
  "application_date": "2026-06-22T12:00:00Z",
  "status": "PENDING",
  "cv": "https://...supabase.co/storage/v1/object/public/uploads/cv_1_abc123.pdf",
  "motivation_letter": "I am very interested in this position"
}
```

---

## Messages

### `POST /messages/`

**Request body**
```json
{
  "sender_id": 1,
  "sender_type": "athlete",
  "receiver_id": 2,
  "receiver_type": "organization",
  "content": "Hello, I am interested in your offer"
}
```

**Response** `201 Created`
```json
{
  "id": 1,
  "direction": "sent",
  "other": {
    "id": 2,
    "type": "organization",
    "email": "club@example.com",
    "name": "EMSI Club",
    "photo": null
  },
  "content": "Hello, I am interested in your offer",
  "sent_date": "2026-06-22T12:00:00Z"
}
```

---

### `GET /messages/`

Get all messages for a user. Optional explicit role (otherwise auto-detected):
```
GET /messages/?user_id=1
GET /messages/?user_id=1&user_role=athlete
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "direction": "sent",
    "other": {
      "id": 2,
      "type": "organization",
      "email": "club@example.com",
      "name": "EMSI Club",
      "photo": null
    },
    "content": "Hello, I am interested in your offer",
    "sent_date": "2026-06-22T12:00:00Z"
  },
  {
    "id": 2,
    "direction": "received",
    "other": {
      "id": 2,
      "type": "organization",
      "email": "club@example.com",
      "name": "EMSI Club",
      "photo": null
    },
    "content": "Great! Please apply through the platform.",
    "sent_date": "2026-06-22T12:05:00Z"
  }
]
```

---

### `GET /messages/conversation/{other_user_id}`

Get the conversation between the current user and another user:
```
GET /messages/conversation/2?user_id=1
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "direction": "sent",
    "other": {
      "id": 2,
      "type": "organization",
      "email": "club@example.com",
      "name": "EMSI Club",
      "photo": null
    },
    "content": "Hello, I am interested in your offer",
    "sent_date": "2026-06-22T12:00:00Z"
  },
  {
    "id": 2,
    "direction": "received",
    "other": {
      "id": 2,
      "type": "organization",
      "email": "club@example.com",
      "name": "EMSI Club",
      "photo": null
    },
    "content": "Great! Please apply through the platform.",
    "sent_date": "2026-06-22T12:05:00Z"
  }
]
```

---

## Summary of All Endpoints

| Method | Path | Status | Description |
|--------|------|--------|-------------|
| GET | `/health` | 200 | Health check |
| POST | `/auth/register` | 200 | Register a user |
| POST | `/auth/login` | 200 | Login |
| GET | `/users/` | 200 | List all users |
| GET | `/users/{id}` | 200 | Get a user |
| PUT | `/users/{id}` | 200 | Update a user |
| DELETE | `/users/{id}` | 204 | Delete a user |
| GET | `/athletes/` | 200 | List athletes |
| GET | `/athletes/{id}` | 200 | Get athlete profile |
| PUT | `/athletes/{id}` | 200 | Update athlete |
| DELETE | `/athletes/{id}` | 204 | Delete athlete |
| POST | `/athletes/{id}/photo` | 200 | Upload photo |
| GET | `/organizations/` | 200 | List organizations |
| GET | `/organizations/{id}` | 200 | Get organization |
| PUT | `/organizations/{id}` | 200 | Update organization |
| DELETE | `/organizations/{id}` | 204 | Delete organization |
| POST | `/organizations/{id}/logo` | 200 | Upload logo |
| POST | `/diplomas/` | 201 | Create diploma |
| GET | `/diplomas/` | 200 | List diplomas |
| PUT | `/diplomas/{id}` | 200 | Update diploma |
| DELETE | `/diplomas/{id}` | 204 | Delete diploma |
| POST | `/experiences/` | 201 | Create experience |
| GET | `/experiences/` | 200 | List experiences |
| PUT | `/experiences/{id}` | 200 | Update experience |
| DELETE | `/experiences/{id}` | 204 | Delete experience |
| POST | `/offers/` | 201 | Create offer |
| GET | `/offers/` | 200 | List offers |
| GET | `/offers/{id}` | 200 | Get offer |
| PUT | `/offers/{id}` | 200 | Update offer |
| DELETE | `/offers/{id}` | 204 | Delete offer |
| POST | `/applications/` | 201 | Create application |
| GET | `/applications/` | 200 | List applications |
| PUT | `/applications/{id}/accept` | 200 | Accept application |
| PUT | `/applications/{id}/reject` | 200 | Reject application |
| POST | `/applications/{id}/cv` | 200 | Upload CV |
| POST | `/messages/` | 201 | Send message |
| GET | `/messages/` | 200 | List user messages |
| GET | `/messages/conversation/{id}` | 200 | Get conversation |
