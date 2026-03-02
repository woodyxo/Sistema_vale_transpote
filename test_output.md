### 1. POST (Create) - /api/users/
```json
{
  "id": "bee008b6-d27a-4d6f-80dc-40365a0d6279",
  "name": "Maria Silva Teste",
  "email": "maria_32345678901@example.com",
  "cpf": "32345678901",
  "status": "none",
  "active": true
}
```

### 2. GET (List All) - /api/users/
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "4ebb7d97-e94e-4409-b38d-5642ee8406a2",
      "name": "Hudson dos santos",
      "email": "woodydead@yahoo.com",
      "cpf": "03454676207",
      "status": "approved",
      "active": true,
      "created_at": "2026-03-02T17:00:56.207226-04:00",
      "modified_at": "2026-03-02T17:00:56.207315-04:00"
    },
    {
      "id": "bee008b6-d27a-4d6f-80dc-40365a0d6279",
      "name": "Maria Silva Teste",
      "email": "maria_32345678901@example.com",
      "cpf": "32345678901",
      "status": "none",
      "active": true,
      "created_at": "2026-03-02T19:47:24.273377-04:00",
      "modified_at": "2026-03-02T19:47:24.273533-04:00"
    },
    {
      "id": "88a49504-7876-4194-aba2-f49df3ec2242",
      "name": "Maria Silva de Souza",
      "email": "maria@example.com",
      "cpf": "12345678901",
      "status": "none",
      "active": true,
      "created_at": "2026-03-02T19:46:16.043040-04:00",
      "modified_at": "2026-03-02T19:46:16.128655-04:00"
    }
  ]
}
```

### 3. GET (Details) - /api/users/bee008b6-d27a-4d6f-80dc-40365a0d6279/
```json
{
  "id": "bee008b6-d27a-4d6f-80dc-40365a0d6279",
  "name": "Maria Silva Teste",
  "email": "maria_32345678901@example.com",
  "cpf": "32345678901",
  "status": "none",
  "active": true,
  "created_at": "2026-03-02T19:47:24.273377-04:00",
  "modified_at": "2026-03-02T19:47:24.273533-04:00"
}
```

### 4. PATCH (Update Partial) - /api/users/bee008b6-d27a-4d6f-80dc-40365a0d6279/
```json
{
  "id": "bee008b6-d27a-4d6f-80dc-40365a0d6279",
  "name": "Maria Silva de Souza",
  "email": "maria_32345678901@example.com",
  "cpf": "32345678901",
  "status": "none",
  "active": true
}
```

### 5. DELETE - /api/users/bee008b6-d27a-4d6f-80dc-40365a0d6279/
```text
Status 204
No Content
```

### 6. GET (List After Delete) - /api/users/
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "4ebb7d97-e94e-4409-b38d-5642ee8406a2",
      "name": "Hudson dos santos",
      "email": "woodydead@yahoo.com",
      "cpf": "03454676207",
      "status": "approved",
      "active": true,
      "created_at": "2026-03-02T17:00:56.207226-04:00",
      "modified_at": "2026-03-02T17:00:56.207315-04:00"
    },
    {
      "id": "88a49504-7876-4194-aba2-f49df3ec2242",
      "name": "Maria Silva de Souza",
      "email": "maria@example.com",
      "cpf": "12345678901",
      "status": "none",
      "active": true,
      "created_at": "2026-03-02T19:46:16.043040-04:00",
      "modified_at": "2026-03-02T19:46:16.128655-04:00"
    },
    {
      "id": "bee008b6-d27a-4d6f-80dc-40365a0d6279",
      "name": "Maria Silva de Souza",
      "email": "maria_32345678901@example.com",
      "cpf": "32345678901",
      "status": "none",
      "active": false,
      "created_at": "2026-03-02T19:47:24.273377-04:00",
      "modified_at": "2026-03-02T19:47:24.395128-04:00"
    }
  ]
}
```
