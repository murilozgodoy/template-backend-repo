from fastapi import Request, Response


class CheckSessionValidityUseCase:
    def execute(self, response: Response, request: Request):
        return {
            "status": "success",
            "message": "Autenticação é válida para acessar a página do usuário",
        }
