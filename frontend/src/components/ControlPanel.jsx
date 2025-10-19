import React, { useEffect, useState } from 'react';
import './ControlPanel.css';

const ControlPanel = () => {
    const [connected, setConnected] = useState(false);
    const [stats, setStats] = useState({
        connections: 0,
        themes: 0,
        uptime: '00:00:00'
    });
    const [logs, setLogs] = useState([]);
    const [ws, setWs] = useState(null);

    useEffect(() => {
        connectWebSocket();
        return () => {
            if (ws) ws.close();
        };
    }, []);

    const connectWebSocket = () => {
        try {
            const websocket = new WebSocket('ws://localhost:8000/ws/control-panel');
      
            websocket.onopen = () => {
                setConnected(true);
                addLog('success', 'WebSocket connecté');
                setWs(websocket);
            };

            websocket.onmessage = (event) => {
                const message = JSON.parse(event.data);
                handleWebSocketMessage(message);
            };

            websocket.onclose = () => {
                setConnected(false);
                addLog('error', 'WebSocket déconnecté');
                // Reconnexion automatique
                setTimeout(connectWebSocket, 5000);
            };

            websocket.onerror = (error) => {
                addLog('error', `Erreur WebSocket: ${error.message}`);
            };

        } catch (error) {
            addLog('error', `Erreur connexion: ${error.message}`);
        }
    };

    const handleWebSocketMessage = (message) => {
        switch (message.type) {
            case 'theme_generated':
                addLog('success', `Thème généré: ${message.user.nom}`);
                setStats(prev => ({ ...prev, themes: prev.themes + 1 }));
                break;
      
            case 'server_status':
                addLog('info', `Serveur: ${message.status}`);
                if (message.details?.connections !== undefined) {
                    setStats(prev => ({ ...prev, connections: message.details.connections }));
                }
                break;
        
            case 'file_change':
                addLog('info', `Fichier ${message.change_type}: ${message.file_path}`);
                break;
        
            case 'api_call':
                addLog('info', `API ${message.method} ${message.endpoint} - ${message.status} (${message.duration}ms)`);
                break;
        
            case 'pong':
                // Heartbeat response
                break;
        
            default:
                addLog('info', `Message: ${message.type}`);
        }
    };

    const addLog = (level, message) => {
        const newLog = {
            id: Date.now(),
            level,
            message,
            timestamp: new Date().toLocaleTimeString()
        };
    
        setLogs(prev => [newLog, ...prev.slice(0, 99)]); // Garder seulement 100 logs
    };

    const testAPI = async () => {
        const testData = {
            nom: 'Test Control Panel',
            ville_naissance: 'New York',
            date_naissance: '01/01/1990',
            heure_naissance: '12:00'
        };

        try {
            addLog('info', 'Test API en cours...');
            const response = await fetch('http://localhost:8000/api/generer-svg', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(testData)
            });

            if (response.ok) {
                const result = await response.json();
                addLog('success', 'Test API réussi!');
            } else {
                addLog('error', `Test API échoué: ${response.status}`);
            }
        } catch (error) {
            addLog('error', `Erreur API: ${error.message}`);
        }
    };

    const getStatusAPI = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/status');
            if (response.ok) {
                const status = await response.json();
                setStats(prev => ({
                    ...prev,
                    connections: status.connections
                }));
                addLog('info', `Statut serveur récupéré: ${status.status}`);
            }
        } catch (error) {
            addLog('error', `Erreur statut: ${error.message}`);
        }
    };

    const clearLogs = () => {
        setLogs([]);
        addLog('info', 'Logs effacés');
    };

    const sendPing = () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'ping' }));
            addLog('info', 'Ping envoyé');
        }
    };

    return (
        <div className="control-panel">
            <div className="panel-header">
                <h1>🌟 AstroSource Control Panel Pro</h1>
                <div className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
                    {connected ? '✅ Connecté' : '❌ Déconnecté'}
                </div>
            </div>

            <div className="panel-grid">
                <div className="panel-section">
                    <h3>📊 Statistiques Temps Réel</h3>
                    <div className="stats-grid">
                        <div className="stat-item">
                            <span className="stat-label">Connexions:</span>
                            <span className="stat-value">{stats.connections}</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-label">Thèmes générés:</span>
                            <span className="stat-value">{stats.themes}</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-label">Uptime:</span>
                            <span className="stat-value">{stats.uptime}</span>
                        </div>
                    </div>
                </div>

                <div className="panel-section">
                    <h3>🎯 Actions Rapides</h3>
                    <div className="actions-grid">
                        <button onClick={testAPI} className="action-btn test">
              🧪 Test API
                        </button>
                        <button onClick={getStatusAPI} className="action-btn status">
              📊 Statut Serveur
                        </button>
                        <button onClick={connectWebSocket} className="action-btn reconnect">
              🔄 Reconnecter
                        </button>
                        <button onClick={sendPing} className="action-btn ping">
              📡 Ping
                        </button>
                        <button onClick={clearLogs} className="action-btn clear">
              🗑️ Clear Logs
                        </button>
                        <button 
                            onClick={() => window.open('http://localhost:5173', '_blank')} 
                            className="action-btn browser"
                        >
              🌐 Ouvrir Interface
                        </button>
                    </div>
                </div>

                <div className="panel-section logs-section">
                    <h3>📝 Logs Temps Réel</h3>
                    <div className="logs-container">
                        {logs.map(log => (
                            <div key={log.id} className={`log-entry log-${log.level}`}>
                                <span className="log-time">{log.timestamp}</span>
                                <span className="log-message">{log.message}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="panel-section">
                    <h3>🔧 Outils Développement</h3>
                    <div className="dev-tools">
                        <div className="tool-item">
                            <strong>Backend:</strong> http://localhost:8000
                        </div>
                        <div className="tool-item">
                            <strong>Frontend:</strong> http://localhost:5173
                        </div>
                        <div className="tool-item">
                            <strong>API Docs:</strong> http://localhost:8000/docs
                        </div>
                        <div className="tool-item">
                            <strong>WebSocket:</strong> ws://localhost:8000/ws/
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ControlPanel;
