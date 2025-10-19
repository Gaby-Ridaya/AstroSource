"""
WebSocket Manager pour synchronisation temps réel
AstroSource Pro Control Panel
"""
import asyncio
import json
import logging
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.watchers: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connecté: {client_id or 'Anonymous'}")
        
        # Envoyer le statut initial
        await self.send_personal_message({
            "type": "connected",
            "message": "Connexion WebSocket établie",
            "timestamp": datetime.now().isoformat(),
            "client_id": client_id
        }, websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        # Retirer de tous les watchers
        for path in list(self.watchers.keys()):
            self.watchers[path].discard(websocket)
            if not self.watchers[path]:
                del self.watchers[path]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Erreur envoi message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        """Diffuser un message à tous les clients connectés"""
        if not self.active_connections:
            return
        
        message["timestamp"] = datetime.now().isoformat()
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur broadcast: {e}")
                disconnected.add(connection)
        
        # Nettoyer les connexions fermées
        for connection in disconnected:
            self.disconnect(connection)
    
    async def notify_file_change(self, file_path: str, change_type: str):
        """Notifier un changement de fichier"""
        message = {
            "type": "file_change",
            "file_path": file_path,
            "change_type": change_type,  # created, modified, deleted
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def notify_theme_generated(self, user_data: dict, files: dict):
        """Notifier qu'un nouveau thème a été généré"""
        message = {
            "type": "theme_generated",
            "user": user_data,
            "files": files,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def notify_server_status(self, status: str, details: dict = None):
        """Notifier le statut du serveur"""
        message = {
            "type": "server_status", 
            "status": status,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def notify_api_call(self, endpoint: str, method: str, status: int, duration: float):
        """Notifier un appel API"""
        message = {
            "type": "api_call",
            "endpoint": endpoint,
            "method": method,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)

# Instance globale
websocket_manager = WebSocketManager()
