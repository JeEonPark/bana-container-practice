from fastapi import APIRouter, Request, Response
import socket
import os

router = APIRouter()

@router.get("/frontend-info")
def get_frontend_info(request: Request, response: Response):
    """フロントエンドのPod情報を返すエンドポイント"""
    # クライアントのIPアドレスを取得
    client_ip = request.client.host
    
    # 環境判定
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        # Kubernetes環境ではPod名を返す
        pod_name = socket.gethostname()
        pod_ip = socket.gethostbyname(socket.gethostname())
        node_name = os.getenv("NODE_NAME", "unknown")
    else:
        # 開発環境ではMacの情報を返す
        pod_name = socket.getfqdn()
        pod_ip = socket.gethostbyname(socket.gethostname())
        node_name = "localhost"
    
    # レスポンスヘッダーにPod情報を追加
    response.headers["X-Pod-Name"] = pod_name
    response.headers["X-Pod-IP"] = pod_ip
    response.headers["X-Node-Name"] = node_name
    response.headers["X-Client-IP"] = client_ip
    
    return {
        "pod_name": pod_name,
        "pod_ip": pod_ip,
        "node_name": node_name,
        "client_ip": client_ip,
        "environment": env
    } 
