import urllib.request
import urllib.error
import json
import traceback

base_url = "http://127.0.0.1:8000/api/users/"
outputs = []

def print_section(title, data):
    if isinstance(data, (dict, list)):
        outputs.append(f"### {title}\n```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```\n")
    else:
        outputs.append(f"### {title}\n```text\n{data}\n```\n")

try:
    # 1. POST (Create)
    req = urllib.request.Request(base_url, method="POST")
    req.add_header("Content-Type", "application/json")
    # Using a random cpf to prevent unique constraint failures on multiple runs
    import random
    cpf = f"{random.randint(100,999)}45678901"
    
    data = json.dumps({
        "name": "Maria Silva Teste",
        "email": f"maria_{cpf}@example.com",
        "password": "senha_segura",
        "cpf": cpf
    }).encode('utf-8')

    try:
        with urllib.request.urlopen(req, data=data) as response:
            res_data = json.loads(response.read())
            print_section("1. POST (Create) - /api/users/", res_data)
            user_id = res_data["id"]
    except urllib.error.HTTPError as e:
        print_section("Error 1. POST", json.loads(e.read()))
        raise e
        
    # 2. GET (List)
    req = urllib.request.Request(base_url, method="GET")
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read())
        print_section("2. GET (List All) - /api/users/", res_data)

    # 3. GET (Retrieve)
    req = urllib.request.Request(f"{base_url}{user_id}/", method="GET")
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read())
        print_section(f"3. GET (Details) - /api/users/{user_id}/", res_data)

    # 4. PATCH (Update)
    req = urllib.request.Request(f"{base_url}{user_id}/", method="PATCH")
    req.add_header("Content-Type", "application/json")
    data = json.dumps({"name": "Maria Silva de Souza"}).encode('utf-8')
    with urllib.request.urlopen(req, data=data) as response:
        res_data = json.loads(response.read())
        print_section(f"4. PATCH (Update Partial) - /api/users/{user_id}/", res_data)

    # 5. DELETE
    req = urllib.request.Request(f"{base_url}{user_id}/", method="DELETE")
    with urllib.request.urlopen(req) as response:
        outputs.append(f"### 5. DELETE - /api/users/{user_id}/\n```text\nStatus {response.status}\nNo Content\n```\n")

    # 6. GET (List again to verify deletion)
    req = urllib.request.Request(base_url, method="GET")
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read())
        print_section("6. GET (List After Delete) - /api/users/", res_data)

except Exception as e:
    outputs.append(f"### Exception Details\n```text\n{traceback.format_exc()}\n```\n")

# Write output to test_output.md
with open("test_output.md", "w", encoding="utf-8") as f:
    f.write("\n".join(outputs))
