import ReactDOM from 'react-dom/client';

// Test ultra-simple
function TestApp() {
    return (
        <div style={{
            background: 'blue',
            color: 'white',
            minHeight: '100vh',
            padding: '20px',
            fontSize: '24px'
        }}>
            <h1>🚀 REACT FONCTIONNE !</h1>
            <p>Si vous voyez cette page BLEUE, React marche parfaitement !</p>
        </div>
    );
}

console.log('🔥 main.jsx commence à charger...');

const root = ReactDOM.createRoot(document.getElementById('root'));
console.log('🔥 Root créé:', root);

root.render(<TestApp />);
console.log('🔥 React rendu !');
