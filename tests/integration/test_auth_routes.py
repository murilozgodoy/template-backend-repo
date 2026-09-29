from models.user_model import UserModel

USUARIO = {"name": "Joao Silva", "email": "joao@example.com", "password": "senha123"}


def registrar(client, dados=USUARIO):
    return client.post("/user/auth/register", json=dados)


def login(client, email=USUARIO["email"], password=USUARIO["password"]):
    return client.post("/user/auth/login", json={"email": email, "password": password})


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_registro_cria_usuario_com_senha_em_hash(client, db_session):
    response = registrar(client)

    assert response.status_code == 201
    usuario = db_session.query(UserModel).filter_by(email=USUARIO["email"]).one()
    assert usuario.password != USUARIO["password"]


def test_registro_com_email_duplicado_retorna_409(client):
    registrar(client)

    response = registrar(client)

    assert response.status_code == 409


def test_registro_com_campo_extra_e_rejeitado(client):
    response = registrar(client, {**USUARIO, "admin": True})

    assert response.status_code == 422


def test_login_com_sucesso_devolve_cookie(client):
    registrar(client)

    response = login(client)

    assert response.status_code == 202
    assert "user_auth_token" in response.cookies


def test_login_com_senha_errada_retorna_400(client):
    registrar(client)

    response = login(client, password="errada")

    assert response.status_code == 400


def test_check_token_sem_cookie_retorna_401(client):
    response = client.post("/user/auth/check/token")

    assert response.status_code == 401


def test_check_token_com_token_invalido_retorna_401(client):
    client.cookies.set("user_auth_token", "Bearer token-invalido")

    response = client.post("/user/auth/check/token")

    assert response.status_code == 401


def test_check_token_com_cookie_malformado_retorna_401(client):
    client.cookies.set("user_auth_token", "cookie-sem-o-prefixo-bearer")

    response = client.post("/user/auth/check/token")

    assert response.status_code == 401


def test_cors_libera_so_o_front_configurado(client):
    preflight = {"Access-Control-Request-Method": "POST"}

    permitido = client.options(
        "/user/auth/login", headers={**preflight, "Origin": "http://localhost:5173"}
    )
    bloqueado = client.options(
        "/user/auth/login", headers={**preflight, "Origin": "https://site-qualquer.com"}
    )

    assert permitido.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert "access-control-allow-origin" not in bloqueado.headers


def test_check_token_com_login_valido_retorna_200(client):
    registrar(client)
    token = login(client).cookies["user_auth_token"]
    client.cookies.set("user_auth_token", token)

    response = client.post("/user/auth/check/token")

    assert response.status_code == 200


def test_fluxo_completo_de_recuperacao_de_senha(client, db_session):
    registrar(client)

    pedido = client.post("/user/auth/pwd/recovery/email", json={"email": USUARIO["email"]})
    assert pedido.status_code == 200

    usuario = db_session.query(UserModel).filter_by(email=USUARIO["email"]).one()
    db_session.refresh(usuario)
    token = usuario.reset_pwd_token

    reset = client.post("/user/auth/reset/pwd", json={"token": token, "password": "nova456"})
    assert reset.status_code == 200

    assert login(client, password="senha123").status_code == 400
    assert login(client, password="nova456").status_code == 202
